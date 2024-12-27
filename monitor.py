import subprocess
import requests
import os

# List of IPs to monitor
IPS_TO_MONITOR = ["8.8.8.8", "1.1.1.1"]

# Telegram bot details
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

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
