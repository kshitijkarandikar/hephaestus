# Only a chat window (ChatGPT, Gemini or Claude on the web)

A chat window cannot read your folder or write files. You do the copying. It still works well.

## Setup (once)

1. In the kit folder run `./start.sh pack` (Windows: `start.cmd pack`). It makes `outputs/pack.md`: one file with the rules, your context and all skills. No AI tool or language needed.
2. Start a new chat project (a "Project" in Claude or ChatGPT, a "Gem" in Gemini). Upload `outputs/pack.md` as project instructions or knowledge. No project feature? Paste the file as your first message.
3. For each task, also paste the input (an email thread, notes, the invoices log).

## Using it

- Say: "Use the draft-reply skill. Here is the thread: ..."
- Copy the result into `outputs/` by hand.
- For a PDF: ask for the HTML, save it as `invoice.html`, open it in Chrome, Print, Save as PDF.
- Math: ask the chat to show each calculation line. Check the total with a calculator.

## Work log in chat-only

The chat cannot run `./kit log`. At the end of a task ask: "Give me the worklog command for this task". You can run it yourself later if you also did the first-start setup in a terminal.

## What you lose

No direct file reading, no tools, no Gmail or Calendar connection. Skills that need a script (`html-to-pdf`) become copy and print steps.
