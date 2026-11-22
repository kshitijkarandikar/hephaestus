# Google with ChatGPT Codex

Codex reads `AGENTS.md` natively. Skills work because `AGENTS.md` tells it to open `skills/<name>/SKILL.md`.

## MCP connection

Codex can use MCP servers listed in its config file, `~/.codex/config.toml`:

```toml
[mcp_servers.google_calendar]
command = "<command that starts the MCP server>"
args = ["<arguments>"]
```

Use a well known Google MCP server, read its permissions, follow its README for the exact command. Restart Codex. Ask it "which tools do you have?" to check.

If this is too fiddly, use the no-connection fallback in `README.md` of this folder. You lose nothing in the workshop.
