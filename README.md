# 🛡️ CyberSec Agent

A fully local, autonomous AI agent for CTF competitions and cybersecurity, powered by Ollama.

## Architecture

```
CyberSecAgent/
├── main.py              # FastAPI backend + LangChain ReAct agent
├── tools.py             # 8 cybersec tools (terminal, nmap, pcap, image analysis, cyberchef, etc.)
├── rag_setup.py         # Ingest writeups/notes into local ChromaDB vector store
├── requirements.txt     # Python dependencies
├── run.sh               # One-shot setup & launch script
├── Dockerfile           # Docker container with all system tools pre-installed
├── docker-compose.yml   # Docker Compose for easy container management
├── static/
│   ├── index.html       # Cyberpunk chat interface
│   ├── style.css        # Neon-glow dark theme
│   └── script.js        # Frontend chat logic
└── knowledge_base/      # Drop .md/.txt files here for RAG ingestion
    └── sample_ctf_notes.md
```

## Prerequisites

- **Ollama** installed and running (`ollama serve`)
- **Python 3.10+**
- (Optional) **Docker** for sandboxed execution

## Quick Start

### Option 1: Direct (Fastest)

```bash
# Pull models
ollama pull dolphin-llama3
ollama pull nomic-embed-text

# Run the setup & launch script
chmod +x run.sh
./run.sh
```

Open **http://localhost:8000** in your browser.

### Option 2: Docker (Sandboxed)

```bash
docker-compose up -d --build
```

Open **http://localhost:8000** in your browser.

## Tools Available

| Tool | Description |
|---|---|
| `execute_command` | Run any shell command |
| `run_nmap_scan` | Port/service scanning via Nmap |
| `analyze_pcap` | Packet capture analysis via PyShark/tshark |
| `analyze_image` | Run exiftool, binwalk, strings on files |
| `aperisolve_scan` | Steganography analysis advisory |
| `cyberchef_recipe` | Chain encoding/decoding ops (base64, rot13, hex, etc.) |
| `search_knowledge` | Query local RAG knowledge base |
| `search_ctf_writeups` | Search the web for CTF writeups via DuckDuckGo |
| `analyze_memory` | Memory forensics via Volatility 3 |
| `analyze_binary_ghidra` | Headless binary analysis using Ghidra |
| `run_metasploit_module` | Execute Metasploit exploits/auxiliary via msfrpcd |

## RAG Knowledge Base

Drop any `.md` or `.txt` files into the `knowledge_base/` folder, then run:

```bash
python rag_setup.py
```

This will chunk and embed them locally using `nomic-embed-text` into a ChromaDB vector store. The agent can then recall this information during conversations.

## Model

Uses **dolphin-llama3** — an uncensored Llama 3 variant that won't refuse legitimate cybersecurity queries. Lightweight enough to run on most machines with 8GB+ RAM.

## Local Fine-Tuning Pipeline

The project includes a local fine-tuning pipeline designed for low-VRAM environments (like an NVIDIA Quadro T1000 with 4GB VRAM) using Unsloth. The scripts are located in the `finetune/` directory:

1. **Prepare Dataset (`prepare_dataset.py`)**: Downloads a public cybersecurity dataset from HuggingFace and formats it into JSONL.
2. **Train LoRA (`train_lora.py`)**: Fine-tunes a lightweight model (e.g., Llama-3.2-1B-Instruct) using 4-bit quantization and LoRA adapters.
3. **Export to Ollama (`export_to_ollama.sh`)**: Converts the fine-tuned adapter into a GGUF file and automatically creates an Ollama Modelfile (`hackon-1b`).

After training, you can update `MODEL_NAME` in `main.py` to your custom model (e.g., `hackon-1b`).

## TODO & Next Steps

- [ ] **Agent Memory Enhancements**: Implement a robust short-term/long-term memory system across different chat sessions or CTF challenges.
- [ ] **Multi-Agent Architecture**: Separate responsibilities into sub-agents (e.g., a reverse engineering specialist, a web exploitation specialist).
- [ ] **Automated Reporting**: Generate a polished CTF writeup or pentest report automatically from the agent's actions and tool outputs.
- [ ] **UI/UX Improvements**: Add data visualization in the frontend for complex outputs like Nmap graphs and packet capture summaries.

