import subprocess
import os
import requests
from langchain.tools import tool
import nmap
import pyshark
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import DuckDuckGoSearchRun
from chepy import Chepy

@tool
def execute_command(command: str) -> str:
    """Execute a local shell command and return the output. Useful for recon, reading files, etc."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        if len(output) > 2000:
            output = output[:2000] + "\n... [TRUNCATED]"
        return output
    except Exception as e:
        return f"Error executing command: {str(e)}"

@tool
def run_nmap_scan(target: str, arguments: str = "-sV") -> str:
    """Run an Nmap scan on a target with specified arguments. Returns open ports and services."""
    try:
        nm = nmap.PortScanner()
        nm.scan(hosts=target, arguments=arguments)
        output = []
        for host in nm.all_hosts():
            output.append(f"Host: {host} ({nm[host].hostname()}) - State: {nm[host].state()}")
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in sorted(ports):
                    state = nm[host][proto][port]['state']
                    name = nm[host][proto][port]['name']
                    output.append(f"Port: {port}/{proto} - State: {state} - Service: {name}")
        return "\n".join(output) if output else "No results found."
    except Exception as e:
        return f"Error running Nmap: {str(e)}"

@tool
def analyze_pcap(file_path: str, bpf_filter: str = "") -> str:
    """Analyze a pcap file using pyshark. Pass a bpf_filter to narrow down results (e.g., 'tcp port 80'). Returns a summary of packets."""
    try:
        capture = pyshark.FileCapture(file_path, display_filter=bpf_filter)
        packets = []
        for i, pkt in enumerate(capture):
            if i > 20:
                packets.append("... [Output truncated, more packets exist]")
                break
            try:
                protocol = pkt.highest_layer
                src = pkt.ip.src if hasattr(pkt, 'ip') else "unknown"
                dst = pkt.ip.dst if hasattr(pkt, 'ip') else "unknown"
                packets.append(f"[{protocol}] {src} -> {dst}")
            except AttributeError:
                packets.append(f"Packet {i} - {pkt.highest_layer}")
        capture.close()
        return "\n".join(packets) if packets else "No matching packets found."
    except Exception as e:
        return f"Error analyzing pcap: {str(e)}"

@tool
def search_knowledge(query: str) -> str:
    """Search the local knowledge base (RAG) for CTF writeups, CVEs, and hints."""
    try:
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
        docs = db.similarity_search(query, k=3)
        if not docs:
            return "No relevant information found in the knowledge base."
        return "\n\n---\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        return f"Error searching knowledge base: {str(e)}"

@tool
def analyze_image(file_path: str) -> str:
    """Run standard image analysis tools (exiftool, binwalk, strings) on a local image file."""
    output = []
    try:
        output.append("=== EXIFTOOL ===")
        res = subprocess.run(f"exiftool {file_path}", shell=True, capture_output=True, text=True)
        output.append(res.stdout[:500] + ("..." if len(res.stdout) > 500 else ""))
        
        output.append("\n=== BINWALK ===")
        res = subprocess.run(f"binwalk {file_path}", shell=True, capture_output=True, text=True)
        output.append(res.stdout[:500] + ("..." if len(res.stdout) > 500 else ""))
        
        output.append("\n=== STRINGS (Top 20) ===")
        res = subprocess.run(f"strings {file_path} | head -n 20", shell=True, capture_output=True, text=True)
        output.append(res.stdout)
        
        return "\n".join(output)
    except Exception as e:
        return f"Error analyzing image: {str(e)}"


@tool
def search_ctf_writeups(query: str) -> str:
    """Search online for CTF writeups, techniques, and solutions using DuckDuckGo."""
    try:
        search = DuckDuckGoSearchRun()
        return search.invoke(f"CTF writeup {query}")
    except Exception as e:
        return f"Error searching: {str(e)}"

# List of tools to pass to the LangChain agent
agent_tools = [
    execute_command, 
    run_nmap_scan, 
    analyze_pcap, 
    search_knowledge,
    analyze_image,
    search_ctf_writeups
]
