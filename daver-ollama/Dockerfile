FROM ollama/ollama:latest

# nohup wait solution, to wait for ollama to start before pulling models
RUN nohup ollama serve > /tmp/ollama.log 2>&1 & \
    sleep 10 && \
    ollama pull phi4-mini:3.8b && \
    ollama pull gemma3:4b && \
    ollama pull deepseek-coder:6.7b

EXPOSE 11434
ENTRYPOINT ["/bin/ollama"]
CMD ["serve"]