#!/usr/bin/env bash
set -e

# Check for -d flag
DETACH=""
if [ "$1" = "-d" ]; then
  DETACH="-d"
fi

# Load .env
export $(grep -v '^#' .env | xargs)

# Choose whether to spin up local Ollama
if [ -z "$OLLAMA_HOST" ]; then
  echo "Starting Ollama in local mode..."
  docker compose --profile local-ollama up $DETACH
else
  echo "Starting Ollama in remote mode..."
  docker compose up $DETACH
fi