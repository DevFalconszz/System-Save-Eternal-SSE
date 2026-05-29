#!/usr/bin/env bash
# SSE — Atalho para Linux 🐧
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"

if [ -f "${SCRIPT_DIR}/venv/bin/activate" ]; then
    source "${SCRIPT_DIR}/venv/bin/activate"
    exec python3 "${SCRIPT_DIR}/src/main.py" "$@"
else
    exec python3 "${SCRIPT_DIR}/src/main.py" "$@"
fi
