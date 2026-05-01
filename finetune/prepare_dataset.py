import json
from datasets import load_dataset
import os

def prepare_dataset():
    print("[*] Downloading public cybersecurity dataset from HuggingFace...")
    # We will use a public cybersecurity QA dataset
    # You can change this to any other CTF/infosec dataset you find on HF
    dataset_name = "rdpahalavan/cybersec-data" 
    
    try:
        dataset = load_dataset(dataset_name, split="train")
        print(f"[+] Downloaded {len(dataset)} records.")
    except Exception as e:
        print(f"[-] Failed to download dataset: {e}")
        return

    output_file = "training_data.jsonl"
    print(f"[*] Formatting data into JSONL for Unsloth at {output_file}...")
    
    formatted_data = []
    
    # Format into Alpaca/Instruct format
    # The dataset has 'instruction', 'input', 'output' columns.
    for i, row in enumerate(dataset):
        instruction = row.get("instruction", "")
        input_text = row.get("input", "")
        output_text = row.get("output", "")
        
        # Skip empty rows
        if not instruction or not output_text:
            continue
            
        formatted_data.append({
            "instruction": instruction,
            "input": input_text,
            "output": output_text
        })
        
        # For testing, let's limit to 500 high-quality rows so it trains fast on your 4GB VRAM
        if len(formatted_data) >= 500:
            break

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in formatted_data:
            f.write(json.dumps(item) + '\n')
            
    print(f"[+] Successfully wrote {len(formatted_data)} examples to {output_file}.")
    print("[!] Please review 'training_data.jsonl' to verify the quality before training.")

if __name__ == "__main__":
    prepare_dataset()
