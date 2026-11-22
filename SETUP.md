# Setup: start here

Read the steps one by one and do each one. Each step says what you should see. If you do not see it, go to "If something goes wrong" at the bottom.

**Part 1** gets the kit running. It takes about 10 minutes. **Part 2** connects Google (Gmail, Calendar, Drive). It is optional. You make your own Google project, which takes about 20 to 30 minutes once, mostly clicking in Google's website. Do Part 1 and, if you want Google, Part 2 before the workshop. At the workshop, only the sign-in and the tests are left (about 10 minutes). Skipping Google is fine: the workshop has a path that needs none.

Use **fake client data** while you practise. Everything you type goes to your AI provider.

---

## Part 1: Get the kit running

### Step 1. Install an AI tool that works in a folder

You need one of these. Pick the one you already have an account for:

- **Claude Code** (best tested): https://docs.claude.com/en/docs/claude-code/setup
- **ChatGPT Codex**: https://github.com/openai/codex
- **Gemini CLI**: https://github.com/google-gemini/gemini-cli

You should see: the install page finishes without errors. Check it later in step 5.

### Step 2. Install Python 3 and git

Open a terminal (Mac: the app "Terminal". Windows: "Windows Terminal" or "Command Prompt"). Type:

```
python3 --version
git --version
```

(On Windows, type `python --version` for the first line.)

You should see two version numbers. If one says "command not found":

- **Python, Mac:** type `xcode-select --install`. A window opens. Click Install and wait. This also installs git.
- **Python, Windows:** type `winget install Python.Python.3.12`, then close the terminal and open a new one.
- **git, Windows:** download it from https://git-scm.com/downloads, then open a new terminal.

### Step 3. Download the kit

In the terminal, type these two lines:

```
git clone https://github.com/kshitijkarandikar/hephaestus.git
cd hephaestus
```

You should see: a new folder `hephaestus`, and your terminal is now inside it. Type `ls` (Mac) or `dir` (Windows) to see files like `AGENTS.md` and `start.sh`.

### Step 4. Start the kit

Mac and Linux:

```
./start.sh
```

Windows:

```
start.cmd
```

Do this yourself in the terminal. Do not ask the AI to run it.

You should see: `Starting Claude Code in this folder.` (or Codex, or Gemini). Then the AI tool opens and starts working on its own. If it says "No AI tool found", go back to step 1.

On a Mac you may see `permission denied`. Type `chmod +x start.sh` and try again.

### Step 5. Let it check the kit

The AI runs a health check. This takes about a minute. The kit is already built and tested, so the AI builds nothing and you review nothing.

It may ask permission to run commands. Say yes to the ones that start with `./kit`. They only touch this folder.

You should see: `All good.` and a short hello with three things to try.

### Step 6. Try it

Type these one at a time:

```
What can you do in this folder?
```

You should see a list of skills: summarize, draft a reply, next steps, PDF, skill builder.

```
Summarize inbox/meeting-notes-noord-studio.txt
```

You should see: a summary with decisions, promises and open questions. It saves a file in `outputs/` and asks how many minutes it took you. Answer with a number, or say you do not know.

### Step 7. Check your work log

Open a second terminal in the kit folder and type:

```
./kit log list
```

You should see: a line for the task you just did. Also try `./kit doctor`. You should see `All good.`

**Part 1 is done.**

---

## Part 2: Connect Google (optional)

This lets the AI read your Gmail, Calendar and Drive, and prepare drafts. It never sends, deletes or shares anything.

1. **Make your Google project and download the client file.** Follow `integrations/google-kit.md`, Part B, steps 1 to 4. The AI can read the steps out one at a time. Use a test Google account if you can. At the end you have a `.json` file in your Downloads folder. Part 1 must be done first: `./kit doctor` says `All good.`
2. In the AI, type: **connect Google**. (Codex: it will ask you to approve each Google command, because Google needs the internet. Click Approve each time.) and tell it where the file is. The AI runs one command that saves the file safely. You never move files or make folders.
3. The AI runs the sign-in. A browser tab opens. Choose your Google account and click **Allow**. If Google says "hasn't verified this app", click **Advanced**, then **Go to ... (unsafe)**. That warning is normal for a test app.
4. The AI tests it by reading your next 7 days of calendar and 3 recent emails.

The AI checks in this order: sign-in succeeds, then `./kit google status` says `signed in, level read`, then it reads your calendar and emails. You should see a short list of both. If status still says "not signed in", see the table below. In test mode, Google signs you out after 7 days. Run step 2 again then.

---

## Part 3: Make it yours

1. Open `context/business.md` and replace the example business with yours.
2. Replace `context/clients.csv` and `context/rates.csv`.
3. Delete the sample entries in `worklog/` (all the `.json` files in that folder).
4. Ask the AI: `Make a skill for something I do every week.` It will interview you and write the skill.

---

## If something goes wrong

| What you see | What to do |
|---|---|
| `No AI tool found` | Install one (step 1), close the terminal, open a new one |
| `permission denied` on `./start.sh` | Type `chmod +x start.sh`, or `bash start.sh` |
| The AI says it cannot start itself or a daemon folder fails | You asked the AI to run `start.sh`. Run it yourself in a terminal |
| `Python 3 is not installed` | Do step 2, then open a new terminal and start again |
| The AI says a kit file was changed ("CHANGED") | Type `git checkout .` in the kit folder, then start again |
| `./kit: command not found` | You are not in the kit folder. Type `cd hephaestus` |
| Google sign-in says the file is missing | Tell the AI where the downloaded file is. It runs `./kit google client file=...` |
| `Error: PermissionError`, a sandbox message, or `Could not reach Google` | Codex or another sandboxed tool: click **Approve** when it asks to run a Google command outside the sandbox. It asks every time. If you cannot approve, open a normal terminal in the kit folder and run `./kit google auth` there (Claude Code: type `! ./kit google auth`). Then go back to the AI and say "done" |
| Google stopped working after a week | Test mode signs you out after 7 days. Say "connect Google" again |
| Something else | Run `./kit doctor` and read its `[FAIL]` and `[warn]` lines. Send them to the person running the workshop |
