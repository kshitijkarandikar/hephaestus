# Business Agent Kit for freelancers

An AI agent here is **a folder of plain text files**. No app, no server, no account with us. Any AI tool that can read files can run it. The example business is a fictional freelance designer, "Studio Sam". Replace it with your own.

**New here? Open `SETUP.md` and follow the steps one by one.**

The kit ships with its tools already built, tested and sealed (one small Python program in `core/`). Nobody has to write or review code. Your AI assistant only checks that the kit is healthy and then starts working. The only thing you install is Python 3, and the assistant tells you how if it is missing.

## Contents

1. [How it works](#how-it-works)
2. [What you need](#what-you-need)
3. [Start with one command](#start-with-one-command)
4. [What happens on first start](#what-happens-on-first-start)
5. [Folder map](#folder-map)
6. [Skills](#skills)
7. [The `kit` command](#the-kit-command)
8. [Work log](#work-log)
9. [Security](#security)
10. [Connect Google (optional)](#connect-google-optional)
11. [Using a chat window only](#using-a-chat-window-only)
12. [Use it for your own business](#use-it-for-your-own-business)
13. [Build and extend](#build-and-extend)
14. [Git](#git)
15. [Workshop files](#workshop-files)
16. [Troubleshooting](#troubleshooting)
17. [Known limits and what is untested](#known-limits-and-what-is-untested)

## How it works

| Part | Where | What it is |
|---|---|---|
| Instructions | `AGENTS.md` | Who the assistant is and its rules. `CLAUDE.md` and `GEMINI.md` just point to it |
| Context | `context/` | What it knows: business, clients, rates, invoices, brand voice |
| Skills | `skills/` | One recipe per repeated task, written in plain English |
| Tools | `core/` | The `kit` program: work log, security checks, calculator, PDF, Google. Built, tested, sealed |
| Specs | `spec/` | Plain-English description of the tools, and the tests they pass. For people who change the tools |
| First run | `setup/BOOTSTRAP.md` | Short checklist the assistant follows on the first start |
| Input | `inbox/` | Raw material: notes, email threads |
| Output | `outputs/` | Everything the assistant makes: drafts, invoices, PDFs |
| Work log | `worklog/` | One JSON file per day: what was done, when, for whom, how long |
| Security | `security/` | Rules for what the assistant may read, write, run and connect to |

Three words to remember:
- A **skill** is a recipe for one task.
- An **agent** is instructions + context + skills + freedom to choose which skill to use.
- A **spec** describes a tool in words, so an AI can build it in any language.

You can read and change every file. That is the whole trick.

## What you need

- An AI tool that works in a folder: **Claude Code** (tested path), ChatGPT Codex, Gemini CLI or Antigravity. A chat window also works in a reduced way (see below).
- **Python 3.9 or newer.** Macs get it with a one-time `xcode-select --install`. You do not need to install it first: if it is missing, the assistant tells you the exact command.
- **Chrome, Edge or Brave** for PDF output.
- A terminal. Mac and Linux are the main path. Windows has a `start.cmd` that is untested.

No API keys are stored in this folder. Never put any here.

## Start with one command

```
git clone <repo-url> business-agent-kit
cd business-agent-kit
./start.sh          # Mac and Linux
start.cmd           # Windows
```

`start.sh` is a short shell script. It finds your AI tool (Claude Code, Codex or Gemini CLI), starts it in this folder, and, on the first run, tells it to do a quick health check. No tool installed? It prints the install links.

`start.sh` is for **you**, in a normal terminal. Do not ask an AI to run it: it would try to start a second AI tool inside the first one and fail (the sandbox blocks it).

Variants:
- `./start.sh claude` starts a specific tool (`codex`, `gemini` also work). Windows: `start.cmd claude`.
- `./start.sh pack` builds `outputs/pack.md` for a chat window. No AI tool needed.
- Antigravity or another desktop app: open the folder as a project, then type: `Read setup/BOOTSTRAP.md and do the first run of this kit.`

## What happens on first start

The assistant follows `setup/BOOTSTRAP.md`:

1. **Checks** the kit with `./kit doctor`: Python is there, the security rules pass their 74 tests, the work log chain is intact, and no protected file was changed.
2. **Fixes what it can.** No Python: it gives you the install command for your system. A changed protected file: it tells you to run `git checkout .`.
3. **Says hello** and logs the first run.

It takes about a minute. Nothing is built, and you review no code. For Claude Code the security hook and deny list are already in `.claude/settings.json`, so they are active from the first start.

Then ask: **"What can you do in this folder?"** and try:
- "Summarize `inbox/meeting-notes-noord-studio.txt`."
- "Draft a reply to the latest message in `inbox/email-thread-bloem.txt`."
- "Plan the next steps from `inbox/meeting-notes-noord-studio.txt`. Today is 2026-12-08."

Check the results in `outputs/` and the log with `./kit log list`.

## Folder map

```
SETUP.md               start here: step-by-step setup for participants
start.sh, start.cmd    one-command launcher (a short shell script)
AGENTS.md              rules for the assistant (read first, every session)
CLAUDE.md, GEMINI.md   one line each: point to AGENTS.md
.claude/settings.json  Claude Code: deny list, and (after setup) the security hook

context/               your business facts, clients, rates, invoices, brand voice
  templates/invoice.html   layout reference for invoices
inbox/                 sample input: meeting notes, an email thread, job notes, an injection test
outputs/               results go here (not tracked by git)

skills/                ready-made skills, one folder each
solutions/             finished versions of the two skills built live
integrations/          Google guide (google-kit.md), other tool options, chat-only route

spec/                  the tools, described in plain steps (no code)
  README.md, cli.md, worklog.md, security.md, tools.md, google.md
  conformance.json     commands with expected results: the tests for the built tools
  google-conformance.json, google-fixtures/   offline tests for the Google tool
setup/
  BOOTSTRAP.md         what the assistant does on first start
  core.sha256.json     checksum seal of the core files (made by the kit owner)

core/                  the program: kit.py (everything) and google.py (Google tool)
kit, kit.cmd           the launchers (they run core/kit.py with Python 3)
maintainer/            run-tests.py: runs all test suites (for the kit owner)

worklog/               one JSON file per day (sample entries included)
security/
  policy.md            plain rules, threats, limits
  rules.json           core rules in machine form
  extensions/          your own extra rules (can only tighten)
  tests/               test cases for the rules
  README.md            how to extend the framework

workshop/
  run-sheet.md         minute-by-minute plan for the 60 minute session
  menu-of-skills.md    skill ideas for the hands-on part
  test-worklog-and-security.md   step-by-step test guide
```

## Skills

A skill is `skills/<name>/SKILL.md`: a name, a one-line description (this decides when it gets used), and numbered steps. You just ask for the task in normal words. The assistant picks the skill.

| Skill | Does | Needs |
|---|---|---|
| `summarize-thread` | Email thread, meeting notes or transcript into decisions, promises and open questions | nothing |
| `draft-reply` | Email draft in your voice. Never sends | nothing. Can save a Gmail draft if Gmail is connected |
| `next-steps` | Action list with owners and dates that fit your working days | nothing. Can propose calendar events if Calendar is connected |
| `html-to-pdf` | HTML file into PDF | the built `kit` and Chrome, Edge or Brave |
| `skill-builder` | **Interviews you, writes a new skill, tests it, fixes it once** | nothing |

Built live in the workshop (finished versions in `solutions/`, copy them into `skills/` to use them):

| Skill | Does |
|---|---|
| `invoice-from-notes` | Messy work notes into an invoice (HTML and PDF). Shows lines and totals, waits for your "ok", then logs the invoice |
| `payment-chaser` | Finds overdue invoices, picks the right reminder level from your policy, drafts one email each |

Every skill ends with a **Log** step that writes to the work log.

## The `kit` command

All tools are one command, `./kit` (Windows: `kit`). Created during setup. Full definition in `spec/cli.md`.

| Command | Does |
|---|---|
| `./kit log add\|list\|verify` | work log |
| `./kit report from=... to=...` | hours report |
| `./kit check scan\|command\|read\|write\|tool\|selftest\|show\|integrity\|seal` | security checks |
| `./kit hook` | the Claude Code security hook (not called by hand) |
| `./kit calc "(4+5+3)*95"` | safe money math, 2 decimals, rounds half up |
| `./kit pdf outputs/invoice.html` | HTML to PDF with a local browser |
| `./kit doctor` | health check of the whole kit |
| `./kit google ...` | optional: Gmail, Calendar, Drive (`spec/google.md`) |

## Work log

`worklog/YYYY-MM-DD.json` holds one file per day. It is both a record of your work (for hours and invoices) and an audit trail of what the assistant did. Full definition in `spec/worklog.md`.

### Entry fields

| Field | Meaning |
|---|---|
| `id`, `time` | `2026-12-08-003`, local time `14:05`. Set by the tool |
| `kind` | `work` (counts for hours), `approval`, `blocked`, `tool`, `note` |
| `client`, `task`, `skill` | what was done, for whom, with which skill |
| `tool` | which AI tool did it, for example `claude-code` |
| `minutes` | **your** time in minutes. Only you know it. The assistant must ask and never invent it |
| `billable` | defaults to true for `work` |
| `files` | files made, for example `outputs/invoice-2026-014-acme-bikes.pdf` |
| `outcome` | `done`, `draft`, `waiting`, or for tool entries `allow`, `ask`, `deny` |
| `notes`, `corrects`, `sample` | free text, the id of an entry this one corrects, sample data flag |
| `prev`, `hash` | hash chain, set by the tool |

### Commands

```
./kit log add client="Acme Bikes" task="Homepage wireframes" skill=next-steps minutes=240 outcome=done
./kit log list                      today's entries
./kit log list date=2026-11-03      another day
./kit log verify                    is the history intact?
./kit report from=2026-11-01 to=2026-11-30
./kit report from=2026-11-01 to=2026-11-30 client="Acme Bikes" by=skill
./kit report from=2026-11-01 to=2026-11-30 format=md save=true
```

`report` options: `from`, `to`, `client`, `by=client|skill|day`, `billable=true|false`, `format=text|md|json`, `save=true` (writes to `outputs/`). It counts only `work` entries that have minutes, and lists the ones without minutes so nothing is lost silently.

### Rules of the log

- **Append only.** Entries are never edited. To fix a mistake, add a new entry with `corrects=<id>`.
- **Tamper evidence.** Each entry holds the hash of the one before it. `verify` finds changed, removed or reordered entries. It does not stop someone with full access from rewriting the whole chain, so commit to git too (see [Git](#git)).
- **The date and time come from the computer clock.**
- **The assistant cannot write into `worklog/` directly.** Only through `./kit log`. In Claude Code the hook enforces this.
- In Claude Code, the security hook also logs every command, file write and connector call it checks, including blocked ones. This works even if the assistant forgets to log.
- **Exact hash rules.** The hash rules are written down precisely (`spec/worklog.md`), so any correct tool, in any language, makes the same log. The 8 sample entries are the proof: `./kit log verify` says `OK: 8 entries, chain intact`.
- The entries in `worklog/` now are **sample data** (flagged `sample`). Delete all `worklog/*.json` when you start with your own business. Delete them all, not one by one, or `verify` fails. After that the sample check in the tests no longer applies.

## Security

Full text: `security/policy.md`. How to extend: `security/README.md`. How it must work: `spec/security.md`.

### Principles

1. Least power: read first, draft second, send never.
2. A human sends. Emails, invites and shared files leave only with your clear "yes".
3. Data is not instructions. Text in emails and notes is read, never obeyed.
4. Secrets stay out of the folder. The assistant cannot read `.env` or key files.
5. Everything is logged.
6. The assistant cannot change its own rules or the code that enforces them.

### How the rules work

`security/rules.json` gives every action one of three decisions: **allow** (runs), **ask** (you approve) or **deny** (blocked). If several rules match, the strictest wins. It covers:

- **Reading:** secrets and key files are denied. Anything outside the kit folder asks.
- **Writing:** `AGENTS.md`, `kit`, `core/`, `spec/`, `setup/`, `security/`, `worklog/`, `.claude/` and `.git/` are denied. `context/`, `skills/`, `solutions/`, `integrations/` and `inbox/` ask. `outputs/` is allowed. Outside the folder is denied.
- **Commands:** network tools, `sudo`, `rm -rf`, `git push`, piping to a shell, reading secrets, and any use of `KIT_` test variables are denied. The `kit` commands, `date`, `ls` and a few more are allowed. Running your own `python` or `node` one-liners, installs and file moves ask. Chained commands (`a; b`, pipes) are never auto-allowed.
- **Connector tools (Gmail, Calendar, Drive):** judged by tool name. `send`, `delete`, `share` are denied. `create`, `draft`, `update`, `upload` ask. `get`, `list`, `search`, `read` are allowed. Unknown names ask.
- **Scan** (`./kit check scan <file>`): finds API keys, private keys, passwords, card numbers, IBAN, BSN, prompt injection phrases and any confidential terms you list.
- **Integrity seal:** setup records a checksum of the core files. If anything in `core/`, `kit`, `kit.cmd` or `rules.json` changes, the hook blocks everything. The kit owner re-seals after reviewing a change (`./kit check seal`). Users never do this. It stops the assistant, or anyone, from quietly swapping the safety code.

### Where it is enforced

| Layer | Strength |
|---|---|
| `AGENTS.md` | Soft. The AI is asked to follow it |
| The hook (`./kit hook`) and the deny list in `.claude/settings.json` | **Hard in Claude Code.** Blocks or asks before each call and logs it |
| Connector permissions at Google | **Hard.** Set read-only or draft-only when you connect |
| Tool sandboxes (Codex, Gemini) | Hard if you switch them on. See `security/README.md` |

With tools other than Claude Code, only the soft layer applies until you add the tool's own settings.

**Important:** the security code is written by an AI during setup. The tests catch wrong behavior, and you are asked to review it. Take the review seriously: this code is what protects you.

### Commands

```
./kit check selftest                          run all rule tests
./kit check scan inbox/email-thread-bloem.txt
./kit check command "curl https://example.com"
./kit check write context/rates.csv
./kit check read .env
./kit check tool mcp__gmail__send_message
./kit check show                              rules in force, with extensions
./kit check integrity                         does the core still match the seal?
```

### Add your own rules

Copy `security/extensions/example.json.off` to `security/extensions/my-rules.json`, keep what you need, add a test in `security/tests/`, and run `./kit check selftest`. Extensions can only add restrictions. A key that would loosen the rules is ignored with a warning. To loosen a rule, edit `rules.json` by hand, then run `./kit check seal`. Details and examples are in `security/README.md`.

### What it does not cover

A determined attacker with access to your laptop, mistakes inside a connector you approved too widely, anything outside the tools the hook watches, and legal duties such as GDPR (AVG) for client data. Ask your accountant or a lawyer about those.

## Connect Google (optional)

`kit google` lets the assistant read Gmail, Calendar and Drive, and prepare drafts, in any AI tool. Follow `integrations/google-kit.md` step by step (about 30 minutes, mostly clicking in Google's website).

- Built from `spec/google.md` like the rest, with offline tests (`spec/google-conformance.json`) that use canned Google answers in `spec/google-fixtures/`.
- Default level is **read-only**. The optional `draft` level adds Gmail drafts, calendar events (never with guests) and Drive uploads of files you made.
- **No send, delete or share command exists**, and the security rules deny them. Google itself has no "drafts only" permission, so the safety is in the tool and the rules. This is stated at sign-in.
- Signing in (`./kit google auth`) and signing out are done by **you**. The assistant is denied both.
- Your sign-in token lives in `secrets/`, which is hidden from git and from the assistant. Everything fetched is marked `UNTRUSTED CONTENT`, saved in `inbox/` and scanned. The work log records only counts, never email text.
- It talks only to Google's own hosts. This is the one place the kit uses the network.
- Practise with a test Google account. In Google's test mode, sign-in lasts 7 days.
- It uses Google's plain REST APIs with OAuth, not MCP connectors.

| Command | Does |
|---|---|
| `./kit google status` | signed in? which level |
| `./kit google gmail search q="..."` | find threads |
| `./kit google gmail thread id=... save=true` | read a thread, save it to `inbox/` |
| `./kit google gmail draft to= subject= body_file=` | create a draft (level draft, asks you) |
| `./kit google calendar list from= to=` | events |
| `./kit google calendar freebusy from= to=` | free time |
| `./kit google calendar create title= start= end=` | event, no guests (level draft, asks you) |
| `./kit google drive search q="..."` and `drive get id=...` | find and read files |
| `./kit google drive upload file=outputs/...` | upload a file you made (level draft, asks you) |

## Using a chat window only

A chat window cannot read your folder, build tools, run commands or write files. You copy and paste, and you lose the work log, calculator and PDF tool.

1. `./start.sh pack` builds `outputs/pack.md` with the rules, security policy, context and all skills. No AI tool or language needed. Windows: `start.cmd pack`.
2. Upload it to a Project, Gem or similar, or paste it as the first message.
3. Paste each task's input. Copy results into `outputs/` by hand.
4. For a PDF: save the HTML, open it in Chrome, Print, Save as PDF.
5. Check the math with a calculator.

Details: `integrations/chat-only.md`.

## Use it for your own business

1. Do the setup once (`SETUP.md`).
2. Replace `context/business.md` (name, address, VAT, payment term, working days, late payment policy).
3. Replace `context/clients.csv`, `rates.csv`, `invoices-log.csv`, `brand-voice.md`. Start with fake client data while you practise.
4. Change the name "Studio Sam" in `AGENTS.md` if you like. That file is protected from the assistant, so edit it by hand.
5. Delete the sample files in `inbox/` and the sample entries in `worklog/*.json`.
6. Copy the skills you want from `solutions/` into `skills/`.

Money and tax: the assistant drafts and calculates with the calculator. Your accountant checks. Real client data goes to your AI provider, so read their privacy terms first.

## Build and extend

**Make a new skill:** say "make a skill" and answer up to 5 questions. `skill-builder` writes it into `skills/`, tests it and fixes it once. Rule of thumb: if you did a task twice, make it a skill. Ideas are in `workshop/menu-of-skills.md`.

**Change or add a tool (for the kit owner):** edit `core/kit.py`, update the spec in `spec/` and its tests, run `python3 maintainer/run-tests.py` until it says `TOTAL FAILURES: 0`, review the change yourself, then run `./kit check seal` in a normal terminal and commit. Do not ask the assistant to change `core/`: it is not allowed to.

**Level up later:**
- Memory: tell the assistant to read the last few days of `worklog/` at the start.
- Hours into invoices: ask `skill-builder` for an "invoice from hours" skill that uses `./kit report`.
- A review skill that checks the output of another skill.
- Search over many documents (RAG): under about 100 documents, a folder plus an index file (`context/index.md`, one line per document) is enough. Build real RAG only when it outgrows that.
- Connect Google, then schedule a weekly "Friday admin" run.
- Weekly security review skill: read the `blocked` entries in `worklog/` and summarize them.

## Git

This folder is a git repo (branch `main`). Commit when you want a snapshot. The commit history is a second audit trail and backs up the work log's hash chain. `outputs/`, `.env*`, keys and `secrets/` are ignored. The work log, the security rules and `core/` are tracked, so a change to the code shows up in `git diff`. The log holds client names, so keep the repo private. Do not push it anywhere you would not show a client list. The assistant is not allowed to push, and asks before it commits.

## Workshop files

| File | Use |
|---|---|
| `workshop/run-sheet.md` | 60 minute plan: 10 min demo, about 30 min hands-on, buffer, questions. Pre-workshop checklist |
| `workshop/menu-of-skills.md` | Skill ideas for the hands-on part |
| `workshop/test-worklog-and-security.md` | Tests for the work log and security |
| `solutions/` | The two skills built live, as a fallback |

## Troubleshooting

| Problem | Try |
|---|---|
| The tool ignores the folder rules | Say "Read AGENTS.md first". Note which tool did not load it |
| Asked the AI to "run the start script" and it failed (daemon folder, sandbox) | Run `./start.sh` yourself in a normal terminal. Or, inside an AI session, paste: `Read setup/BOOTSTRAP.md and do the first run of this kit.` |
| `./start.sh`: permission denied | Run `chmod +x start.sh`, or `bash start.sh` |
| Sandboxed tool (Codex): Google commands fail (`PermissionError`, sandbox, `Could not reach Google`) | Codex runs commands in a sandbox with no internet. It should ask you to approve each `./kit google` command: click Approve. If it does not ask, tell it: "run this outside the sandbox and ask me for approval". Fallback: run `./kit google auth` in a normal terminal |
| `./kit doctor` shows `FAIL` | Read the line. Send it to the person running the workshop |
| Python 3 not found | Mac: `xcode-select --install`. Windows: `winget install Python.Python.3.12`. Or download from python.org. Restart the terminal |
| `./kit: command not found` | You are not in the kit folder. Type `cd business-agent-kit` |
| PDF says no browser found | Install Chrome or Edge, or open the HTML file and use Print, Save as PDF |
| A command or file write is blocked | Read the reason. Run `./kit check command "<cmd>"` to see which rule. Rephrase the task. Edit `rules.json` by hand only if you understand the risk |
| A worklog entry was blocked because the text contains a word like "curl" | Rephrase the task text. The rules read the whole command line |
| `./kit log verify` says BROKEN | Someone changed history. Look at `git diff worklog`, restore with `git checkout worklog` |
| The hook blocks everything and says "Security files were changed" | Something in `core/`, `kit`, `kit.cmd` or `rules.json` differs from the seal. Type `git checkout .` to restore the originals. Kit owners: review `git diff`, then re-seal |
| Hook does not run on Windows | In `.claude/settings.json` change the hook command to `kit.cmd hook` |

## Known limits and what is untested

- **Tested:** all four test suites pass (74 security rules, 23 command tests, the work log chain, 22 offline Google tests) on Python 3.15 and on the macOS system Python 3.9. Google is tested offline against canned answers only.
- **Not tested yet:** a real Google sign-in and token refresh, the hook inside a live Claude Code session, Codex and Gemini end to end, `start.cmd` and `kit.cmd` on Windows, and PDF output on every OS.
- **Hard limits only in Claude Code.** There the hook blocks and logs. In Codex, Gemini CLI and Antigravity the rules are a request the assistant follows, not a lock. The real protection there is the tool itself: `kit google` has no send, delete or share command and talks to four Google hosts only.
- **Google test mode.** The sign-in lasts 7 days and Google shows an "unverified app" notice. Fine for a workshop. For daily use, make your own Google project.
- The hours in the report are only as good as the minutes you give.
- The security rules are a safety net, not a guarantee.
- Everything here is a starting point. Read the files, change them, make them yours.
