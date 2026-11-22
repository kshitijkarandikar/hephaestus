---
name: draft-reply
description: Draft an email reply or follow-up to a client in the freelancer's voice. Use when the user wants an email written, answered or followed up. Never sends anything.
---

# Draft an email

## Inputs
What the email is for, plus the thread or notes (`inbox/` or pasted). Client from `context/clients.csv`.

## Steps
0. If the user wants this saved as a Gmail draft, ask now for the recipient's email address (check `context/clients.csv` first). Gmail cannot make a draft without one. If they only want text to copy, no address is needed. Say which kind you are making: a copy-ready text, or a Gmail draft.
1. Read `context/brand-voice.md` and the client's row in `context/clients.csv` (the notes column matters).
2. Read the thread or notes. Find: what they asked, what I promised, what I need.
3. Write the draft:
   - Subject line.
   - First two lines: the point or the answer.
   - Answer every question they asked. Skip nothing.
   - Close with one next step and a date.
4. Save as `outputs/<date>-email-<client>.md`. Show it.
5. If Google is connected (`./kit google status` says signed in with level draft), offer to save it as a **draft** in Gmail with `./kit google gmail draft to=<address> subject=<subject> body_file=<the file you saved> thread=<thread id>`. Only after the user says yes. Never send. Without Google, the user copies the text.

## Rules
- Do not invent prices, dates or promises. Put `[CHECK: ...]` where a fact is missing.
- Match the language of the client's last email.
- Max 150 words unless the user asks for more.

## Log
Last step: ask the user how many minutes this took them (optional), then run `./kit log add client="<client>" task="<what you did>" skill=draft-reply minutes=<n> files=<output file> outcome=<done|draft>`.
