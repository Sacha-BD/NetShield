import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import datetime
import time
import pytz

st.set_page_config(page_title="Dashboard Suricata", layout="wide")
st.title("Suricata – Alertes et IP bloquées automatiquement")

# Chemins
LOG_FILE = Path("/var/log/suricata/eve.json")
BLOCKED_FILE = Path("/tmp/blocked_ips.txt")

# Session state
if "seen" not in st.session_state:
    st.session_state.seen = set()

# Zones d'affichage
alert_placeholder = st.empty()
blocked_placeholder = st.empty()
alert_data = []

# Barre latérale : filtre + réinitialisation
with st.sidebar:
    st.subheader(" Filtrer les alertes")
    selected_ip = st.text_input("IP source (laisse vide pour tout afficher)", "")

# Lecture en continu (tail -f)
def tail_log(file_path):
    with file_path.open("r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line

# Lecture des IP bloquées depuis /tmp/blocked_ips.txt
def read_blocked_ips():
    if not BLOCKED_FILE.exists():
        return pd.DataFrame()
    with open(BLOCKED_FILE, "r") as f:
        ips = [line.strip() for line in f if line.strip()]
    df = pd.DataFrame({"IP bloquée": ips})
    return df.drop_duplicates().iloc[::-1].reset_index(drop=True)

# Boucle principale
for line in tail_log(LOG_FILE):
    try:
        data = json.loads(line)
        if "alert" in data:
            proto = data.get("proto", "").upper()
            uid = (
                data.get("timestamp", ""),
                data.get("src_ip", ""),
                data.get("src_port", ""),
                data.get("dest_ip", ""),
                data.get("dest_port", ""),
                proto
            )

            if uid not in st.session_state.seen:
                st.session_state.seen.add(uid)

                alert = {
                    "Horodatage": data.get("timestamp", ""),
                    "Protocole": proto,
                    "Source IP": data.get("src_ip", ""),
                    "Source Port": data.get("src_port", ""),
                    "Destination IP": data.get("dest_ip", ""),
                    "Destination Port": data.get("dest_port", ""),
                    "Message": data["alert"].get("signature", "")
                }

                alert_data.insert(0, alert)
                if len(alert_data) > 1000:
                    alert_data = alert_data[:1000]

                df_alerts = pd.DataFrame(alert_data)
                df_alerts["Horodatage"] = pd.to_datetime(df_alerts["Horodatage"], utc=True)
                df_alerts["Horodatage"] = df_alerts["Horodatage"].dt.tz_convert("Europe/Paris")

                # Tableau des alertes avec filtre IP
                with alert_placeholder.container():
                    st.subheader("Alertes Suricata en direct")
                    if selected_ip:
                        df_filtered = df_alerts[df_alerts["Source IP"].str.contains(selected_ip)]
                        st.dataframe(df_filtered, use_container_width=True)
                    else:
                        st.dataframe(df_alerts, use_container_width=True)

                # Tableau des IP bloquées
                df_blocked = read_blocked_ips()
                with blocked_placeholder.container():
                    st.subheader(" IP bloquées automatiquement")
    except json.JSONDecodeError:
        continue