#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Use local workspace venv if available
if [ -f "$DIR/../.venv/bin/python" ]; then
    PYTHON="$DIR/../.venv/bin/python"
elif [ -f "$DIR/.venv/bin/python" ]; then
    PYTHON="$DIR/.venv/bin/python"
else
    PYTHON="python3"
fi

PORT="${PORT:-8000}"
HOST="${HOST:-127.0.0.1}"

echo "=========================================================="
echo " 🛰️  LAUNCHING PERSONAL COMMAND CENTER (AETHER OS)"
echo "=========================================================="
echo " Python: $PYTHON"
echo " Host:   http://$HOST:$PORT"
echo " Docs:   http://$HOST:$PORT/docs"
echo "=========================================================="

exec "$PYTHON" -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
