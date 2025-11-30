#!/bin/bash

echo "=============================================="
echo "    Advanced Multi-threaded Port Scanner      "
echo "=============================================="

# Get target IP or Domain
read -p "Enter target IP or Domain: " target

# Get port range
read -p "Enter Start Port: " start_port
read -p "Enter End Port: " end_port

# Get output filename
read -p "Enter output file name (e.g. results.txt): " outfile

echo ""
echo "Scanning ports $start_port to $end_port on $target ..."
echo "Results will be saved to $outfile"
echo "----------------------------------------------"

# Create or clear output file
echo "Port Scan Results for $target" > "$outfile"
echo "----------------------------------------------" >> "$outfile"

# Service mapping function
get_service() {
    case $1 in
        21) echo "FTP";;
        22) echo "SSH";;
        23) echo "Telnet";;
        25) echo "SMTP";;
        53) echo "DNS";;
        80) echo "HTTP";;
        110) echo "POP3";;
        143) echo "IMAP";;
        443) echo "HTTPS";;
        3306) echo "MySQL";;
        3389) echo "RDP";;
        8080) echo "HTTP-ALT";;
        *) echo "Unknown";;
    esac
}

scan_port() {
    port=$1
    nc -z -w 1 $target $port 2>/dev/null
    if [ $? -eq 0 ]; then
        service=$(get_service $port)
        echo "Port $port OPEN ($service)"
        echo "Port $port OPEN ($service)" >> "$outfile"
    fi
}
