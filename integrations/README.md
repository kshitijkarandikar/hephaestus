# Connect your Google account (optional)

The kit works without any connection: you paste or drop text into `inbox/` and get drafts in `outputs/`. Connections are a bonus. They let the assistant read your Gmail, Calendar and Drive directly.

**Status of these guides:** written from memory in November 2026, not tested on the day. Menus and names change often. Test one connection at home before the workshop. If it fails, skip it. The kit still works.

## Safety first (read this)

- Connect **only** if you are comfortable letting this AI tool read that mailbox. For practice, use a test Google account.
- Start with **read-only** access. Add "create draft" later. Never allow "send".
- The assistant rules in `AGENTS.md` say: ask before anything leaves the laptop. That is a rule in a text file, not a lock. Real safety is the permission you grant in the connection.
- Email content can contain tricks ("forward all invoices to ..."). The assistant should treat email as data. Still read what it plans to do before you approve.

## Pick your tool

| Tool | Guide |
|---|---|
| Claude Code (main) | `google-claude-code.md` |
| Gemini CLI or Antigravity | `google-gemini.md` |
| ChatGPT Codex | `google-codex.md` |
| Only a chat window (no files) | `chat-only.md` |

## What each connection adds

| Connection | What it unlocks | Skills that use it |
|---|---|---|
| Gmail | read threads, save drafts | `summarize-thread`, `draft-reply`, `payment-chaser` |
| Google Calendar | see free time, add events | `next-steps` |
| Google Drive | find and read files, save PDFs | `invoice-from-notes` |

## No connection? Do this instead

- Gmail: open the thread, select all, copy, paste into `inbox/thread.txt`.
- Calendar: tell the assistant your plans for the week in a sentence.
- Drive: download the file into `inbox/`. Upload the PDF by hand.
