#!/bin/bash

echo "=== System Health Check ==="
echo "Date: $(date)"

# Check CPU load
echo -e "\n[CPU Load]"
uptime | awk -F'load average:' '{ print $2 }'

# Check Memory
echo -e "\n[Memory Usage]"
free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }'

# Check Disk Space
echo -e "\n[Disk Usage (/)]"
df -h / | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}'

# Network Check (Google DNS)
echo -e "\n[Network Status]"
if ping -c 1 8.8.8.8 &> /dev/null; then
    echo "Network is UP"
else
    echo "Network is DOWN"
fi

echo -e "\n=== Health Check Complete ==="
