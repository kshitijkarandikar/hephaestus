# Run sheet: 60 minutes, 2026-12-08

| Min | Block | What |
|---|---|---|
| 0-10 | Demo | see below |
| 10-15 | Setup | everyone runs `./start.sh`. The AI checks the kit (about 1 minute, nothing is built). Python 3 missing? See SETUP.md step 2. Google file handed out for those who want Google |
| 15-25 | Build 1 together | `invoice-from-notes` with `skill-builder` |
| 25-40 | Build 2 own pick | payment chaser, or a skill from `menu-of-skills.md` |
| 40-45 | Chain | "Do my Friday admin": assistant picks the skills itself. This is the agent moment |
| 45-50 | Buffer | catch up, fix setups |
| 50-60 | Questions | |

Hands-on is about 30 minutes in total (setup plus builds). The 10 minute buffer sits at the end of hands-on and can absorb a slow setup.

## Demo (10 min)

1. (1 min) One slide: agent = instructions + context + skills. Three words.
2. (4 min) Live in Claude Code: drop `inbox/job-notes-acme.txt`, say "invoice this". Show it reading files, using the skill, calculating, asking "ok?", making the PDF.
3. (2 min) Same folder in a second tool (Codex or Gemini). Same job.
4. (2 min) Open one SKILL.md. "It is just English."
5. (1 min) Say: now you build one.

Record the 4 minute part as video before the day.

## Setup is the risky part

The first start makes each AI write the tools and pass the tests. It takes a few minutes and quota. **Ask everyone to run `./start.sh` at home before the day** and send you a screenshot of `./kit doctor`. In the room, you only demo the idea (5 seconds of it running, or the recording). If someone's setup fails, pair them with a neighbour or let them follow along in a chat window (`./start.sh pack`).

## Before the day

- Email attendees: install ONE AI tool, log in, bring Chrome or Edge. Send the clone command and ask them to run `./start.sh` at home. Node.js or Python is helped along by the setup.
- Do a full setup yourself in Python AND in Node on a clean laptop. Note the time it took and the quota it used.
- Test the kit in Claude Code, Codex and Gemini or Antigravity. Note the exact start commands.
- Test Google connections at home. Treat them as bonus, not plan.
- Check free plan limits of each tool. Have a hotspot ready.

## Facilitator tips

- Skills first draft is rough. Show fixing the SKILL.md, not just the answer.
- If someone's tool is chat-only, point to `integrations/chat-only.md` early.
- Remind: fake data only.
