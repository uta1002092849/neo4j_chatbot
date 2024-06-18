#!/bin/bash
set -e

# Start ollama server in the background
ollama serve &
# Record the PID of the ollama server
OLLAMA_PID=$!

# Pause for 5 seconds to allow the server to start
sleep 5

# Pull llama3 model
echo "Retrieving llama3 model..."
ollama pull llama3
echo "Done"

# Start streamlit server in the foreground
streamlit run /app/dashboard.py --server.port 8501 --server.address=0.0.0.0

# Wait for any process to exit
wait -n

# Exit with the status of the first process to exit
exit $?
