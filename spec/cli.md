# The `kit` command

## Launcher files (the assistant writes these)

- `kit` (Mac, Linux): a short shell script. Runs the generated program in `core/` with the chosen runtime and passes all arguments, standard input and the exit code through. Mark it executable.
- `kit.cmd` (Windows): the same for cmd and PowerShell.

The launcher holds the exact runtime command and entry file directly (written by the assistant at build time). It does not need to read `setup/runtime.json`, which is there for humans and for `kit doctor`. It must not search the PATH for another runtime. If the runtime command contains spaces, quote it.

Users and the assistant always call `./kit <command> ...` (on Windows `kit <command> ...`).

## Subcommands

| Command | Does | Spec |
|---|---|---|
| `kit log add key=value ...` | add a work log entry | `worklog.md` |
| `kit log list [date=YYYY-MM-DD]` | show one day | `worklog.md` |
| `kit log verify` | check the hash chain | `worklog.md` |
| `kit report from= to= ...` | hours report | `worklog.md` |
| `kit check scan <file>` | find secrets, personal data, injection | `security.md` |
| `kit check command "<cmd>"` | decision for a shell command | `security.md` |
| `kit check read <path>` / `write <path>` | decision for a file access | `security.md` |
| `kit check tool <name>` | decision for a connector tool | `security.md` |
| `kit check selftest` | run `security/tests/*.json` | `security.md` |
| `kit check show` | print the rules in force | `security.md` |
| `kit check integrity` / `kit check seal` | verify or write the checksum seal | `security.md` |
| `kit hook` | Claude Code hook, reads JSON on stdin | `security.md` |
| `kit calc "<expression>"` | safe money math | `tools.md` |
| `kit pdf <html file> [pdf file]` | HTML to PDF with a local browser | `tools.md` |
| `kit doctor` | health check of the whole kit | `tools.md` |

No arguments, or `kit help`: print the list of commands as plain text (one per line, with a short description). The exact wording is free.

## Environment variables for tests only

- `KIT_WORKLOG_DIR`: use this folder instead of `ROOT/worklog`.
- `KIT_NOW`: `YYYY-MM-DD HH:MM`. Use this instead of the clock when adding an entry.

Security rules deny any shell command that mentions `KIT_`, so the assistant cannot use them. Do not document them for users.

## Exit codes

- `0`: success. For `kit check`: allow or ask.
- `1`: error or failed check.
- `2`: for `kit check`: deny, or a scan with a high severity finding. For `kit hook`: block the action.
