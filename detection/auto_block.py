#!/usr/bin/env python3

import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Fichier de logs de Suricata
LOG_PATH = Path("/var/log/suricata/eve.json")
# Fichier temporaire pour suivre les IPs déjà bloquées
BLOCKED_IPS_FILE = Path("/tmp/blocked_ips.txt")

# Chargement des IPs déjà bloquées (en cas de redémarrage)
blocked_ips = set()
if BLOCKED_IPS_FILE.exists():
    with open(BLOCKED_IPS_FILE, "r") as f:
        for line in f:
            ip = line.strip().split(",")[0]  # On ne garde que l’IP
            if ip:
                blocked_ips.add(ip)

print("[+] Lancement de la détection automatisée...")

def block_ip(ip):
    if ip in blocked_ips:
        return
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        blocked_ips.add(ip)

        with open(BLOCKED_IPS_FILE, "a") as f:
            f.write(ip + "\n")

        print(f"IP bloquée : {ip}")
    except subprocess.CalledProcessError:
        print(f"Échec du blocage de l’IP : {ip}")

def monitor_log():
    with LOG_PATH.open("r") as log_file:
        log_file.seek(0, 2)  # Se place à la fin du fichier
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(0.5)
                continue
            try:
                data = json.loads(line)
                if "alert" in data and "src_ip" in data:
                    ip = data["src_ip"]
                    block_ip(ip)
            except json.JSONDecodeError:
                continue

if __name__ == "__main__":
    monitor_log()