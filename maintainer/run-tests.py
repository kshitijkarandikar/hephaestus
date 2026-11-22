#!/usr/bin/env python3
"""Maintainer test runner. Run from anywhere: python3 maintainer/run-tests.py
Runs: security rule tests, CLI conformance, work log scenario, Google offline tests.
Uses temp folders for the work log, so the real worklog/ is never touched."""
import json, os, re, shutil, subprocess, sys, tempfile

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = 0


def run(cmd, env_extra=None, temp_log=True):
    env = dict(os.environ)
    if temp_log:
        env["KIT_WORKLOG_DIR"] = tempfile.mkdtemp()
    env.update(env_extra or {})
    return subprocess.run(cmd, shell=True, cwd=KIT, capture_output=True, text=True, env=env)


def lst(t, k):
    v = t.get(k, [])
    return [v] if isinstance(v, str) else v


def sub(a, b):
    return all(k in b and (sub(v, b[k]) if isinstance(v, dict) else v == b[k]) for k, v in a.items())


def check(t, r):
    e = []
    if r.returncode != t["exit"]:
        e.append("exit %d != %d" % (r.returncode, t["exit"]))
    for x in lst(t, "stdout_contains"):
        if x not in r.stdout:
            e.append("stdout missing %r" % x)
    for x in lst(t, "stderr_contains"):
        if x not in r.stderr:
            e.append("stderr missing %r" % x)
    for x in lst(t, "stdout_not_contains"):
        if x in r.stdout:
            e.append("stdout has forbidden %r" % x)
    if "stdout" in t and r.stdout.rstrip("\n") != t["stdout"].rstrip("\n"):
        e.append("stdout differs")
    if "stderr" in t and r.stderr.rstrip("\n") != t["stderr"].rstrip("\n"):
        e.append("stderr differs")
    if "stdout_matches" in t and not re.search(t["stdout_matches"], r.stdout, re.M):
        e.append("no match")
    if "stdout_json" in t:
        try:
            if not sub(t["stdout_json"], json.loads(r.stdout)):
                e.append("json differs")
        except ValueError:
            e.append("bad json")
    return e


def report(name, errs, r):
    global fails
    if errs:
        fails += 1
        print("FAIL", name, errs, "\n  stdout:", r.stdout[:300], "\n  stderr:", r.stderr[:300])


def suite_rules():
    r = run("./kit check selftest")
    print("rules:", r.stdout.strip().splitlines()[-1])
    report("selftest", [] if r.returncode == 0 else ["exit %d" % r.returncode], r)


def suite_cli():
    spec = json.load(open(os.path.join(KIT, "spec/conformance.json")))
    for t in spec["tests"]:
        tmp = tempfile.mkdtemp()
        r = run(t["cmd"].replace("<temp folder>", tmp), temp_log=False)
        report(t["name"], check(t, r), r)
        shutil.rmtree(tmp, ignore_errors=True)
    print("cli: %d tests" % len(spec["tests"]))


def suite_worklog():
    tmp = tempfile.mkdtemp()
    env = {"KIT_WORKLOG_DIR": tmp}
    steps = [
        ("KIT_NOW='2026-01-05 09:30' ./kit log add client=\"Test & Co\" task=\"Café design\" minutes=90 files=\"a.pdf, b.pdf\"", "logged 2026-01-05-001 (work): Café design"),
        ("KIT_NOW='2026-01-05 10:00' ./kit log add kind=note notes=\"hello\"", "logged 2026-01-05-002 (note): hello"),
        ("KIT_NOW='2026-01-06 08:15' ./kit log add task=\"Next day\" billable=no", "logged 2026-01-06-001 (work): Next day"),
        ("./kit log verify", "OK: 3 entries, chain intact"),
    ]
    empty = subprocess.CompletedProcess("", 0, "", "")
    for cmd, want in steps:
        r = run(cmd, env)
        report("worklog " + cmd[:40], [] if want in r.stdout else ["want %r got %r" % (want, r.stdout)], r)
    first = json.load(open(os.path.join(tmp, "2026-01-05.json")))
    entries = first["entries"] if isinstance(first, dict) else first
    good = "6b27e45ef5f580147e6680165b48aaf19c18212535edd31d650976ccafb3f5bc"
    report("worklog first hash", [] if entries[0].get("hash") == good else ["hash " + str(entries[0].get("hash"))], empty)
    print("worklog: scenario done")
    shutil.rmtree(tmp, ignore_errors=True)


def suite_google():
    spec = json.load(open(os.path.join(KIT, "spec/google-conformance.json")))
    tmp = tempfile.mkdtemp()
    env_s = spec["env"].replace("<temp folder>", tmp)
    os.makedirs(os.path.join(KIT, "outputs"), exist_ok=True)
    open(os.path.join(KIT, "outputs/test-body.md"), "w").write("Hi Daan, two warmer options attached. Best, Sam")
    for t in spec["tests"]:
        r = run(t["cmd"].replace("<env>", env_s).replace("<temp folder>", tmp))
        report(t["name"], check(t, r), r)
    for f in ("outputs/test-body.md", "inbox/thread-t1.txt", "inbox/drive-Invoice-template-2026.txt"):
        try:
            os.remove(os.path.join(KIT, f))
        except OSError:
            pass
    shutil.rmtree(tmp, ignore_errors=True)
    print("google: %d tests" % len(spec["tests"]))


if __name__ == "__main__":
    for s in (suite_rules, suite_cli, suite_worklog, suite_google):
        s()
    print("TOTAL FAILURES:", fails)
    sys.exit(1 if fails else 0)
