#!/bin/bash
# scripts/export_to_ollama.sh
# This script converts the fine-tuned LoRA model into a GGUF format and adds it to your local Ollama instance.

echo "================================================="
echo "   Exporting Fine-Tuned Model to Ollama          "
echo "================================================="

if [ ! -d "lora_model" ]; then
    echo "[-] Error: 'lora_model' directory not found. Please run train_lora.py first."
    exit 1
fi

echo "[+] Generating Ollama Modelfile..."

# Unsloth makes exporting to GGUF very easy via python
cat << 'EOF' > export_gguf.py
from unsloth import FastLanguageModel
import os

model_name = "unsloth/Llama-3.2-1B-Instruct"
max_seq_length = 512
dtype = None
load_in_4bit = True

print("[*] Loading base model and applying LoRA weights...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "lora_model",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

print("[*] Exporting to Ollama GGUF (q4_k_m quantization)...")
model.save_pretrained_gguf("ollama_export", tokenizer, quantization_method = "q4_k_m")
print("[+] Export complete!")
EOF

python3 export_gguf.py

echo "[+] Loading GGUF into Ollama..."
# The exported file usually ends up in the ollama_export dir, let's find it
GGUF_FILE=$(find ollama_export -name "*.gguf" | head -n 1)

if [ -z "$GGUF_FILE" ]; then
    echo "[-] Error: GGUF file not generated."
    exit 1
fi

cat << EOF > Modelfile
FROM $GGUF_FILE
TEMPLATE """{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

"""
PARAMETER stop "<|eot_id|>"
EOF

ollama create hackon-1b -f Modelfile

echo "================================================="
echo " Done. Your model is available in Ollama as 'hackon-1b'"
echo " You can now update MODEL_NAME in main.py to use it!"
echo "================================================="
