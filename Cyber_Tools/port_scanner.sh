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
