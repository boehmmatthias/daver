# entrypoint.sh
#!/usr/bin/env bash
# Launch Ollama in background
ollama serve &
pid="$!"

# Wait for server to be ready (adjust if needed)
sleep 5

# Pre-pull one or more models
ollama pull llama3.2
#ollama pull gemma3:4b

# Keep Ollama running
wait "$pid"
