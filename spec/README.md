# Specs: the kit's tools, described in plain steps

This folder describes every tool the kit needs. It contains **no code**. During setup, your AI assistant reads these specs, checks which language your laptop has (Node.js, Python or another), writes the tools in that language, and proves they work by passing the tests in `conformance.json` and `../security/tests/`.

Why this way: the kit works on any laptop and with any AI tool, nothing is pre-built for one language, and you see how an agent builds its own tools.

## Files

| File | Describes |
|---|---|
| `cli.md` | The one command, `kit`, and all its subcommands |
| `worklog.md` | Work log entries, the hash chain, `kit log` and `kit report` |
| `security.md` | Rule engine, `kit check`, the Claude Code hook, integrity seal |
| `tools.md` | `kit calc`, `kit pdf`, `kit doctor` |
| `conformance.json` | Commands with expected results. All must pass |

Setup instructions for the assistant: `../setup/BOOTSTRAP.md`.

## Rules for whoever writes the code (the assistant, or you)

1. Use the **standard library only**. No packages to install. No network access.
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
