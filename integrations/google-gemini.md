# Google with Gemini CLI or Antigravity

The kit works as is: Gemini CLI reads `GEMINI.md`, which points to `AGENTS.md`. Antigravity should read `AGENTS.md` or `GEMINI.md` too. Check on a test run: ask "what are your instructions for this folder?"

## Gemini CLI

1. Install and sign in as the Gemini CLI docs say. Start it in the kit folder: `gemini`.
2. Look for an official **Google Workspace** extension for Gemini CLI (Gmail, Calendar, Drive). Run `/extensions` or search the Gemini CLI extensions page. Install it with the command shown there. Sign in with Google.
3. Test: "List my next 3 calendar events."

## Antigravity

Open the kit folder as a workspace. Look in its settings for MCP servers or integrations (the menu name changes). Add the Google connection if offered. If not, use the no-connection fallback in `README.md` of this folder.

## Skills

If your Gemini tool does not load skills by itself, `AGENTS.md` already tells it to read `skills/<name>/SKILL.md`. That is enough.
