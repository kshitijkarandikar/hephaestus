#!/usr/bin/env python3
"""kit: the freelancer kit's one command. Built from spec/*.md. Standard library only.

Parts, in order: helpers, work log, report, security engine, check/hook, calc, pdf, doctor, main.
"""
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

getcontext().prec = 60

# ROOT is the kit folder: the parent of core/. Symlinks resolved so path checks are stable.
ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

HELP = """kit commands:
  kit log add key=value ...        add a work log entry
  kit log list [date=YYYY-MM-DD]   show one day
  kit log verify                   check the hash chain
  kit report from= to= ...         hours report
  kit check scan <file>            find secrets, personal data, injection
  kit check command "<cmd>"        decision for a shell command
  kit check read <path>            decision for reading a file
  kit check write <path>           decision for writing a file
  kit check tool <name>            decision for a connector tool
  kit check selftest               run security/tests/*.json
  kit check show                   print the rules in force
  kit check integrity              verify the checksum seal
  kit check seal                   write the checksum seal
  kit hook                         Claude Code hook (JSON on stdin)
  kit calc "<expression>"          safe money math
  kit pdf <html file> [pdf file]   HTML to PDF with a local browser
  kit doctor                       health check of the whole kit
  kit google ...                   Gmail, Calendar, Drive (optional; kit google help)"""


class KitError(Exception):
    """A user mistake: print the message to stderr and exit 1."""


def fail(msg, code=1):
    sys.stderr.write(msg + "\n")
    sys.exit(code)


def parse_kv(words):
    """Turn ['a=b', 'c=d e'] into {'a': 'b', 'c': 'd e'}. Words without '=' are ignored."""
    out = {}
    for w in words:
        if "=" in w:
            k, v = w.split("=", 1)
            out[k.strip()] = v
    return out


def now():
    """Local date and time as (YYYY-MM-DD, HH:MM). KIT_NOW overrides (tests only)."""
    env = os.environ.get("KIT_NOW")
    if env:
        m = re.match(r"^(\d{4}-\d{2}-\d{2})[ T](\d{2}:\d{2})", env.strip())
        if m:
            return m.group(1), m.group(2)
    n = datetime.datetime.now()
    return n.strftime("%Y-%m-%d"), n.strftime("%H:%M")


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


# --------------------------------------------------------------------------
# Work log
# --------------------------------------------------------------------------

KEY_ORDER = ["id", "time", "kind", "client", "task", "skill", "tool", "minutes", "billable",
             "files", "outcome", "notes", "corrects", "sample"]
KINDS = ["work", "approval", "blocked", "tool", "note"]


def worklog_dir():
    return os.environ.get("KIT_WORKLOG_DIR") or os.path.join(ROOT, "worklog")


def canon_str(s):
    """JSON string, compact rules from worklog.md: escape only quote, backslash, controls."""
    out = ['"']
    names = {"\b": "\\b", "\t": "\\t", "\n": "\\n", "\f": "\\f", "\r": "\\r"}
    for ch in s:
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch in names:
            out.append(names[ch])
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def canonical(x):
    """Canonical JSON: no spaces, stored key order, no null."""
    if x is True:
        return "true"
    if x is False:
        return "false"
    if isinstance(x, str):
        return canon_str(x)
    if isinstance(x, int):
        return str(x)
    if isinstance(x, float):
        if x == int(x):
            return str(int(x))
        return repr(x)
    if isinstance(x, list):
        return "[" + ",".join(canonical(i) for i in x) + "]"
    if isinstance(x, dict):
        return "{" + ",".join(canon_str(k) + ":" + canonical(v) for k, v in x.items()) + "}"
    raise TypeError("cannot encode %r" % (x,))


def entry_hash(prev, entry):
    body = {k: v for k, v in entry.items() if k not in ("prev", "hash")}
    return sha256_hex((prev + canonical(body)).encode("utf-8"))


DAY_RE = re.compile(r"^\d{4}-\d{2}-\d{2}\.json$")


def day_files(d):
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if DAY_RE.match(f))


def read_day(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_day(path, data):
    """Write to a temp file in the same folder, then rename over the real file."""
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-", suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


class Lock:
    """Lock by creating the folder <worklog>/.lock (mkdir is atomic)."""

    def __init__(self, d):
        self.path = os.path.join(d, ".lock")

    def __enter__(self):
        for _ in range(100):
            try:
                os.mkdir(self.path)
                return self
            except FileExistsError:
                try:
                    if time.time() - os.path.getmtime(self.path) > 10:  # stale lock
                        os.rmdir(self.path)
                        continue
                except OSError:
                    pass
                time.sleep(0.03)
        raise KitError("worklog is locked")

    def __exit__(self, *a):
        try:
            os.rmdir(self.path)
        except OSError:
            pass


def truthy(v):
    return v.strip().lower() in ("true", "yes")


def log_add(kv):
    """Add one entry. Returns the printed confirmation line. Raises KitError on bad input."""
    kv = {k: v for k, v in kv.items() if v != ""}
    kind = kv.get("kind", "work")
    if kind not in KINDS:
        raise KitError("Error: kind must be one of " + ", ".join(KINDS))
    if kind == "work" and not kv.get("task"):
        raise KitError("Error: task is required for kind work")
    minutes = None
    if "minutes" in kv:
        try:
            minutes = float(kv["minutes"])
        except ValueError:
            raise KitError("Error: minutes must be a number")
        if minutes != minutes or minutes in (float("inf"), float("-inf")) or minutes < 0:
            raise KitError("Error: minutes must be a number of 0 or more")
        if minutes == int(minutes):
            minutes = int(minutes)
    date, hhmm = now()
    d = worklog_dir()
    os.makedirs(d, exist_ok=True)
    with Lock(d):
        path = os.path.join(d, date + ".json")
        day = read_day(path) if os.path.exists(path) else {"date": date, "entries": []}
        # prev: last entry of this day, else of the latest earlier day that has entries
        prev = ""
        if day["entries"]:
            prev = day["entries"][-1].get("hash", "")
        else:
            for f in reversed([f for f in day_files(d) if f < date + ".json"]):
                es = read_day(os.path.join(d, f)).get("entries", [])
                if es:
                    prev = es[-1].get("hash", "")
                    break
        nums = [int(e["id"].rsplit("-", 1)[1]) for e in day["entries"]
                if re.search(r"-\d+$", e.get("id", ""))]
        eid = "%s-%03d" % (date, (max(nums) if nums else 0) + 1)
        e = {"id": eid, "time": hhmm, "kind": kind}
        for k in ("client", "task", "skill", "tool"):
            if k in kv:
                e[k] = kv[k]
        if minutes is not None:
            e["minutes"] = minutes
        if "billable" in kv:
            e["billable"] = truthy(kv["billable"])
        elif kind == "work":
            e["billable"] = True
        if "files" in kv:
            files = [x.strip() for x in kv["files"].split(",") if x.strip()]
            if files:
                e["files"] = files
        for k in ("outcome", "notes", "corrects"):
            if k in kv:
                e[k] = kv[k]
        if "sample" in kv:
            e["sample"] = truthy(kv["sample"])
        e["prev"] = prev
        e["hash"] = entry_hash(prev, e)
        day["entries"].append(e)
        write_day(path, day)
    return "logged %s (%s): %s" % (eid, kind, e.get("task") or e.get("notes") or "")


def log_verify(d=None):
    """Returns (ok, message)."""
    d = d or worklog_dir()
    prev_seen = ""
    n = 0
    for f in day_files(d):
        for e in read_day(os.path.join(d, f)).get("entries", []):
            if e.get("prev", "") != prev_seen:
                return False, "BROKEN at %s %s: link to the previous entry is broken (entry removed or reordered?)" % (f, e.get("id"))
            if entry_hash(prev_seen, e) != e.get("hash"):
                return False, "BROKEN at %s %s: entry content was changed after it was written" % (f, e.get("id"))
            prev_seen = e["hash"]
            n += 1
    return True, "OK: %d entries, chain intact" % n


def cmd_log(args):
    sub = args[0] if args else ""
    kv = parse_kv(args[1:])
    if sub == "add":
        try:
            print(log_add(kv))
        except KitError as ex:
            fail(str(ex))
    elif sub == "list":
        date = kv.get("date") or now()[0]
        path = os.path.join(worklog_dir(), date + ".json")
        entries = read_day(path).get("entries", []) if os.path.exists(path) else []
        if not entries:
            print("no entries for " + date)
            return 0
        for e in entries:
            line = "%s %s [%s] " % (e["id"], e.get("time", ""), e.get("kind", ""))
            if e.get("client"):
                line += e["client"] + ": "
            line += e.get("task") or e.get("notes") or ""
            if e.get("minutes"):
                line += " (%s min)" % canonical(e["minutes"])
            print(line)
    elif sub == "verify":
        ok, msg = log_verify()
        if ok:
            print(msg)
            return 0
        fail(msg)
    else:
        fail("Usage: kit log add|list|verify")
    return 0


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def hours(minutes):
    """minutes -> Decimal hours, 2 decimals, half up."""
    return (Decimal(minutes) / Decimal(60)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def cmd_report(args):
    o = parse_kv(args)
    frm = o.get("from") or "0000-01-01"
    to = o.get("to") or "9999-12-31"
    by = o.get("by") or "client"
    fmt = o.get("format") or "text"
    if by not in ("client", "skill", "day"):
        fail("by must be client, skill or day")
    if fmt not in ("text", "md", "json"):
        fail("format must be text, md or json")
    d = worklog_dir()
    groups = {}
    missing = []
    for f in day_files(d):
        date = f[:-5]
        if date < frm or date > to:
            continue
        for e in read_day(os.path.join(d, f)).get("entries", []):
            if e.get("kind") != "work":
                continue
            if o.get("client") and (e.get("client", "").lower() != o["client"].lower()):
                continue
            if "billable" in o and o["billable"] != "":
                want = truthy(o["billable"])
                if (e.get("billable") is not False) != want:
                    continue
            if "minutes" not in e:
                missing.append((date, e.get("id", ""), e.get("task", "")))
                continue
            key = {"client": e.get("client") or "(no client)",
                   "skill": e.get("skill") or "(none)", "day": date}[by]
            g = groups.setdefault(key, [Decimal(0), Decimal(0)])
            g[0] += Decimal(str(e["minutes"]))
            if e.get("billable") is not False:
                g[1] += Decimal(str(e["minutes"]))
    tot = sum((g[0] for g in groups.values()), Decimal(0))
    totb = sum((g[1] for g in groups.values()), Decimal(0))
    keys = sorted(groups)
    total_line = "Total: %s h, billable %s h" % (hours(tot), hours(totb))
    miss_lines = []
    if missing:
        miss_lines = ["", "%d work entries have no minutes and are NOT counted:" % len(missing)]
        miss_lines += ["- %s: %s" % (i, t) for (_, i, t) in missing]
    if fmt == "json":
        out = {"from": frm, "to": to, "by": by,
               "groups": {k: {"hours": float(hours(groups[k][0])),
                              "billable_hours": float(hours(groups[k][1]))} for k in keys},
               "total_hours": float(hours(tot)), "billable_hours": float(hours(totb)),
               "entries_without_minutes": [{"date": a, "id": b, "task": c} for a, b, c in missing]}
        text = json.dumps(out, indent=2, ensure_ascii=False)
    elif fmt == "md":
        lines = ["# Hours report %s to %s" % (frm, to), "",
                 "| %s | Hours | Billable hours |" % by, "|---|---|---|"]
        lines += ["| %s | %s | %s |" % (k, hours(groups[k][0]), hours(groups[k][1])) for k in keys]
        lines += ["", total_line] + miss_lines
        text = "\n".join(lines)
    else:
        lines = ["Hours report %s to %s" % (frm, to), ""]
        lines += ["%s %7s h   billable %7s h" % (k.ljust(24), hours(groups[k][0]), hours(groups[k][1]))
                  for k in keys]
        lines += ["", total_line] + miss_lines
        text = "\n".join(lines)
    print(text)
    if o.get("save") and truthy(o["save"]):
        name = "%s-hours-report.%s" % (now()[0], "json" if fmt == "json" else "md")
        os.makedirs(os.path.join(ROOT, "outputs"), exist_ok=True)
        with open(os.path.join(ROOT, "outputs", name), "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print("Saved outputs/" + name)
    return 0


# --------------------------------------------------------------------------
# Security engine
# --------------------------------------------------------------------------

STRICT = {"allow": 0, "ask": 1, "deny": 2}


def stricter(a, b):
    return a if STRICT[a] >= STRICT[b] else b


def rx(p):
    return re.compile(p, re.IGNORECASE)


def load_rules():
    """Load rules.json plus extensions. Returns (rules, loaded_names, warnings)."""
    with open(os.path.join(ROOT, "security", "rules.json"), encoding="utf-8") as f:
        rules = json.load(f)
    loaded, warnings = [], []
    ext_dir = os.path.join(ROOT, "security", "extensions")
    files = sorted(x for x in os.listdir(ext_dir) if x.endswith(".json")) if os.path.isdir(ext_dir) else []
    list_keys = ["read_deny", "write_deny", "command_deny", "command_ask", "mcp_tool_rules",
                 "blocked_mcp_servers", "injection_patterns", "confidential_terms"]
    for name in files:
        try:
            with open(os.path.join(ext_dir, name), encoding="utf-8") as f:
                ext = json.load(f)
            if not isinstance(ext, dict):
                raise ValueError("top level is not an object")
        except Exception as ex:
            warnings.append("%s: not valid JSON, ignored (%s)" % (name, ex))
            continue
        loaded.append(name)
        for key, val in ext.items():
            if key == "description":
                continue
            if key in ("command_allow", "write_allow", "write_ask"):
                warnings.append('%s: "%s" would loosen the rules. Edit rules.json by hand for that. Ignored.' % (name, key))
            elif key in list_keys:
                cur = rules.setdefault(key, [])
                for item in val:
                    if item not in cur:
                        cur.append(item)
            elif key == "actions":
                acts = rules.setdefault("actions", {})
                for a, dec in val.items():
                    acts[a] = stricter(acts[a], dec) if a in acts else dec
            elif key == "scan_patterns":
                rules.setdefault("scan_patterns", {}).update(val)
            elif key == "default_decision":
                rules["default_decision"] = stricter(rules.get("default_decision", "ask"), val)
            else:
                warnings.append('%s: unknown key "%s", ignored' % (name, key))
    return rules, loaded, warnings


def glob_re(g):
    """Turn a glob into a regex that must match the whole path."""
    if g.startswith("~/"):
        g = os.path.expanduser("~").replace("\\", "/") + g[1:]
    if g == "**":
        return rx(r".*")
    out = ""
    i = 0
    trailing = g.endswith("/**")
    if trailing:
        g = g[:-3]
    while i < len(g):
        if g.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif g[i] == "*":
            out += "[^/]*"
            i += 1
        elif g[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(g[i])
            i += 1
    if trailing:
        out += "(?:/.*)?"
    return rx("^" + out + "$")


def locate(p):
    if p.startswith("~/"):
        p = os.path.join(os.path.expanduser("~"), p[2:])
    full = p if os.path.isabs(p) else os.path.join(ROOT, p)
    full = os.path.normpath(full)
    if os.path.exists(full):
        ab = os.path.realpath(full)
    else:
        ab = os.path.join(os.path.realpath(os.path.dirname(full)), os.path.basename(full))
    try:
        rel = os.path.relpath(ab, ROOT).replace("\\", "/")
    except ValueError:  # another drive on Windows
        rel = ab.replace("\\", "/")
    outside = rel.startswith("..") or os.path.isabs(rel)
    return {"abs": ab.replace("\\", "/"), "rel": rel, "outside": outside}


def path_match(globs, loc):
    for g in globs:
        r = glob_re(g)
        if r.match(loc["abs"]) or (not loc["outside"] and r.match(loc["rel"])):
            return g
    return None


def check_path(rules, mode, p):
    loc = locate(p)
    rel = loc["rel"]
    g = path_match(rules.get("read_deny", []), loc)
    if g:
        return "deny", "%s is a secret or private file (rule %s)" % (rel, g)
    if mode == "read":
        if loc["outside"]:
            return "ask", "%s is outside the kit folder" % p
        return "allow", "inside kit folder"
    if loc["outside"]:
        return "deny", "writing outside the kit folder is not allowed (%s)" % p
    g = path_match(rules.get("write_deny", []), loc)
    if g:
        return "deny", "%s is protected (rule %s). Only the owner edits it by hand" % (rel, g)
    g = path_match(rules.get("write_ask", []), loc)
    if g:
        return "ask", "changing %s needs the owner's ok (rule %s)" % (rel, g)
    g = path_match(rules.get("write_allow", []), loc)
    if g:
        return "allow", "%s is a normal output location" % rel
    return rules.get("default_decision", "ask"), "%s matches no rule" % rel


QUOTED = re.compile(r'"[^"]*"|\'[^\']*\'')


def check_command(rules, cmd):
    cmd = cmd.strip()
    for r in rules.get("command_deny", []):
        if rx(r).search(cmd):
            return "deny", "command matches deny rule " + r
    stripped = QUOTED.sub('""', cmd)
    chained = bool(re.search(r"[;&|\n]", stripped))
    no_single = re.sub(r"'[^']*'", "", cmd)
    if "$(" in no_single or "`" in no_single:
        chained = True
    if not chained:
        for r in rules.get("command_allow", []):
            if rx(r).search(cmd):
                return "allow", "command matches allow rule " + r
    for r in rules.get("command_ask", []):
        if rx(r).search(cmd):
            return "ask", "command matches ask rule " + r
    return rules.get("default_decision", "ask"), ("chained command, check each part" if chained else "command matches no rule")


def check_tool(rules, name):
    if not name.startswith("mcp__"):
        return "allow", "not a connector tool"
    parts = name.split("__")
    server = parts[1] if len(parts) > 1 else ""
    tool = "_".join(parts[2:]).lower()
    for b in rules.get("blocked_mcp_servers", []):
        if b.lower() in server.lower():
            return "deny", "connector %s is blocked" % server
    best, why = None, None
    for rule in rules.get("mcp_tool_rules", []):
        if rx(rule["match"]).search(tool):
            if best is None or STRICT[rule["decision"]] > STRICT[best]:
                best, why = rule["decision"], 'connector tool "%s" matches rule "%s"' % (tool, rule["match"])
    if best:
        return best, why
    return rules.get("default_decision", "ask"), 'connector tool "%s" matches no rule' % tool


def mask(s):
    return "***" if len(s) <= 6 else s[:4] + "***" + s[-2:]


def luhn(digits):
    total = 0
    for i, ch in enumerate(reversed(digits)):
        n = int(ch)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0


def scan_text(rules, text):
    findings = []
    for ln, line in enumerate(text.splitlines(), 1):
        for name, pat in rules.get("scan_patterns", {}).items():
            for m in rx(pat["regex"]).finditer(line):
                findings.append({"type": name, "severity": pat["severity"], "line": ln, "snippet": mask(m.group(0))})
        if rules.get("card_number_check"):
            for m in rx(r"\b(?:\d[ -]?){13,19}\b").finditer(line):
                digits = re.sub(r"\D", "", m.group(0))
                if 13 <= len(digits) <= 19 and luhn(digits):
                    findings.append({"type": "card_number", "severity": "high", "line": ln, "snippet": mask(digits)})
        for pat in rules.get("injection_patterns", []):
            if rx(pat).search(line):
                findings.append({"type": "prompt_injection", "severity": "high", "line": ln, "snippet": line.strip()[:80]})
        for term in rules.get("confidential_terms", []):
            if term and term.lower() in line.lower():
                findings.append({"type": "confidential_term", "severity": "medium", "line": ln, "snippet": term})
    return findings


def selftest():
    """Returns (passed, failed, failure_lines, loaded, warnings)."""
    rules, loaded, warnings = load_rules()
    passed, failed, lines = 0, 0, []
    tdir = os.path.join(ROOT, "security", "tests")
    for f in sorted(x for x in os.listdir(tdir) if x.endswith(".json")):
        with open(os.path.join(tdir, f), encoding="utf-8") as fh:
            cases = json.load(fh)["cases"]
        for c in cases:
            t, inp, exp = c["type"], c["input"], c["expect"]
            if t == "command":
                got = check_command(rules, inp)[0]
            elif t in ("read", "write"):
                got = check_path(rules, t, inp)[0]
            elif t == "tool":
                got = check_tool(rules, inp)[0]
            else:
                types = {x["type"] for x in scan_text(rules, inp)}
                got = exp if (exp in types if exp != "none" else not types) else (",".join(sorted(types)) or "none")
            if got == exp:
                passed += 1
            else:
                failed += 1
                lines.append("FAIL %s: %s %s expected %s, got %s" % (f, t, inp[:70], exp, got))
    return passed, failed, lines, loaded, warnings


def core_files():
    """Everything in core/, plus kit, kit.cmd, security/rules.json (relative paths, sorted)."""
    out = []
    for base, dirs, files in os.walk(os.path.join(ROOT, "core")):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for f in files:
            if f.endswith(".pyc"):
                continue
            out.append(os.path.relpath(os.path.join(base, f), ROOT).replace("\\", "/"))
    for extra in ("kit", "kit.cmd", "security/rules.json"):
        if os.path.exists(os.path.join(ROOT, extra)):
            out.append(extra)
    return sorted(set(out))


def file_sha(rel):
    with open(os.path.join(ROOT, rel), "rb") as f:
        return sha256_hex(f.read())


SEAL = os.path.join(ROOT, "setup", "core.sha256.json")


def integrity():
    """Returns (ok, lines). lines are the messages to print."""
    if not os.path.exists(SEAL):
        return False, ["No seal yet. Run: kit check seal"]
    with open(SEAL, encoding="utf-8") as f:
        seal = json.load(f)
    now_files = {p: file_sha(p) for p in core_files()}
    bad = [p for p in sorted(set(seal) | set(now_files)) if seal.get(p) != now_files.get(p)]
    if bad:
        return False, ["CHANGED: " + p for p in bad]
    return True, ["OK: seal matches %d files" % len(seal)]


def cmd_check(args):
    sub = args[0] if args else ""
    rest = " ".join(args[1:])
    if sub in ("seal", "integrity"):
        if sub == "seal":
            seal = {p: file_sha(p) for p in core_files()}
            os.makedirs(os.path.dirname(SEAL), exist_ok=True)
            with open(SEAL, "w", encoding="utf-8", newline="\n") as f:
                json.dump(seal, f, indent=2)
                f.write("\n")
            print("Sealed %d files in setup/core.sha256.json" % len(seal))
            return 0
        ok, lines = integrity()
        if ok:
            print(lines[0])
            return 0
        sys.stdout.write("\n".join(lines) + "\n")
        return 1
    if sub == "selftest":
        p, f, lines, loaded, warnings = selftest()
        for w in warnings:
            sys.stderr.write("WARNING: " + w + "\n")
        for ln in lines:
            print(ln)
        print("%d passed, %d failed. Extensions loaded: %s" % (p, f, ", ".join(loaded) or "none"))
        return 1 if f else 0
    rules, loaded, warnings = load_rules()
    for w in warnings:
        sys.stderr.write("WARNING: " + w + "\n")
    if sub in ("command", "read", "write", "tool"):
        if sub == "command":
            dec, why = check_command(rules, rest)
        elif sub == "tool":
            dec, why = check_tool(rules, rest)
        else:
            dec, why = check_path(rules, sub, rest)
        print(json.dumps({"decision": dec, "reason": why}, indent=2, ensure_ascii=False))
        return 2 if dec == "deny" else 0
    if sub == "scan":
        target = args[1] if len(args) > 1 else ""
        full = os.path.join(ROOT, target) if target else ""
        if not target or not os.path.isfile(full):
            fail("Give a file that exists.")
        with open(full, encoding="utf-8", errors="replace") as f:
            findings = scan_text(rules, f.read())
        print(json.dumps({"file": target, "clean": not findings, "findings": findings}, indent=2, ensure_ascii=False))
        return 2 if any(x["severity"] == "high" for x in findings) else 0
    if sub == "show":
        print(json.dumps({"extensions_loaded": loaded, "warnings": warnings, "rules": rules}, indent=2, ensure_ascii=False))
        return 0
    fail("Usage: kit check scan|command|read|write|tool|selftest|show|integrity|seal")


def cmd_hook():
    raw = sys.stdin.read()
    try:
        ev = json.loads(raw)
        if not isinstance(ev, dict):
            return 0
    except ValueError:
        return 0
    try:
        if os.path.exists(SEAL):
            ok, lines = integrity()
            if not ok:
                first = lines[0].replace("CHANGED: ", "")
                sys.stderr.write("Security files were changed (%s). Stopped. Tell the kit owner, or reinstall the kit with: git checkout .\n" % first)
                return 2
        name = ev.get("tool_name", "")
        ti = ev.get("tool_input") or {}
        rules, _, _ = load_rules()
        if name == "Bash":
            target = ti.get("command", "")
            dec, why = check_command(rules, target)
        elif name == "Read":
            target = ti["file_path"]
            dec, why = check_path(rules, "read", target)
        elif name in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
            target = ti.get("file_path") or ti["notebook_path"]
            dec, why = check_path(rules, "write", target)
        elif name.startswith("mcp__"):
            target = name
            dec, why = check_tool(rules, name)
        else:
            return 0
    except Exception as ex:
        sys.stderr.write("Security hook error: %s\n" % ex)
        return 2
    if not (name == "Read" and dec == "allow"):
        try:
            t = target[len(ROOT):].lstrip("/") if target.startswith(ROOT) else target
            log_add({"kind": "blocked" if dec == "deny" else "tool", "tool": "claude-code",
                     "task": ("%s: %s" % (name, t))[:200], "outcome": dec, "notes": why})
        except Exception:
            pass  # a failure to log must not stop the hook
    if dec == "deny":
        sys.stderr.write("Blocked by security rules: %s\n" % why)
        return 2
    if dec == "ask":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "ask",
                                                 "permissionDecisionReason": why}}, separators=(",", ":"), ensure_ascii=False))
    return 0


# --------------------------------------------------------------------------
# calc
# --------------------------------------------------------------------------

CALC_ERR = 'Use only numbers and + - * / ( ). Example: calc "(4+5+3)*95"'


def cmd_calc(args):
    expr = " ".join(args)
    if not re.match(r"^[0-9+\-*/().\s]*$", expr) or "**" in expr or "//" in expr:
        fail(CALC_ERR)
    toks = re.findall(r"\d+\.?\d*|\.\d+|[+\-*/()]|\S", expr)
    pos = [0]

    def peek():
        return toks[pos[0]] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def expr_():
        v = term()
        while peek() in ("+", "-"):
            v = v + term() if take() == "+" else v - term()
        return v

    def term():
        v = unary()
        while peek() in ("*", "/"):
            if take() == "*":
                v = v * unary()
            else:
                v = v / unary()  # Decimal raises on zero
        return v

    def unary():
        t = peek()
        if t == "-":
            take()
            return -unary()
        if t == "+":
            take()
            return unary()
        if t == "(":
            take()
            v = expr_()
            if take() != ")":
                raise ValueError
            return v
        if t is None:
            raise ValueError
        take()
        return Decimal(t)  # raises on junk such as "1.2.3" or a lone "."

    try:
        v = expr_()
        if pos[0] != len(toks):
            raise ValueError
        out = v.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (ValueError, InvalidOperation, ZeroDivisionError, IndexError, ArithmeticError):
        fail("That is not a valid calculation.")
    if out == 0:
        out = abs(out)  # no "-0.00"
    print(format(out, "f"))
    return 0


# --------------------------------------------------------------------------
# pdf and doctor
# --------------------------------------------------------------------------

def find_browser():
    if sys.platform == "darwin":
        c = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
             "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
             "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    elif sys.platform.startswith("win"):
        pf86, pf, la = (os.environ.get(k, "") for k in ("ProgramFiles(x86)", "ProgramFiles", "LOCALAPPDATA"))
        c = [pf86 + r"\Microsoft\Edge\Application\msedge.exe", pf + r"\Microsoft\Edge\Application\msedge.exe",
             pf + r"\Google\Chrome\Application\chrome.exe", la + r"\Google\Chrome\Application\chrome.exe"]
    else:
        c = ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/microsoft-edge"]
    for p in c:
        if os.path.isfile(p):
            return p
    return None


def inside(path, folder):
    return os.path.realpath(path).startswith(os.path.realpath(folder) + os.sep)


def cmd_pdf(args):
    if not args:
        fail("Usage: kit pdf <html file> [pdf file]")
    src = os.path.join(ROOT, args[0])
    if not os.path.exists(src):
        fail("File not found: " + args[0])
    if not (inside(src, os.path.join(ROOT, "outputs")) or inside(src, os.path.join(ROOT, "context", "templates"))):
        fail("Only files in outputs/ or context/templates/ can be printed.")
    if len(args) > 1:
        pdf = os.path.join(ROOT, args[1])
    else:
        pdf = os.path.join(ROOT, "outputs", os.path.splitext(os.path.basename(src))[0] + ".pdf")
    pdf = os.path.join(os.path.realpath(os.path.dirname(pdf)), os.path.basename(pdf))
    if not inside(pdf, os.path.join(ROOT, "outputs")):
        fail("The PDF must go in outputs/.")
    browser = find_browser()
    if not browser:
        fail("No Chrome or Edge found. Open the HTML file and use Print, Save as PDF.", 2)
    prof = tempfile.mkdtemp(prefix="kit-pdf-")
    url = "file://" + os.path.realpath(src) if not sys.platform.startswith("win") else "file:///" + os.path.realpath(src).replace("\\", "/")
    base = [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--user-data-dir=" + prof, "--print-to-pdf=" + pdf]
    err = ""
    for extra in ([], ["--no-sandbox", "--blink-settings=scriptEnabled=false"]):
        try:
            r = subprocess.run(base[:1] + extra + base[1:] + [url], timeout=45,
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            err = r.stderr.decode("utf-8", "replace").strip().splitlines()[-1:] or [""]
            err = err[0][:200]
        except subprocess.TimeoutExpired:
            err = "the browser took too long"
        if os.path.exists(pdf):
            if extra:
                sys.stderr.write("Note: Chrome's own sandbox could not start here (your AI tool already sandboxes it), so the PDF was made without it and with scripts off.\n")
            break
    shutil.rmtree(prof, ignore_errors=True)
    if not os.path.exists(pdf):
        fail("No PDF was made." + (" Browser said: " + err if err else "") +
             " Try again in a normal terminal window, or open the HTML file and use Print, Save as PDF.")
    print(pdf)
    return 0


def cmd_doctor():
    bad = False
    print("Kit health check")

    def line(tag, text):
        print("  [%s]%s%s" % (tag, " " * (3 if tag == "ok" else 1 if tag == "warn" else 1), text))

    line("ok", "Runtime: Python " + sys.version.split()[0])
    try:
        p, f, _, loaded, _ = selftest()
        if f:
            bad = True
            line("FAIL", "Security rules: %d passed, %d failed" % (p, f))
        else:
            line("ok", "Security rules: %d passed, 0 failed. Extensions loaded: %s" % (p, ", ".join(loaded) or "none"))
    except Exception as ex:
        bad = True
        line("FAIL", "Security rules: %s" % ex)
    try:
        ok, msg = log_verify()
        if not ok:
            bad = True
        line("ok" if ok else "FAIL", "Work log: " + msg)
    except Exception as ex:
        bad = True
        line("FAIL", "Work log: %s" % ex)
    try:
        ok, lines = integrity()
        if ok:
            line("ok", "Integrity seal: " + lines[0])
        elif not os.path.exists(SEAL):
            line("warn", "Integrity seal: " + lines[0])
        else:
            bad = True
            line("FAIL", "Integrity seal: " + ", ".join(lines))
    except Exception as ex:
        bad = True
        line("FAIL", "Integrity seal: %s" % ex)
    b = find_browser()
    line("ok" if b else "warn", "Browser for PDF: " + (b if b else "none found, PDF will not work"))
    found = [t for t in ("claude", "codex", "gemini") if shutil.which(t)]
    line("ok" if found else "warn", "AI tools on the PATH: " + (", ".join(found) if found else "none found"))
    if bad:
        print("Fix the problems above.")
        return 1
    print("All good.")
    return 0


def main(argv):
    if not argv or argv[0] in ("help", "-h", "--help"):
        print(HELP)
        return 0
    cmd, rest = argv[0], argv[1:]
    try:
        if cmd == "log":
            return cmd_log(rest)
        if cmd == "report":
            return cmd_report(rest)
        if cmd == "check":
            return cmd_check(rest)
        if cmd == "hook":
            return cmd_hook()
        if cmd == "calc":
            return cmd_calc(rest)
        if cmd == "pdf":
            return cmd_pdf(rest)
        if cmd == "doctor":
            return cmd_doctor()
        if cmd == "google":
            import importlib.util
            gp = os.path.join(ROOT, "core", "google.py")
            spec = importlib.util.spec_from_file_location("kit_google", gp)
            gm = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(gm)
            return gm.main(rest, sys.modules[__name__])
    except KitError as ex:
        fail(str(ex))
    except (OSError, ValueError, KeyError) as ex:
        fail("Error: %s" % ex)
    fail("Unknown command: %s\n%s" % (cmd, HELP))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
