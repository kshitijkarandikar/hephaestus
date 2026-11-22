@echo off
rem One command to get started on Windows:   start.cmd
rem   start.cmd            start the first AI tool found in this folder
rem   start.cmd claude     start a specific tool (also: codex, gemini)
rem   start.cmd pack       make outputs\pack.md for a chat window (no AI tool needed)
cd /d "%~dp0"

set "PROMPT=Read setup/BOOTSTRAP.md and set up this kit."
if exist setup\runtime.json set "PROMPT=What can you do in this folder?"

if /i "%~1"=="pack" goto pack
set "CHOICE=%~1"
if not "%CHOICE%"=="" goto launch
for %%t in (claude codex gemini) do call :probe %%t
if "%CHOICE%"=="" goto none
goto launch

:probe
if not "%CHOICE%"=="" exit /b
where %1 >nul 2>nul
if not errorlevel 1 set "CHOICE=%1"
exit /b

:launch
where %CHOICE% >nul 2>nul
if errorlevel 1 (
  echo %CHOICE% is not installed.
  goto none
)
echo.
echo Starting %CHOICE% in this folder.
if not exist setup\runtime.json echo First run: the AI will build the kit's tools. You will be asked a few questions.
echo If it does not start by itself, type:  %PROMPT%
echo.
if /i "%CHOICE%"=="gemini" (gemini) else (%CHOICE% "%PROMPT%")
exit /b

:pack
if not exist outputs mkdir outputs
(
  echo # PACK: paste or upload this once at the start of a chat
  echo.
  echo You have no file access. Everything you need is below. When a task matches a skill, follow that skill's steps. Output files as text I can copy.
  echo.
  for %%f in (AGENTS.md security\policy.md context\business.md context\brand-voice.md context\rates.csv context\clients.csv context\invoices-log.csv skills\*\SKILL.md) do (
    echo ## FILE: %%f
    type "%%f"
    echo.
  )
) > outputs\pack.md
echo Made outputs\pack.md. Upload it to a Project or Gem, or paste it as your first message. See integrations\chat-only.md.
exit /b

:none
echo No AI tool found. Install one, then run start.cmd again:
echo.
echo   Claude Code    https://docs.claude.com/en/docs/claude-code/setup
echo   ChatGPT Codex  https://github.com/openai/codex
echo   Gemini CLI     https://github.com/google-gemini/gemini-cli
echo.
echo Only have a chat window? Run: start.cmd pack
exit /b 1
