FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    nmap \
    tshark \
    exiftool \
    binwalk \
    binutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variable to point to local Ollama on the host
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Expose port for the Web UI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
