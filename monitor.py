import subprocess
import requests
import os
import socket

# List of IPs to monitor
#ISP_NAME_MONITOR = ["DC_EZECOM","DC_NTC","DC_SINET","DC_MEKONG","DR_MEKONG"]
#IPS_TO_MONITOR = ["110.74.212.129","202.124.33.129","136.228.128.1","100.65.0.3","38.47.36.157"]

ISP_NAME_MONITOR = ["DC_EZECOM","DC_NTC","DC_SINET"]
IPS_TO_MONITOR = ["110.74.212.129","202.124.33.129","136.228.128.1"]

# Telegram bot details
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Load from environment variable
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")      # Load from environment variable

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    raise EnvironmentError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set in the environment.")
    
# Execute nslookup to check if the DNS server is responding
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
# Execute ping to check if the IP is responding
def is_reachable_ping_callback(ip):
    """
    Check if the IP is reachable by trying to make an HTTP request first, fallback to ping.
    """
    try:
        # Test HTTP reachability (faster and more reliable in cloud environments)
        response = requests.get(f"http://{ip}", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        # Fallback to ping if HTTP fails
        try:
            subprocess.run(["ping", "-c", "1", "-W", "1", ip], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False
# Execute tcp to check if the IP is responding
def is_reachable_tcp(ip, port=80):
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
        
    i = 0
    while i < len(IPS_TO_MONITOR):
        if not is_reachable(IPS_TO_MONITOR[i]):
            message = f"⚠️ Alert: {ISP_NAME_MONITOR[i]} IP {IPS_TO_MONITOR[i]} is unreachable!"
            print(message)  # Log message to console        
            send_telegram_message(message)
        i +=1

if __name__ == "__main__":
    main()
