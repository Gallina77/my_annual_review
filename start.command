#!/bin/bash
# Double-click to start My Annual Review. Keep this window open while you use it.
cd "$(dirname "$0")" || exit 1
if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found on this Mac."
  echo "Install it from https://www.python.org/downloads/ and double-click this file again."
  read -n 1 -s -r -p "Press any key to close."
  exit 1
fi
exec python3 server.py
