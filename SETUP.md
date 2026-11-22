# Setup: start here

Read the steps one by one and do each one. Each step says what you should see. If you do not see it, go to "If something goes wrong" at the bottom.

**Part 1** gets the kit running. It takes about 15 minutes. **Part 2** connects Google (Gmail, Calendar, Drive). It is optional and takes about 30 minutes. Do Part 1 before the workshop. Do Part 2 only if you want it.

Use **fake client data** while you practise. Everything you type goes to your AI provider.

---

## Part 1: Get the kit running

### Step 1. Install an AI tool that works in a folder

You need one of these. Pick the one you already have an account for:

- **Claude Code** (best tested): https://docs.claude.com/en/docs/claude-code/setup
- **ChatGPT Codex**: https://github.com/openai/codex
- **Gemini CLI**: https://github.com/google-gemini/gemini-cli

You should see: the install page finishes without errors. Check it later in step 5.

### Step 2. Install git

Open a terminal (Mac: the app "Terminal". Windows: "Windows Terminal" or "Command Prompt"). Type:

```
git --version
```

You should see a version number. If you see "command not found", install git from https://git-scm.com/downloads, close the terminal, open a new one, and try again.

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

### Step 5. Answer the language question

The AI is now setting up the kit. First it checks which programming language your laptop has: Node.js or Python.

- It asks you which one to use. Pick either. If you do not care, say **Python**.
- If you have neither, it tells you how to install one. Do that, close the AI tool, and start again from step 4.

You should see: a message like `Found Python 3.12` and your question.

### Step 6. Let it build

The AI now writes a small program for you, using plain-English instructions in the `spec/` folder. This takes about 5 to 10 minutes. It will ask for permission to create files and run commands. Say yes to those. They stay inside the kit folder. Say no to anything that touches other folders or the internet.

You should see: at the end, something like `All 23 conformance checks passed` and `54 passed` (or more) for the security tests.

If a test fails, the AI fixes its own code. That is normal. If it is still failing after 5 tries, see the bottom of this page.

### Step 7. Review and approve

The AI asks: **"Do you approve this code?"**

You do not need to read all of it. It is good to ask first:

```
Explain in plain English what the security parts of core/ do.
```

When you are happy, type: **yes**

You should see: the AI thanks you and asks you to run one command yourself (next step).

### Step 8. Seal it (you do this one, not the AI)

This records a checksum of the safety code, so any later change is noticed. The AI is not allowed to do this step. That is on purpose.

Open a **second terminal window** (or a new tab), go to the kit folder (`cd business-agent-kit`) and type:

Mac and Linux:
```
./kit check seal
```
Windows:
```
kit check seal
```

In Claude Code you can also type `! ./kit check seal` in the prompt.

You should see: `Sealed 4 files in setup/core.sha256.json` (the number may differ).

Then go back to the AI and type: **sealed**

### Step 9. Finish and restart

The AI checks the seal, runs a health check (`./kit doctor`), and writes the first line in your work log. Then it tells you to restart.

1. Close the AI tool (type `/exit`, or press Ctrl+C twice).
2. Run `./start.sh` (Windows: `start.cmd`) again.

You should see: the AI starts again, this time without building anything.

### Step 10. Try it

Type these one at a time:

```
What can you do in this folder?
```

You should see a list of skills: summarize, draft a reply, next steps, PDF, skill builder.

```
Summarize inbox/meeting-notes-noord-studio.txt
```

You should see: a summary with decisions, promises and open questions. It saves a file in `outputs/` and asks how many minutes it took you. Answer with a number, or say you do not know.

### Step 11. Check your work log

In the second terminal:

```
./kit log list
```

You should see: a line for the task you just did.

Also try:

```
./kit doctor
```

You should see: `All good.`

**Part 1 is done.**

---

## Part 2: Connect Google (optional)

This lets the AI read your Gmail, Calendar and Drive, and prepare drafts. It never sends, deletes or shares anything. Follow `integrations/google-kit.md` step by step. It starts with asking the AI to add the Google tool.

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
| Neither Node.js nor Python is found | Mac: `brew install python`. Windows: `winget install Python.Python.3.12`. Or download from python.org. Then open a new terminal |
| The AI keeps failing a test | Close it, start again with a stronger model if you can, and say: `Run setup/BOOTSTRAP.md again from step 3` |
| The AI says "denied" for `./kit check seal` | Right. You run that one yourself (step 8) |
| `./kit: command not found` | Setup is not finished. Do steps 4 to 9 |
| Something else | Run `./kit doctor` and read its `[FAIL]` and `[warn]` lines. Send them to the person running the workshop |
