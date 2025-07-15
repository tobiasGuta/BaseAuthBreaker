import argparse
import requests
import threading
import time
from queue import Queue

# Global queue for notifications
webhook_queue = Queue()

def check_basic_auth(url, webhook_enabled):
    try:
        response = requests.get(url, allow_redirects=False, timeout=5)
        if response.status_code == 401:
            www_auth = response.headers.get("WWW-Authenticate", "")
            if "Basic" in www_auth:
                print(f"[+] {url} requires Basic Authentication.")
                if webhook_enabled:
                    webhook_queue.put(url)
                return True
        print(f"[-] {url} does NOT require Basic Authentication.")
        return False
    except requests.RequestException as e:
        print(f"[!] Error checking {url}: {e}")
        return False

def send_discord_notification_loop(webhook_url):
    while True:
        url = webhook_queue.get()
        if url is None:
            break  # Sentinel to end the thread
        send_discord_notification(url, webhook_url)
        time.sleep(1.5)  # Rate limit to avoid hammering the webhook
        webhook_queue.task_done()

def send_discord_notification(url, webhook_url):
    data = {
        "content": f"🔐 Detected Basic Auth on: {url}"
    }
    try:
        response = requests.post(webhook_url, json=data, timeout=5)
        if response.status_code == 204:
            print(f"📬 Notification sent to Discord for: {url}")
        else:
            print(f"[!] Discord webhook responded with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"[!] Failed to send Discord notification: {e}")

def main():
    parser = argparse.ArgumentParser(description="Detect URLs requiring Basic Authentication, optionally notify via Discord")
    parser.add_argument("-u", "--urls", required=True, help="Path to file containing list of URLs to check")
    parser.add_argument("-w", "--webhook", help="Discord webhook URL to send notifications to (optional)")
    args = parser.parse_args()

    # Start notification thread if webhook provided
    if args.webhook:
        notif_thread = threading.Thread(target=send_discord_notification_loop, args=(args.webhook,), daemon=True)
        notif_thread.start()
    else:
        notif_thread = None

    with open(args.urls, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        check_basic_auth(url, webhook_enabled=bool(args.webhook))

    if args.webhook:
        webhook_queue.join()         # Wait until all tasks are sent
        webhook_queue.put(None)      # Send sentinel to end the thread
        notif_thread.join()

if __name__ == "__main__":
    main()
