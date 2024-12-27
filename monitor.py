import subprocess
import requests

# List of IPs to monitor
IPS_TO_MONITOR = ["8.8.8.8", "1.1.1.1"]

# Telegram bot details
TELEGRAM_BOT_TOKEN = "bot7599220977:AAFN5IW6VPgU4bVRVvfYXCOwGlruHDXkcVQ"
TELEGRAM_CHAT_ID = "-4770635821"

def is_reachable(ip):
    try:
        # Ping the IP
        subprocess.check_output(["ping", "-c", "1", ip], stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError:
        return False

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, data=payload)

for ip in IPS_TO_MONITOR:
    if not is_reachable(ip):
        send_telegram_message(f"⚠️ IP {ip} is unreachable!")
