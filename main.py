import requests
from bs4 import BeautifulSoup

file_name = "Proxies.txt"

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
    return proxies

def fetch_socks_proxies():
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
    return proxies

def main():
    print("Select a protocol (HTTPS, SOCKS4):")
    protocol = input().strip().upper()

    print("Select a country (two-letter ISO code, for example 'US', 'RU', 'IT') or 'ALL' for all:")
    country = input().strip().upper()

    if protocol not in ["HTTPS", "SOCKS4"]:
        print("Error: invalid protocol. Acceptable values: HTTPS, SOCKS4")
        return

    if protocol == "HTTPS":
        proxy_list = fetch_https_proxies()
        # format proxy_list(ip, port, country)
        result = []
        for ip, port, ctry in proxy_list:
            if country == "ALL" or ctry.upper() == country:
                result.append(f"{ip}:{port}")
    else:
        proxy_list = fetch_socks_proxies()
        # format proxy_list(ip, port, country, version)
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
        with open(file_name, "w") as f:
            for p in result:
                f.write(p + "\n")

        print(f"Total found: {len(result)} proxies\nProxy list saved to [ {file_name} ]")

if __name__ == "__main__":
    main()