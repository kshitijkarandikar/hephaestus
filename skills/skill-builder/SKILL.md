---
name: skill-builder
description: Build a new skill for this folder. Use when the user says "make a skill", "I do this task often", "turn this into a skill" or wants to automate a repeated task.
---

# Skill builder

A skill is a folder `skills/<name>/` with one file, `SKILL.md`. It is a recipe the assistant follows. You write it with the user, in plain English.

## Steps

1. **Ask what the task is.** One question at a time. Max 5 questions. Cover:
   - What starts the task? (an email, notes, a date)
   - What goes in? (files in `inbox/`, a client name)
   - What must come out? (a file, a draft, a table) Where does it go?
   - What facts must be looked up? (`context/` files)
   - What must never happen? (sending, guessing amounts)
2. **Ask for one real example** of input and a good output. If the user has none, use a file from `inbox/`.
3. **Write `skills/<name>/SKILL.md`** with this shape:
   ```
   ---
   name: <short-name-with-dashes>
   description: <one sentence: what it does AND when to use it>
   ---
   # <Title>
   ## Inputs
   ## Steps          (numbered, each step one action)
   ## Output         (file name pattern, where it goes)
   ## Rules          (what never to do)
   ## Log            (last step: ./kit log add ...)
   ## Example        (short input and output)
   ```
4. **Test it now.** Run the skill on the example. Show the result.
5. **Fix once.** Ask what was wrong. Change the SKILL.md, not just the answer. Run again.
6. **Tell the user** how to use it next time: just ask for the task in normal words.

## Rules for a good skill

- The description line decides if the skill gets used. Say when to use it.
- Steps are actions, not wishes. "Read `context/rates.csv`" beats "know the rates".
- Point to files in `context/`. Do not copy prices or facts into the skill.
- Use a script for math and dates.
- Anything that sends or shares needs an explicit "yes" from the user first.
- Keep it under one page. Split big tasks into two skills.
