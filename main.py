import os
import requests
from bs4 import BeautifulSoup

FILE_NAME = "Proxies.txt"

def fetch_https_proxies():
    url = "https://free-proxy-list.net/"
    proxies = []

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error to {url}: {e}")
        return False

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("div", class_="table-responsive fpl-list")
    if not table:
        print(f"The proxy table was not found on [ {url} ]")
        return False

    rows = table.tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 8:
            continue
        ip = cols[0].text.strip()
        port = cols[1].text.strip()
        country = cols[2].text.strip()
        is_https = cols[6].text.strip().lower() == "yes"
        if is_https:
            proxies.append((ip, port, country))
    # format proxy_list(ip, port, country)
    return proxies

def fetch_socks4_proxies():
    url = "https://www.socks-proxy.net/"
    proxies = []

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error to {url}: {e}")
        return False

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("div", class_="table-responsive fpl-list")
    if not table:
        print(f"The proxy table was not found on [ {url} ]")
        return False

    rows = table.tbody.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 8:
            continue
        ip = cols[0].text.strip()
        port = cols[1].text.strip()
        country = cols[2].text.strip()
        version = cols[4].text.strip()
        proxies.append((ip, port, country, version))
    # format proxy_list(ip, port, country, version)    
    return proxies

def main():
    protocol = input("Select a protocol ([1] HTTPS, [2] SOCKS4): ").strip().upper()

    if protocol not in ["HTTPS", "SOCKS4", "1", "2"]:
        print("Error: invalid protocol. Acceptable values: HTTPS, SOCKS4")
        main()

    country = input("Select a country (two-letter ISO code, for example 'US', 'RU', 'IT') or 'ALL' for all: ").strip().upper()

    if protocol == "HTTPS" or "1":
        print("\nFetching HTTPS proxies...")
        proxy_list = fetch_https_proxies()
        result = []
        for ip, port, ctry in proxy_list:
            if country == "ALL" or ctry.upper() == country:
                result.append(f"{ip}:{port}")

    elif protocol == "SOCKS4" or "2":
        print("\nFetching SOCKS4 proxies...")
        proxy_list = fetch_socks4_proxies()
        result = []
        for ip, port, ctry, version in proxy_list:
            if version.lower() == protocol.lower():
                if country == "ALL" or ctry.upper() == country:
                    result.append(f"{ip}:{port}")

    print(f"\nFound proxies: {len(result)}\n")

    for proxy in result:
        print(proxy)

    if not result:
        print("No proxies found.")
        return
    else:
        with open(FILE_NAME, "w") as f:
            for p in result:
                f.write(p + "\n")

        print(f"Total found: {len(result)} proxies\nProxy list saved to [ {os.path.abspath(FILE_NAME)} ]")

if __name__ == "__main__":
    main()