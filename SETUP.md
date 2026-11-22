# Setup: start here

Read the steps one by one and do each one. Each step says what you should see. If you do not see it, go to "If something goes wrong" at the bottom.

**Part 1** gets the kit running. It takes about 10 minutes. **Part 2** connects Google (Gmail, Calendar, Drive). It is optional and takes about 5 minutes if the workshop host gives you a Google file, or about 30 minutes if you make your own. Do Part 1 before the workshop. Do Part 2 only if you want it.

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
git clone https://github.com/kshitijkarandikar/hephaestus.git business-agent-kit
cd business-agent-kit
```

You should see: a new folder `business-agent-kit`, and your terminal is now inside it. Type `ls` (Mac) or `dir` (Windows) to see files like `AGENTS.md` and `start.sh`.

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

1. **Get the Google file.** At the workshop, the host gives you a file. Save it in the `secrets` folder of the kit and name it exactly `google-client.json`. On your own, the AI walks you through making one.
2. In the AI, type: **connect Google**
3. The AI runs the sign-in. A browser tab opens. Choose your Google account and click **Allow**. If Google says "hasn't verified this app", click **Advanced**, then **Go to ... (unsafe)**. That warning is normal for a test app.
4. The AI tests it by reading your next 7 days of calendar and 3 recent emails.

You should see: a short list of your calendar and emails. In test mode, Google signs you out after 7 days. Run step 2 again then.

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
| `./kit: command not found` | You are not in the kit folder. Type `cd business-agent-kit` |
| Google sign-in says the file is missing | The file must be at `secrets/google-client.json`, with exactly that name |
| Google stopped working after a week | Test mode signs you out after 7 days. Say "connect Google" again |
| Something else | Run `./kit doctor` and read its `[FAIL]` and `[warn]` lines. Send them to the person running the workshop |
