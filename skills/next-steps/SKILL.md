---
name: next-steps
description: Turn notes, a summary or a thread into a plan of next steps with owners and dates. Use when the user asks "what should I do next", "make a to-do list" or "plan the follow-up".
---

# Plan next steps

## Inputs
Notes, a summary from `summarize-thread`, or an inbox file. Optional: today's date and my working days (`context/business.md`).

## Steps
1. List every action found in the text. Split big actions into small ones that take under 2 hours.
2. For each action give: what, who, due date, how long.
   - Dates must fit my working days. If a client is on holiday, plan around it.
   - If no date is stated, propose one and mark it "(proposed)".
3. Order by date. Put anything that blocks someone else first.
4. Add a **Waiting on others** list: what I need from the client and the date I will chase.
5. Save as `outputs/<date>-next-steps-<client>.md`.
6. If Google is connected, check free time first: `./kit google calendar freebusy from=<date> to=<date> hours=09:00-17:00 days=Mon,Tue,Wed,Thu`. Then offer to create events for the dated actions with `./kit google calendar create title=... start=... end=...` (needs level draft). Ask first. Never create without a "yes". Events never have guests.

## Output shape
| Action | Who | Due | Time |
|---|---|---|---|

## Rules
- Do not add work nobody asked for.
- Flag anything that depends on a missing answer.

## Log
Last step: ask the user how many minutes this took them (optional), then run `./kit log add client="<client>" task="<what you did>" skill=next-steps minutes=<n> files=<output file> outcome=<done|draft>`.
