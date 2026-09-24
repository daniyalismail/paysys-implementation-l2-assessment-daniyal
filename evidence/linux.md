# Linux Evidence

## OS/Kernel Identification
```text
Linux daniyals-lappy 6.17.0-40-generic #40~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Tue Jun 23 16:48:12 UTC 2 x86_64 x86_64 x86_64 GNU/Linux
PRETTY_NAME="Ubuntu 24.04.4 LTS"
```

## CPU, Memory and Disk Utilization
**CPU & Memory (`top -bn1 | head -n 5` & `free -h`)**:
```text
               total        used        free      shared  buff/cache   available
Mem:            15Gi       7.1Gi       5.6Gi       1.0Gi       4.1Gi       8.4Gi
Swap:             0B          0B          0B

top - 12:35:16 up 14 min,  1 user,  load average: 1.93, 1.88, 1.34
Tasks: 332 total,   3 running, 329 sleeping,   0 stopped,   0 zombie
%Cpu(s): 17.8 us,  3.3 sy,  0.0 ni, 77.8 id,  1.1 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :  15868.6 total,   5764.8 free,   7308.4 used,   4170.5 buff/cache
MiB Swap:      0.0 total,      0.0 free,      0.0 used.   8560.3 avail Mem
```

**Disk Utilization (`df -h`)**:
```text
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           1.6G  2.5M  1.6G   1% /run
/dev/nvme0n1p5   62G   56G  3.5G  95% /
tmpfs           7.8G  483M  7.3G   7% /dev/shm
tmpfs           5.0M  8.0K  5.0M   1% /run/lock
efivarfs        384K   96K  284K  26% /sys/firmware/efi/efivars
/dev/nvme0n1p1   96M   48M   49M  50% /boot/efi
tmpfs           1.6G  140K  1.6G   1% /run/user/1000
/dev/sda5       113G   69G   39G  64% /media/daniyalismail19/backup1
```

## Listening Ports and Relevant Processes (`ss -tulpn`)
```text
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess

udp   UNCONN 0      0         127.0.0.54:53         0.0.0.0:*
udp   UNCONN 0      0      127.0.0.53%lo:53         0.0.0.0:*
udp   UNCONN 0      0            0.0.0.0:51225      0.0.0.0:*    users:(("chrome",pid=3597,fd=61))
udp   UNCONN 0      0            0.0.0.0:51568      0.0.0.0:*    users:(("chrome",pid=3597,fd=218))
udp   UNCONN 0      0            0.0.0.0:37728      0.0.0.0:*
udp   UNCONN 0      0        224.0.0.251:5353       0.0.0.0:*    users:(("chrome",pid=3542,fd=1207))
udp   UNCONN 0      0        224.0.0.251:5353       0.0.0.0:*    users:(("chrome",pid=3597,fd=211))
udp   UNCONN 0      0            0.0.0.0:5353       0.0.0.0:*
udp   UNCONN 0      0                  *:48656            *:*    users:(("chrome",pid=3597,fd=159))
```

## DNS/Network Connectivity Checks (`ping -c 2 8.8.8.8`)
```text
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=18.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=116 time=18.5 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 18.494/18.512/18.531/0.018 ms
```

## Application/Container Logs
Since no specific containers are running yet, an example command to fetch logs for a docker container named `minipay-api` would be:
```bash
docker logs minipay-api --tail 50 -f
```

## Identifying the Process Consuming the Most Memory (`ps -eo pid,cmd,%mem --sort=-%mem | head -n 5`)
```text
    PID CMD                         %MEM
   3542 /opt/google/chrome/chrome    5.9
   4746 /opt/google/chrome/chrome -  5.0
   4415 /opt/google/chrome/chrome -  3.6
   8223 /opt/google/chrome/chrome -  2.9
```

## Identifying Disk Usage by Directory (`du -h --max-depth=1 /home/daniyalismail19 | sort -hr | head -n 5`)
```text
35G     /home/daniyalismail19
9.8G    /home/daniyalismail19/.cache
7.3G    /home/daniyalismail19/.config
3.7G    /home/daniyalismail19/.vscode
3.4G    /home/daniyalismail19/.npm
```

## Simple Repeatable Health-Check Script
See `investigation/health-check.sh`

## Troubleshooting Explanations

- **High CPU:** I would use `top` or `htop` to identify the process using the most CPU. If it's a known application, I would check its logs. If it's a web service, it might be receiving high traffic or stuck in a loop.
- **Low disk space:** I would run `df -h` to see which partition is full, then `du -h --max-depth=1 /path | sort -hr` to drill down and find the largest directories/files (often logs or database backups). I would safely compress or delete old logs.
- **Unreachable API:** I would first check if the process is running using `systemctl status` or `docker ps`. Then I would check if the port is listening using `ss -tulpn`. Next, I'd check logs to see if it crashed, and use `curl -v http://localhost:PORT/health` to test locally. Lastly, check firewall rules.
- **Repeatedly terminating process:** I would look at the exit code of the process (e.g., using `journalctl -u service_name` or `docker inspect <container>`). Common causes are Out of Memory (OOM) kills (check `dmesg -T | grep -i oom`), misconfiguration, or missing dependencies.
