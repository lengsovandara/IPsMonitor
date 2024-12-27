import subprocess
import requests
import os
import socket

# List of IPs to monitor
IPS_NAME_MONITOR = ["DC_EZECOM","DC_NTC","DC_SINET","DC_MEKONG"]
IPS_TO_MONITOR = ["110.74.212.129","202.124.33.129","136.228.128.1","100.65.0.3","100.65.0.4"]

# Telegram bot details
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Load from environment variable
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # Load from environment variable

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise EnvironmentError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set in the environment.")

def is_reachable(ip):
    """
    Check if the IP is reachable using nslookup (DNS lookup).
    """
    try:
        # Execute nslookup to check if the DNS server is responding
        result = subprocess.run(
            ["nslookup", ip],
            check=True,  # Raise error if nslookup fails
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True  # If nslookup succeeds, the IP is reachable
    except subprocess.CalledProcessError:
        return False  # If nslookup fails, the IP is unreachable

def send_telegram_message(message):
    """
    Send a message to a Telegram chat using the Telegram bot.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"Failed to send Telegram message: {response.text}")

def main():
    """
    Monitor the IPs and send an alert if any IP is unreachable.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Telegram bot token or chat ID not set.")
        return

    for ip in IPS_TO_MONITOR:
        if not is_reachable(ip):
            message = f"⚠️ Alert: IP {ip} is unreachable!"
            print(message)  # Log message to console
            send_telegram_message(message)

if __name__ == "__main__":
    main()
