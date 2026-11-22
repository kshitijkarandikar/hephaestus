# Security framework

| File | Purpose |
|---|---|
| `policy.md` | Human rules. Read this first |
| `rules.json` | Core rules in machine form: paths, commands, connector tools, scan patterns |
| `extensions/*.json` | Your own extra rules. Can only **add** restrictions |
| `../spec/security.md` | How the rule engine, `./kit check` and the hook must work. Your AI builds the code from it during setup |
| `tests/*.json` | Test cases. `selftest` runs all of them |

## Try it

```
./kit check selftest
./kit check command "curl https://example.com"
./kit check write context/rates.csv
./kit check tool mcp__gmail__send_message
./kit check scan inbox/email-thread-bloem.txt
./kit check show
```

## Decisions

- `deny`: blocked. The assistant gets an error message.
- `ask`: you are asked to approve.
- `allow`: runs.
- Several rules match: the strictest wins. Order for commands: deny, allow, ask, default (`ask`).
- A chained command (`a; b`, `a && b`, pipes) is never auto-allowed. Each part must be safe.

## Add your own rule (5 minutes)

1. Copy `extensions/example.json.off` to `extensions/my-rules.json`.
2. Keep only what you need. Examples:
   - Block the Drive connector: `"blocked_mcp_servers": ["drive"]`
   - Protect a client file: `"write_deny": ["context/clients.csv"]`
   - Flag a confidential project name in drafts: `"confidential_terms": ["Project Falcon"]`
   - Never create calendar events: `"actions": { "create_calendar_event": "deny" }`
3. Add a test in `tests/my-rules.json`:
   ```json
   { "cases": [ { "type": "tool", "input": "mcp__drive__get_file", "expect": "deny" } ] }
   ```
   Types: `command`, `read`, `write`, `tool`, `scan`. For `scan`, expect a finding type like `api_key`, or `none`.
4. Run `./kit check selftest`. All must pass.
5. Ask the assistant to build one for you: "Use skill-builder. I want a rule that ...". It may write to `security/extensions/` only if you approve and you removed that folder from `write_deny` yourself. Easier: ask it to show you the JSON, then you save it.

Warnings from bad extensions print when you run any `./kit check` command.

## Other AI tools

The hook only works in Claude Code. For others:

- **Codex:** run it with its sandbox and approval settings on (for example workspace-write sandbox, approval on request). Check its docs for the exact flags. Not tested here.
- **Gemini CLI, Antigravity:** switch on sandbox or approval mode if offered. Newer versions may support hooks. If yours does, point a before-tool hook at `./kit hook`. The input format may differ from Claude Code, so test with `echo ... | ./kit hook` first. Not tested here.
- **Chat-only:** nothing runs on your laptop. Safety is what you paste in. Do not paste secrets.
- **Everywhere:** `AGENTS.md` still asks the assistant to follow the rules. That is a request, not a lock.

## Windows

The hook command in `.claude/settings.json` uses `$CLAUDE_PROJECT_DIR`. This is untested on Windows. If it fails, change the hook command to `kit.cmd hook`.

## Ideas to extend

- Scan every new file in `outputs/` before it can be attached to a draft.
- Block drafts that contain a confidential term.
- Daily check: `./kit log verify` and `./kit check selftest` in one command.
- Per-client rules: some clients forbid AI use. Add their name to `confidential_terms` and block their folder.
- Weekly review skill: read the `blocked` entries in `worklog/` and summarize what the assistant tried.
