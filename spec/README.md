# Specs: the kit's tools, described in plain steps

This folder describes every tool the kit has, in plain steps, with the tests they must pass. The shipped program is `../core/kit.py` (Python 3, standard library only). These specs are the source of truth: they say what the code must do, and the tests in `conformance.json`, `google-conformance.json` and `../security/tests/` prove it. Run them all with `python3 ../maintainer/run-tests.py`.

Why keep specs: you can rewrite the tools in another language (an AI can do it from these specs and the tests), and anyone can read what the tools promise without reading code.

## Files

| File | Describes |
|---|---|
| `cli.md` | The one command, `kit`, and all its subcommands |
| `worklog.md` | Work log entries, the hash chain, `kit log` and `kit report` |
| `security.md` | Rule engine, `kit check`, the Claude Code hook, integrity seal |
| `tools.md` | `kit calc`, `kit pdf`, `kit doctor` |
| `google.md` | `kit google` for Gmail, Calendar and Drive (optional, built on request) |
| `conformance.json` | Commands with expected results. All must pass |
| `google-conformance.json`, `google-fixtures/` | Offline tests for `kit google`, with canned Google answers |

First run checklist for the assistant: `../setup/BOOTSTRAP.md`.

## Rules for whoever writes the code (the assistant, or you)

1. Use the **standard library only**. No packages to install. No network access, with one exception: `kit google` may talk to the Google hosts listed in `google.md`, and only when the user asked for the Google tool.
2. One entry file `core/kit.<ext>` is enough. You may split into modules in `core/`. Keep the code readable and commented: people will read it.
3. Do not change anything in `spec/`, `security/rules.json`, `security/tests/` or `worklog/` to make a test pass. Fix the code instead.
4. Do not hide behavior that is not in the specs. If the specs are unclear, ask the user.
5. Same inputs must give the same outputs in every language. In particular, the work log hash chain must come out byte for byte the same (see `worklog.md`). The sample files in `worklog/` are the proof.
6. Errors: print a short plain message to stderr and exit with a non-zero code. Never print a stack trace for a user mistake.
7. Arguments are `key=value` words, not `-flags`, so the commands look the same everywhere. A value with spaces is quoted by the shell: `task="Homepage wireframes"`.

## Words used in the specs

- **must**: required. **may**: optional.
- `ROOT`: the kit folder (the folder that holds `AGENTS.md`).
- **Decision**: one of `allow`, `ask`, `deny`. Order of strictness: allow, then ask, then deny. When several rules match, the strictest wins.
- **Local time**: the laptop clock in its own time zone.
