# Security engine

The rules are **data** in `security/rules.json`, the same for every language. This spec says how to read and apply them. Human version: `../security/policy.md`.

## Regular expressions

All patterns in the rules use a small common part of regex syntax: `\b \s \S \w \d`, `[...]`, `(...)`, `(?:...)`, `|`, `* + ? {n,m}`, `.`, `^ $`. Always match **case-insensitive**. "Matches" means the pattern is found anywhere in the text, unless the pattern has `^` or `$`. If your language needs the backslashes written differently, convert, do not change the pattern.

## Loading the rules

1. Read `security/rules.json`.
2. Read every `security/extensions/*.json` file in name order (ignore other file types). A file that is not valid JSON: add the warning `<file>: not valid JSON, ignored (<reason>)` and skip it. Otherwise remember its name as loaded.
3. Merge each key of an extension (ignore the key `description`):
   - `command_allow`, `write_allow`, `write_ask`: these would loosen the rules. Ignore them and add the warning `<file>: "<key>" would loosen the rules. Edit rules.json by hand for that. Ignored.`
   - List keys `read_deny`, `write_deny`, `command_deny`, `command_ask`, `mcp_tool_rules`, `blocked_mcp_servers`, `injection_patterns`, `confidential_terms`: append items that are not already in the list (compare the items as JSON).
   - `actions`: per entry, keep the stricter decision.
   - `scan_patterns`: add or replace entries by name.
   - `default_decision`: keep the stricter.
   - Any other key: add the warning `<file>: unknown key "<key>", ignored`.
4. Warnings are printed to stderr as `WARNING: <text>` by every `kit check` command.

## Paths

`locate(p)`:
- If `p` starts with `~/`, replace `~` with the user's home folder.
- `abs` = `p` resolved against ROOT, with symbolic links resolved. If the file does not exist yet, resolve its folder and add the file name.
- `rel` = `abs` relative to ROOT, with `/` as separator.
- `outside` = `rel` is exactly `..`, or starts with `../`, or is absolute (for example another drive on Windows). A file called `..notes` inside ROOT is not outside.
- All paths use `/` for matching.

Globs: `*` is any characters except `/`, `?` is one character except `/`, `**/` is any number of folders (including none), a trailing `/**` is the folder itself or anything below it, a lone `**` is anything. A glob must match the whole path, case-insensitive. A glob starting with `~/` is turned into the home folder path first.

`matches(globs, loc)`: the first glob that matches `loc.abs`, or (when not outside) `loc.rel`.

`checkPath(mode, p)`, where mode is `read` or `write`:
1. If `matches(read_deny)`: **deny**, reason `<rel> is a secret or private file (rule <glob>)`.
2. mode `read`: outside gives **ask** (`<p> is outside the kit folder`), otherwise **allow** (`inside kit folder`).
3. mode `write`:
   - outside: **deny** (`writing outside the kit folder is not allowed (<p>)`)
   - matches `write_deny`: **deny** (`<rel> is protected (rule <glob>). Only the owner edits it by hand`)
   - matches `write_ask`: **ask** (`changing <rel> needs the owner's ok (rule <glob>)`)
   - matches `write_allow`: **allow** (`<rel> is a normal output location`)
   - otherwise `default_decision` (`<rel> matches no rule`)

## Commands

`checkCommand(cmd)`, on the trimmed command text:
1. For each regex in `command_deny`: if found, **deny** (`command matches deny rule <regex>`).
2. Work out `chained`:
   - Take the text and replace every double quoted part and every single quoted part by `""`. If the result contains any of `; & |` or a newline: chained.
   - Take the text, remove single quoted parts. If it contains `$(` or a backtick: chained.
3. If not chained: for each regex in `command_allow`: if found, **allow** (`command matches allow rule <regex>`).
4. For each regex in `command_ask`: if found, **ask** (`command matches ask rule <regex>`).
5. Otherwise `default_decision`, reason `chained command, check each part` if chained, else `command matches no rule`.

## Connector tools

`checkTool(name)`:
- Name does not start with `mcp__`: **allow** (`not a connector tool`).
- Split on `__`: `mcp`, `<server>`, then the rest joined with `_` as `<tool>`, lowercased.
- If any entry of `blocked_mcp_servers` appears in the server name (case-insensitive substring): **deny** (`connector <server> is blocked`).
- Look at every rule in `mcp_tool_rules`. If its `match` pattern is found in `<tool>` (the lowercased tool part only, not the server name), it applies. The strictest applying decision wins. Reason: `connector tool "<tool>" matches rule "<match>"`.
- No rule applies: `default_decision` (`connector tool "<tool>" matches no rule`).

## The `actions` list

`actions` in `rules.json` (for example `send_email`) is a reference list for people and skills. No `kit` command enforces it by name: the enforcement is the command, path and connector tool rules. Still merge it from extensions as described above, so it stays correct for anyone who reads `kit check show`.

## Scan

`scan(text)` returns findings `{type, severity, line, snippet}`. For every line (line numbers start at 1):
1. Each entry in `scan_patterns` (`type` = its name, `severity` and `regex` from the rule): every match is a finding.
2. If `card_number_check` is true: find `\b(?:\d[ -]?){13,19}\b`. Take only the digits. If there are 13 to 19 digits and they pass the Luhn check: finding `card_number`, severity `high`.
3. Each regex in `injection_patterns`: if found in the line, finding `prompt_injection`, severity `high`, snippet = the line trimmed, at most 80 characters.
4. Each non-empty term in `confidential_terms`: if the line contains it (case-insensitive), finding `confidential_term`, severity `medium`, snippet = the term.

Snippets must be **masked** for every finding that comes from `scan_patterns` and for `card_number`. Injection snippets (the line text) and confidential terms are shown as they are. The mask is: if the text is 6 characters or fewer, `***`, otherwise first 4 characters + `***` + last 2. Never print a full secret.

## `kit check` subcommands

Output for `command`, `read`, `write`, `tool`: JSON with 2-space indent: `{ "decision": "...", "reason": "..." }`. The arguments after the subcommand are joined with a space. Exit 2 if deny, else 0.

`scan <file>`: a relative path is relative to the current folder. File missing: `Give a file that exists.` exit 1. Print `{ "file": <as given>, "clean": <bool>, "findings": [ ... ] }`. Exit 2 if any finding has severity `high`, else 0.

`selftest`: for every `security/tests/*.json` file in name order, for every case `{ "type", "input", "expect" }`:
- `command`, `read`, `write`, `tool`: the decision must equal `expect`.
- `scan`: `expect` is a finding type (the scan must produce that type) or `none` (no findings).
- On a failure print (to standard output) `FAIL <file>: <type> <input cut to 70 chars> expected <expect>, got <what you got>`.
- At the end print `<n> passed, <m> failed. Extensions loaded: <names or none>`. Exit 1 if any failed.

`show`: print JSON `{ "extensions_loaded": [...], "warnings": [...], "rules": <merged rules> }`.

`integrity` and `seal`: see below.

## Integrity seal

Purpose: the assistant must not quietly swap the code that enforces the rules.

- The core files are every regular file in `core/` (ignore any `__pycache__` folder, `*.pyc` files and `node_modules`), plus `kit`, `kit.cmd` and `security/rules.json`.
- `kit check seal` writes `setup/core.sha256.json` and prints `Sealed <n> files in setup/core.sha256.json`. Security rules deny the assistant from running `seal` once the hook is active: only the owner seals, in a normal terminal. The file is JSON with 2-space indentation and a trailing newline. It looks like this: `{ "<path relative to ROOT>": "<sha256 hex of the file bytes>", ... }` with paths sorted. Line endings: hash the bytes as stored.
- `kit check integrity`: compare. All equal: print `OK: seal matches <n> files`, exit 0. Missing seal file: print `No seal yet. Run: kit check seal`, exit 1. Any file changed, added or missing: print `CHANGED: <path>` per file, exit 1.

## `kit hook` (Claude Code PreToolUse hook)

Claude Code runs this before each Bash, file or connector call. It writes the event as JSON on stdin: `{ "tool_name": "...", "tool_input": { ... } }`.

1. Read stdin. Not valid JSON: exit 0.
2. Check the seal as `kit check integrity` does. If it fails, **block** everything: stderr `Security core was changed (<first changed path>). Review it, then run: kit check seal`, exit 2. (Blocking even the assistant is the point. The owner runs the seal command in a normal terminal.) If there is no seal file at all, skip this step.
3. Decide by tool:
   - `Bash`: `checkCommand(tool_input.command)`, target = the command
   - `Read`: `checkPath("read", tool_input.file_path)`. A file event with no path: treat as an error (step 4)
   - `Write`, `Edit`, `MultiEdit`, `NotebookEdit`: `checkPath("write", tool_input.file_path or notebook_path)`
   - name starts with `mcp__`: `checkTool(name)`, target = the name
   - any other tool: exit 0 and log nothing
4. If the rules cannot be loaded or any error happens: **fail closed**: stderr `Security hook error: <reason>`, exit 2.
5. Log it unless it is a `Read` with decision allow: add a work log entry with `kind` = `blocked` if deny, else `tool`; `tool=claude-code`; `task` = `<tool_name>: <target>`, where `<target>` has the text `<ROOT>/` removed from its front if it starts with it, and the whole task is cut to 200 characters; `outcome` = the decision; `notes` = the reason. A failure to log must not stop the hook.
6. Deny: stderr `Blocked by security rules: <reason>`, exit 2.
7. Ask: print on stdout `{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"<reason>"}}`, exit 0.
8. Allow: print nothing, exit 0.

## Other tools

Gemini CLI, Antigravity and Codex do not run this hook. The rules and `kit check` still work as a helper, and `AGENTS.md` asks the assistant to follow them.
