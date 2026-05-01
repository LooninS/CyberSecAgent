#!/bin/bash
set -e

echo "========================================"
echo "  CyberSec Agent - Setup & Launch"
echo "========================================"

cd "$(dirname "$0")"

# 1. Pull Ollama models
echo "[1/4] Pulling Ollama models..."
ollama pull dolphin-llama3
ollama pull nomic-embed-text

# 2. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[2/4] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[2/4] Virtual environment already exists."
fi

# 3. Install dependencies
echo "[3/4] Installing Python dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# 4. Launch the server
echo "[4/4] Starting CyberSec Agent on http://localhost:8000 ..."
echo "========================================"
python main.py
