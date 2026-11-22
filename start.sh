#!/usr/bin/env bash
# One command to get started on Mac and Linux:   ./start.sh
#   ./start.sh            pick an AI tool and start it in this folder
#   ./start.sh claude     start Claude Code (also: codex, gemini)
#   ./start.sh pack       make outputs/pack.md for a chat window (no AI tool needed)
cd "$(dirname "$0")" || exit 1

PROMPT_SETUP="Read setup/BOOTSTRAP.md and do the first run of this kit."
PROMPT_NORMAL="What can you do in this folder?"
if grep -qs "First run, kit is healthy" worklog/*.json; then PROMPT="$PROMPT_NORMAL"; else PROMPT="$PROMPT_SETUP"; fi

if [ "$1" = "pack" ]; then
  mkdir -p outputs
  {
    printf '# PACK: paste or upload this once at the start of a chat\n\nYou have no file access. Everything you need is below. When a task matches a skill, follow that skill'"'"'s steps. Output files as text I can copy.\n\n'
    for f in AGENTS.md security/policy.md context/business.md context/brand-voice.md context/rates.csv context/clients.csv context/invoices-log.csv skills/*/SKILL.md; do
      printf '## FILE: %s\n' "$f"; cat "$f"; printf '\n'
    done
  } > outputs/pack.md
  echo "Made outputs/pack.md. Upload it to a Project or Gem, or paste it as your first message. See integrations/chat-only.md."
  exit 0
fi

tools=""
for t in claude codex gemini; do command -v "$t" >/dev/null 2>&1 && tools="$tools $t"; done

launch() {
  echo
  echo "Starting $1 in this folder."
  [ "$PROMPT" = "$PROMPT_SETUP" ] && echo "First run: the AI checks the kit (about a minute)."
  echo "If it does not start by itself, type:  $PROMPT"
  echo
  case "$1" in
    claude|codex) exec "$1" "$PROMPT" ;;
    *) exec "$1" ;;
  esac
}

if [ -n "$1" ]; then
  case "$1" in claude|codex|gemini) ;; *) echo "Unknown option: $1"; exit 1;; esac
  command -v "$1" >/dev/null 2>&1 || { echo "$1 is not installed. See the install links below."; tools=""; }
  [ -n "$tools" ] && launch "$1"
fi

if [ -n "$tools" ]; then
  echo "Found:$tools"
  set -- $tools
  if [ $# -eq 1 ]; then launch "$1"; fi
  echo "Which one?"
  select t in "$@" quit; do
    [ "$t" = "quit" ] && exit 0
    [ -n "$t" ] && launch "$t"
  done
  exit 0
fi

cat <<'MSG'
No AI tool found. Install one, then run ./start.sh again:

  Claude Code    https://docs.claude.com/en/docs/claude-code/setup
  ChatGPT Codex  https://github.com/openai/codex
  Gemini CLI     https://github.com/google-gemini/gemini-cli

Only have a chat window (ChatGPT, Gemini, Claude in a browser)? Run: ./start.sh pack
MSG
exit 1
