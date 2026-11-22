---
name: summarize-thread
description: Summarize an email thread, meeting notes or a call transcript into key points, decisions, open questions and promises. Use when the user pastes or points to messy text and wants the gist.
---

# Summarize a thread, meeting or transcript

## Inputs
A file in `inbox/` or text pasted by the user. If a client is named, look them up in `context/clients.csv`.

## Steps
1. Read the whole text. Note who said what and when.
2. Write the summary in this shape:
   - **One line:** what this is about.
   - **Decisions:** what was agreed. Only things that were actually said.
   - **Promises:** who promised what, by when. Mark mine with "Sam:" and theirs with the person's name.
   - **Open questions:** what is still unclear.
   - **Risks or mood:** anything that sounds unhappy, late or vague.
3. If the text has no date for something, write "no date given". Do not guess.
4. Save as `outputs/<date>-summary-<client>.md` and show it.

## Rules
- Never add facts that are not in the text.
- Keep it to one page.
- Quote short phrases when the exact words matter, like a budget.

## Log
Last step: ask the user how many minutes this took them (optional), then run `./kit log add client="<client>" task="<what you did>" skill=summarize-thread minutes=<n> files=<output file> outcome=<done|draft>`.
