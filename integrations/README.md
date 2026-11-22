# Integrations

## Google (Gmail, Calendar, Drive)

Use **`google-kit.md`**. It sets up `kit google`, the kit's own tool that talks to Google's plain REST APIs with OAuth. It does not use MCP connectors, because those are not reliable for reading and writing email yet. It works with any AI tool, is tested offline, and keeps the kit's safety rules.

- Reads: Gmail threads, calendar events and free time, Drive files.
- Writes (level `draft`, always asks you first): Gmail drafts, calendar events without guests, Drive uploads of files you made.
- Never: send, delete, share or invite. No such command exists, and the security rules block them.
- Use a test Google account while you practise.

## No connection

The kit works without any connection:

- Gmail: open the thread, select all, copy, paste into `inbox/thread.txt`.
- Calendar: tell the assistant your plans for the week in a sentence.
- Drive: download the file into `inbox/`. Upload the PDF by hand.

## Only a chat window

See `chat-only.md`.
