# Basic Web Exploitation

When you encounter a login form, some standard SQL injection payloads to try in the username field are:
- `admin' --`
- `admin' #`
- `admin' OR 1=1 --`

# Directory Brute Forcing

Tools like `gobuster` or `ffuf` are excellent for directory brute-forcing. 
Example usage:
`gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt`

# Nmap Scans

Always start a box with a thorough nmap scan. A good standard scan is:
`nmap -sC -sV -oA nmap/initial <target_ip>`

- `-sC`: Run default scripts
- `-sV`: Determine service versions
- `-oA`: Output in all formats
