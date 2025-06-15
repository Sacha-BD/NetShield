# 🛡️ NetShield – Détection et réponse automatisée aux attaques DDoS

NetShield est un projet de cybersécurité local permettant de détecter, visualiser et réagir automatiquement à des attaques DDoS simulées dans un environnement virtualisé.  
Le tout repose sur un système de détection réseau (Suricata) un dashboard Streamlit en temps réel, et un script Python de blocage automatique des IP malveillantes via iptables.

## 🌐 Contexte

Le projet est exécuté localement dans un environnement isolé composé de trois machines virtuelles :

| Rôle       | Nom VM      | OS              | Adresse IP privée | Description                                                           |
|------------|-------------|-----------------|-------------------|-----------------------------------------------------------------------|
|  Victime   | `VM-Cible`  | Ubuntu-Server   | `192.168.100.10`  | Machine cible recevant l’attaque                                      |
|  Attaquant | `VM-Kali`   | Kali Linux      | `192.168.100.11`  | Machine lançant une attaque DDoS via Docker                           |
|  Moniteur  | `VM-Monitor`| Ubuntu-Desktop  | `192.168.100.12`  | Surveille le trafic avec Suricata, affiche les alertes, bloque les IP |

## 📚 Table des matières

- [🌟 Fonctionnalités](#-fonctionnalités)
- [⚙️ Technologies utilisées](#️-technologies-utilisées)
- [📦 Pré-requis](#-pré-requis)
- [🧰 Structure du projet](#-structure-du-projet)
- [📸 Capture d’écran](#-capture-décran)
- [🎯 Limitations & Perspectives](#-limitations--perspectives)
- [👤 Auteur](#-auteur)

## 🌟 Fonctionnalités

- Surveillance du trafic réseau en temps réel avec Suricata
- Dashboard interactif Streamlit affichant les alertes (filtrage, protocole, horodatage)
- Blocage automatique des IP malveillantes via Iptables
- Simulation réaliste d’attaques DDoS (TCP, UDP, ICMP) à l’aide de conteneurs Docker
- Environnement isolé, sécurisé et personnalisable

## ⚙️ Technologies utilisées

- Suricata – IDS/IPS pour la détection en temps réel
- Docker – Simulation d’attaques DDoS distribuées (TCP/UDP/ICMP)
- Python 3.10 – Automatisation et traitement des alertes
- Environnement virtuel Python (`venv`) – Utilisé pour isoler les dépendances du dashboard Streamlit
- Streamlit – Dashboard de monitoring interactif et épuré
- iptables – Blocage des IP malveillantes

## 📦 Pré-requis

- 3 Machines virtuelles Linux (Ubuntu/Kali)
- Python 3.10 installé sur la VM-Monitor
- Suricata installé sur la VM-Monitor
- Iptables installé sur la VM-Monitor
- Environnement virtuel python venv installé sur la VM-Monitor
- Docker installé sur la VM-Kali
- VirtualBox ou tout autre hyperviseur (projet testé sous macOS avec VirtualBox)

---

## 📁 Structure du projet

```bash
NetShield/
├── README.md
├── LICENSE
│
├── dashboard/                   # Interface Streamlit
│   └── dashboard.py             ← Le dashboard Streamlit
│
├── detection/                   # Script de blocage automatique
│   └── auto_block.py            ← Script de détection et blocage automatique
│
├── docker/                      # Simulation d’attaque DDoS
│   ├── Dockerfile               ← Le fichier Dockerfile d’attaque
│   └── start_attack.sh          ← Le script bash pour lancer l'attaque
│
└── docs/                        # Documentation et visuels
    └── screenshots/             ← captures pour le README

```

## 📸 Capture d’écran

Voici un aperçu du dashboard Streamlit en fonctionnement sur la VM de monitoring :

![NetShield Dashboard](docs/screenshots/dashboard.png)

> 📌 *Le tableau présente les alertes Suricata (TCP/UDP/ICMP) en temps réel avec filtres par IP, protocole et port, ainsi que les IP automatiquement bloquées.*

## 🎯 Limitations & Perspectives

### Limitations actuelles

- 🧱 Projet conçu spécifiquement pour 3 VMs locales (non portable directement sur cloud ou Docker Compose)
- ⚠️ Nécessite une configuration manuelle du réseau (IP statiques, interfaces, etc.)
- 🧪 Le blocage via `iptables` s’applique uniquement à la VM de monitoring
- 🧰 Le système de détection repose uniquement sur des règles Suricata (pas d’auto-apprentissage)

### Pistes d'amélioration

- 🧠 Intégration d’un moteur de scoring comportemental (fréquence, durée, impact)
- 📤 Export automatique des logs (CSV, JSON, base de données)
- 🌐 API REST pour exposer les alertes et gérer les IP bloquées
- 🛠️ Interface admin avec historique, whitelisting, visualisation de courbes
- 📦 Version transportable via Docker Compose ou scripts d’installation automatisés

## 👤 Auteur

Ce projet à été réalisé durant la Mise en Situation Professionnelle à l'ECE Paris.

**Sacha**  
