# Setup: build the kit's tools

You are the AI assistant. The kit has no pre-built scripts. Your job now is to build them from the specs, for the language this laptop has, and prove they work. Follow these steps in order. Talk to the user in plain English, short sentences. Do not skip the questions in steps 2 and 5.

Do this once. If `setup/runtime.json` exists and `./kit doctor` is all good, setup is done: tell the user and stop.

## 1. Read

Read all of `spec/`: `README.md`, `cli.md`, `worklog.md`, `security.md`, `tools.md`, `conformance.json`. Also read `security/rules.json` and `security/tests/base.json`. They define exactly what to build. Do not edit them.

## 2. Find a language

Run these checks (each may fail, that is fine):
```
node --version
python3 --version
python --version
py -3 --version
```
Needed: Node.js 18 or newer, or Python 3.8 or newer. Other languages with a plain scripting runtime (Deno, Bun, Ruby) also work if the user prefers.

- **Both found:** ask the user which one to use. Say what you found. If they have no preference, pick Python on Windows and whichever has the newer version elsewhere.
- **One found:** tell the user which and use it.
- **None found:** stop and ask. Offer: "Install Node.js (LTS) or Python 3 first." Give the exact command for their system and ask permission to run it:
  - macOS with Homebrew: `brew install node` or `brew install python`
  - Windows: `winget install OpenJS.NodeJS.LTS` or `winget install Python.Python.3.12`
  - Anything else: tell them to download from https://nodejs.org or https://www.python.org
  After the install, the terminal may need a restart. Ask the user to restart the tool and run `./start.sh` again (Windows: `start.cmd`).

## 3. Write the code

Create these files, following `spec/cli.md` and the other specs:
- `core/kit.<ext>`: the whole `kit` program. Use `.mjs` for Node so no package file is needed. `.py` for Python. You may split it into several files in `core/`.
- `kit` (Mac and Linux): a shell script that runs the program with the chosen runtime and passes through arguments, standard input and the exit code. Make it executable with `chmod +x kit`.
- `kit.cmd` (Windows): the same for cmd and PowerShell.
- `setup/runtime.json`: `{ "runtime": "<node|python|...>", "command": "<exact command to run it, for example python3>", "entry": "core/kit.py", "version": "<version>", "built": "<today's date>" }`.

Rules while writing:
- Standard library only. Do not install anything. No network calls.
- Short, clear, commented code. People will read it.
- Implement every command in `spec/cli.md`. Follow the specs exactly, including messages and exit codes.
- The work log hash chain must match the specs byte for byte. The sample files in `worklog/` show the right values.

## 4. Prove it works

1. Run `./kit check selftest`. Fix the code until it says `0 failed`.
2. Run every test in `spec/conformance.json`. Where it says `<temp folder>`, use a new empty temporary folder. Run the `worklog_scenario` steps too, with `KIT_WORKLOG_DIR` set to a fresh empty temporary folder.
3. After each failure: fix the **code**, never the specs, the rules or the tests. Repeat until everything passes. If you are stuck after 5 rounds, stop and tell the user what fails. A stronger AI model may be needed.
4. Run `./kit log verify` once more at the end. It must say `OK: 8 entries, chain intact`. (Do this before step 6.5. The setup note adds one entry, so afterwards it says 9.) Write any test runner you need **outside** the kit folder, for example in a temporary folder, and do not keep it. Do not leave any extra files from the tests behind (temp folders, changed worklog files).

Show the user a short result: how many tests passed.

## 5. Let the user review

The files that enforce security are `core/` (the `check` and `hook` parts), `kit`, `kit.cmd` and `security/rules.json`. Tell the user:
- what you built and where,
- that they should look at `core/` before relying on it (offer to walk through the security parts in plain English),
- ask: "Do you approve this code?"

Wait for a clear yes. If they ask for changes, make them, then repeat step 4.

## 6. Lock it in

1. **The user seals the core. You do not.** The security rules deny the assistant from running `seal`, on purpose: only the owner can say "this code is approved". Tell the user to run this in a normal terminal in the kit folder, then reply "sealed":
   ```
   ./kit check seal
   ```
   (Windows: `kit check seal`. In Claude Code the user can type `! ./kit check seal` in the prompt.) It prints `Sealed <n> files in setup/core.sha256.json`. Wait for their reply. Never try another way to create the seal file.
2. After they confirm, run `./kit check integrity`. It must say `OK`.
3. If the AI tool is **Claude Code**, write `.claude/settings.json` (create it, or merge into the existing one) so it contains:
   ```json
   {
     "permissions": {
       "deny": [
         "Read(./.env*)", "Read(./secrets/**)",
         "Edit(./AGENTS.md)", "Edit(./core/**)", "Edit(./kit)", "Edit(./kit.cmd)", "Edit(./spec/**)", "Edit(./setup/**)",
         "Edit(./security/**)", "Edit(./worklog/**)", "Edit(./.claude/**)",
         "Bash(curl:*)", "Bash(wget:*)", "Bash(sudo:*)", "Bash(git push:*)"
       ]
     },
     "hooks": {
       "PreToolUse": [
         { "matcher": "Bash|Read|Write|Edit|MultiEdit|NotebookEdit|mcp__.*",
           "hooks": [ { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR/kit\" hook" } ] }
       ]
     }
   }
   ```
   On Windows use `kit.cmd` instead of `kit` in the hook command. Do this **last**: the rules block you from editing these files afterwards.
4. Other tools (Codex, Gemini CLI, Antigravity): there is no hook. Tell the user that the security rules are advice for the assistant in this tool, and point them to `security/README.md` for the tool's own sandbox settings.
5. Run `./kit doctor`. It should say `All good.`
6. Log the setup: `./kit log add kind=note tool=<this AI tool> notes="Setup done with <runtime>"`

## 7. Finish

Tell the user:
- setup is done and which language was used,
- they must **close this AI tool and start it again** (`./start.sh`, Windows `start.cmd`) so the hook and rules take effect,
- then try: "What can you do in this folder?"

## Add Google (optional, only when the user asks)

Only after the base setup is finished and sealed. Read `spec/google.md` and `spec/google-conformance.json`, and `integrations/google-kit.md` for what the user does at Google.

1. Build the `kit google` commands into `core/` (a new file `core/google.<ext>` or inside the main file), in the same language as `setup/runtime.json`. Standard library only.
2. Run every test in `spec/google-conformance.json` (offline, with the fixtures, never the network). Fix the code until all pass. Re-run `./kit check selftest` and the base tests in `spec/conformance.json`: nothing may break.
3. Ask the user to review the new code. Pay special attention to: which hosts it talks to, where it stores the token, and that it has no send, delete or share command. Wait for a clear yes.
4. The user re-seals (the assistant cannot): tell them to run `./kit check seal`, then reply "sealed". Then run `./kit check integrity`.
5. Tell the user to continue with `integrations/google-kit.md` from the step "Create the Google project". Do not run `kit google auth` yourself: it is denied for you, on purpose.
6. Log: `./kit log add kind=note tool=<this AI tool> notes="Google tool added"`.

## To rebuild later (another language, or after a change to the specs)

The assistant cannot do this by itself, on purpose. The owner does it:
1. Delete `core/`, `kit`, `kit.cmd`, `setup/runtime.json`, `setup/core.sha256.json`.
2. Remove the `hooks` block and the `deny` list from `.claude/settings.json`.
3. Run `./start.sh` again.
