FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    nmap \
    tshark \
    exiftool \
    binwalk \
    binutils \
    curl \
    wget \
    unzip \
    default-jre \
    hashcat \
    john \
    steghide \
    radare2 \
    strace \
    ltrace \
    jq \
    smbclient \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# Install Ghidra
RUN wget -q https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0.3_build/ghidra_11.0.3_PUBLIC_20240410.zip -O /tmp/ghidra.zip && \
    unzip -q /tmp/ghidra.zip -d /opt/ && \
    rm /tmp/ghidra.zip && \
    ln -s /opt/ghidra_11.0.3_PUBLIC/support/analyzeHeadless /usr/local/bin/analyzeHeadless

# Install Metasploit Framework
RUN curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
    chmod 755 msfinstall && \
    ./msfinstall && \
    rm msfinstall
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variable to point to local Ollama on the host
ENV OLLAMA_HOST=http://host.docker.internal:11434

# Expose port for the Web UI
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
