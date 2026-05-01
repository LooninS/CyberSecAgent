#!/bin/bash
# scripts/pull_repos.sh
# Run this on your host machine to bypass the Docker/sandbox network restrictions.

echo "================================================="
echo "   Pulling Caveman & CyberChef Repositories      "
echo "================================================="

mkdir -p external_tools
cd external_tools

# Pull Caveman
echo "[+] Installing Caveman via curl..."
curl -fsSL https://raw.githubusercontent.com/JuliusBrussee/caveman/main/install.sh | bash

# Clone CyberChef
echo "[+] Cloning CyberChef..."
if [ ! -d "CyberChef" ]; then
    git clone https://github.com/gchq/CyberChef.git
else
    echo "CyberChef already exists. Pulling latest..."
    cd CyberChef && git pull && cd ..
fi

echo "================================================="
echo " Done. Caveman and CyberChef are available."
echo "================================================="
