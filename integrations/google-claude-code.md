# Google with Claude Code

Two routes. Try A first. It is the easiest.

## Route A: connectors from your Claude account

1. Open claude.ai in a browser, go to **Settings, Connectors** (the name may be "Integrations").
2. Find **Gmail**, **Google Calendar** and **Google Drive**. Click Connect on each. Sign in with Google. Read the permissions on the screen.
3. Start Claude Code in the kit folder (`cd business-agent-kit` then `claude`) while logged in with the same account.
4. Type `/mcp`. You should see the Google connectors in the list. If not, they are not available on your plan or login. Use Route B or the "no connection" fallback.
5. Test: "List my next 3 calendar events." Then: "Find the last email from <someone you know> and summarize it."

Connectors from your account are usually read and draft only. Check what each one offers on the connect screen.

## Route B: your own MCP server

An MCP server is a small program that gives the assistant tools. Many exist for Google. Pick a well known one with many users, read what it asks permission for, and follow its README. Typical command:

```
claude mcp add <name> <command-to-start-the-server>
```

Then `/mcp` to check it is connected. Use `claude mcp list` to see all.

## Test prompts

- "Read `inbox/email-thread-bloem.txt` and use the summarize-thread skill."
- "Find the latest email from a client in Gmail and draft a reply as a Gmail draft. Do not send."
- "Look at my calendar next week and tell me which days have 3 free hours."
