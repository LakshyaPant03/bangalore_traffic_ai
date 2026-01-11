#!/bin/bash

# 1. Start the API in the background (&)
uvicorn src.api:app --host 0.0.0.0 --port 8000 &

# 2. Wait for API to wake up
echo "Waiting for API to start..."
sleep 5

# 3. Start the Frontend
streamlit run src/frontend.py --server.port $PORT --server.address 0.0.0.0