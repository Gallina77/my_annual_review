@echo off
rem Double-click to start My Annual Review. Keep this window open while you use it.
cd /d "%~dp0"
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo Python 3 was not found. Install it from https://www.python.org/downloads/ and run this again.
  pause
  exit /b 1
)
%PY% server.py
pause
