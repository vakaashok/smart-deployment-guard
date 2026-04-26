#!/bin/bash

LOG_FILE="logs/deployment.log"

echo "Running Smart Deployment Guard..."

result=$(python scripts/decision_engine.py)

echo "Decision Result: $result"

timestamp=$(date)
status=$(echo "$result" | grep -o "SUCCESS\|BLOCKED")

echo "----------------------------------------" >> "$LOG_FILE"
echo "Time: $timestamp" >> "$LOG_FILE"
echo "Status: $status" >> "$LOG_FILE"
echo "$result" | grep -o "'cpu_usage': [^,]*" >> "$LOG_FILE"
echo "$result" | grep -o "'memory_free': [^,]*" >> "$LOG_FILE"
echo "$result" | grep -o "'disk_usage': [^,]*" >> "$LOG_FILE"
echo "$result" | grep -o "'port_available': [^}]*" >> "$LOG_FILE"

if echo "$result" | grep -q "BLOCKED"; then
    echo "Deployment Blocked!"
    echo "Deployment blocked. Starting self-healing..." >> "$LOG_FILE"

    echo "Running Self-Healing..."
    python scripts/self_healing.py

    echo "Self-healing completed. Deployment stopped for safety." >> "$LOG_FILE"
    echo "Self-healing completed. Re-run deployment after checking health."

    exit 1
else
    echo "Deployment Allowed!"

    echo "Building Docker image..." >> "$LOG_FILE"
    echo "Building Docker image..."
    docker build -t smart-deployment-guard .

    echo "Running Docker container..." >> "$LOG_FILE"
    echo "Running Docker container..."
    docker run --rm smart-deployment-guard

    echo "Deployment Successful" >> "$LOG_FILE"
    echo "Deployment Successful"
fi