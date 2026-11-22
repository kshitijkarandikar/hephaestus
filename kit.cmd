@echo off
rem Runs the kit program. Needs Python 3.
setlocal
set "ROOT=%~dp0"
set PYTHONDONTWRITEBYTECODE=1
where python >nul 2>nul && (python "%ROOT%core\kit.py" %* & exit /b %ERRORLEVEL%)
where py >nul 2>nul && (py -3 "%ROOT%core\kit.py" %* & exit /b %ERRORLEVEL%)
echo Python 3 is not installed. Run: winget install Python.Python.3.12 1>&2
exit /b 1
