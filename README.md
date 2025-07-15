# BaseAuthBreaker
BaseAuthBreaker is a Python tool that brute forces Basic Authentication using raw HTTP requests. It supports proxies like Burp Suite and provides clear, colorful terminal output for easy debugging.

# BaseAuthBreaker

A no-frills Python Basic Authentication brute force tool designed for pentesters and bug bounty hunters.

---

## Features

- Supports raw HTTP request files  
- Works with proxies like Burp Suite (`--proxy` flag)  
- Colorful, easy-to-read console output  
- Lightweight and simple  focus on effectiveness

---

## Requirements

- Python 3.6+  
- `requests` library  
- `colorama` library

Install dependencies with:

```bash
pip install requests colorama
```

# Usage
```bash
python baseauthbreaker.py -r /path/to/request.txt -w /path/to/wordlist.txt -p "admin:" --proxy
```

### Arguments:

| Flag | Description | Required | Example |
| --- | --- | --- | --- |
| `-r` | Path to raw HTTP request file | Yes | `request.txt` |
| `-w` | Path to password wordlist file | Yes | `passwords.txt` |
| `-p` | Prefix for each wordlist entry (optional) | No | `"admin:"` |
| `--proxy` | Route requests through proxy (127.0.0.1:8080) for Burp Suite (optional) | No | `--proxy` |

Example raw HTTP request file (`request.txt`)
```bash
GET /labs/basic_auth/ HTTP/1.1
Host: example.com
Cache-Control: max-age=0
Authorization: Basic <credentials>
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
```

Notes
-----

-   This tool is intended for authorized testing only.

-   Disabling SSL verification (`verify=False`) is intentional to work with Burp Suite's self-signed certs.

-   Use responsibly.

# Example

<img width="1640" height="446" alt="image" src="https://github.com/user-attachments/assets/af9aba82-bae6-4c1c-94ec-ec5f2e32b4c7" />

<img width="1695" height="372" alt="image" src="https://github.com/user-attachments/assets/8d977c8a-a05f-43ea-8fbf-863b87006082" />

# Second Tool 

<img width="765" height="108" alt="image" src="https://github.com/user-attachments/assets/331b1813-5aa2-49d6-88d7-104d342142ad" />

