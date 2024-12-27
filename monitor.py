import subprocess
import requests
import os
import socket

# List of IPs to monitor
IPS_TO_MONITOR = ["8.8.8.8", "1.1.1.1","192.168.1.10","110.74.212.129"]

# Telegram bot details
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Load from environment variable
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # Load from environment variable

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise EnvironmentError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set in the environment.")

def is_reachable(ip, port=80):
    """
    Check if the IP is reachable by attempting a TCP connection on the specified port (default is 80).
    """
    try:
        sock = socket.create_connection((ip, port), timeout=5)
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False

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
