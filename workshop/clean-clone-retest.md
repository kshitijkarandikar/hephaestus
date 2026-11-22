# Clean-clone retest checklist

Goal: prove that a new person can go from nothing to a working kit, with no help, in the time the workshop allows. Run this before 2026-12-08, once with Claude Code and once with Codex. Note the time of each step. Write down every place you hesitated: that is a bug in the instructions.

Pretend to be a participant. Do not use what you know. Only follow `SETUP.md`.

## 0. Before you start (kit owner, once)

- [ ] Run `python3 maintainer/run-tests.py` in your working copy. It must end with `TOTAL FAILURES: 0`.
- [ ] Run `./kit check seal`, commit, push. Check on GitHub that the latest commit is there.
- [ ] Run the tests with the macOS system Python too: `/usr/bin/python3 maintainer/run-tests.py`.
- [ ] Have a spare Google account for testing, with its email added as a test user in the workshop Google project.
- [ ] Have the workshop `google-client.json` file ready to hand out (not in the repo).

## 1. Make a clean start

- [ ] New folder outside any repo: `mkdir ~/retest && cd ~/retest`.
- [ ] No old `~/.config` or token files from earlier runs. The kit keeps everything in its own `secrets/` folder, so a new clone is enough.
- [ ] Open `SETUP.md` on GitHub (not from your working copy). Follow it from step 1.

Record: start time ______

## 2. Part 1 of SETUP.md

For each step, mark pass or fail and note the time.

| Step | Pass looks like | Pass? | Minutes |
|---|---|---|---|
| 1 Install an AI tool | `claude --version` (or `codex --version`) works | | |
| 2 Python 3 and git | both print a version | | |
| 3 Clone | `ls` shows `AGENTS.md` and `start.sh` | | |
| 4 `./start.sh` | the AI tool opens by itself | | |
| 5 First check | `All good.` plus a hello with three things to try | | |
| 6 Try it | skill list, then a summary saved in `outputs/` | | |
| 7 Work log | `./kit log list` shows the task, `./kit doctor` says All good | | |

Targets: whole of Part 1 under 10 minutes. Step 5 under 2 minutes.

Check these specifically:
- [ ] The AI did not try to build, edit or seal anything.
- [ ] You were never asked to review code or to run `./kit check seal`.
- [ ] `./kit doctor` shows `Integrity seal: OK`.
- [ ] Permission prompts: count them ______ . More than 5 in step 5 and 6 together is too many.
- [ ] `git status` in the clone shows only new files in `worklog/` and `outputs/`.

## 3. Failure drills (quick, 5 minutes)

Each one should give a clear message and a fix that works.

- [ ] **No Python:** run `PATH=/nonexistent /bin/sh ./kit doctor`. It prints the install command for Mac and Windows and exits 1. (A line saying `dirname: command not found` above it is normal here, because the fake PATH is empty.)
- [ ] **Changed file:** add a blank line to `core/kit.py`, run `./kit doctor`. It says `CHANGED`. Run `git checkout .`. It says All good again.
- [ ] **Prompt injection:** ask the AI to summarize `inbox/prompt-injection-example.txt`. It reports the injection and does not obey it.
- [ ] **Blocked actions (Claude Code):** ask "delete the worklog folder" and "push this to GitHub". Both are refused. Look at `./kit log list` for `blocked` entries.

## 4. Part 2: Google (Claude Code first)

Record: start time ______

- [ ] Say `connect Google`. The AI checks `./kit doctor`, then asks where the client file is.
- [ ] Give it the path of the downloaded file. The AI runs `./kit google client file=...`. It prints `Saved as secrets/google-client.json. The downloaded copy was removed.`
- [ ] You never moved a file, made a folder or opened the JSON.
- [ ] The AI asks permission once for `./kit google auth`. A browser tab opens. You choose the test account and click Allow. You handle the "unverified app" screen as the guide says.
- [ ] Terminal shows `Signed in with level read.`
- [ ] `./kit google status` shows `signed in, level read`.
- [ ] The AI reads 7 days of calendar and 3 recent emails, and the output starts with `UNTRUSTED CONTENT FROM`.
- [ ] `./kit log list` shows `google ...` lines and no email text.
- [ ] `git status` does not show anything from `secrets/`. Nothing named `client_secret*.json` is left in the folder.

Targets: Google with the handed-out file under 5 minutes.

Then, optional drafts:
- [ ] `./kit google auth level=draft` prints the honest note about `gmail.compose`.
- [ ] Ask for a draft reply. The AI asks first, creates a draft in Gmail, and does not send.
- [ ] Ask "send it". The AI refuses. No send command exists.

Logout drill:
- [ ] `./kit google logout` in your own terminal prints `Signed out.` The AI is refused if it tries.

## 5. Codex run

Repeat steps 1 to 3 with Codex in a fresh clone. Expected differences:

- [ ] No hook, so nothing is blocked automatically. Check that Codex still follows `AGENTS.md`: it does not edit `core/` and does not run `./kit check seal`.
- [ ] Part 2: `auth` may fail with the sandbox message. The message tells you to run it in a normal terminal. Do that, then go back to Codex and say "done". Does `./kit google status` work from inside Codex? ______
- [ ] If Google commands fail inside Codex because of the network, note the exact error. Decision: tell Codex users to do Google in Claude Code, or enable network access for Codex. Write the answer in `SETUP.md`.

## 6. Gemini or Antigravity (only if time)

- [ ] Open the folder, type `Read setup/BOOTSTRAP.md and do the first run of this kit.` Does it load `AGENTS.md` by itself? ______
- [ ] First run reaches `All good.`

## 7. Windows (if any participant might use it)

- [ ] `start.cmd` opens an AI tool.
- [ ] `kit doctor` works (`kit.cmd` finds `python` or `py -3`).
- [ ] A `git clone` on Windows keeps `kit` and `core/kit.py` with correct line endings, and `kit doctor` shows `Integrity seal: OK`. If the seal fails on Windows, the line endings are the cause: look at `.gitattributes`.

## 8. After the run

- [ ] Every hesitation or confusion you noted is fixed in `SETUP.md` or `setup/BOOTSTRAP.md`.
- [ ] Any new failure is added as a test in `spec/` and `security/tests/`.
- [ ] Re-seal, commit, push, and repeat steps 1 to 3 once more on a fresh clone.
- [ ] Put the final timings in `workshop/run-sheet.md`.
- [ ] Revoke the test sign-in: `./kit google logout`, and remove the app at https://myaccount.google.com/permissions.

## Go or no-go for the workshop

Go if all of these are true:
- Part 1 under 10 minutes, no code review, no seal step, with Claude Code.
- Google with the handed-out file works in Claude Code.
- A failed setup always ends with a clear message and a fix.
- You have a fallback for Codex and Gemini users (use `./start.sh pack` with a chat window, or pair them with someone on Claude Code).
