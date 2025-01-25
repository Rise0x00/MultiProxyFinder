import os
import requests
from bs4 import BeautifulSoup

FILE_NAME = "Proxies.txt"

def get_country_name(iso_code):
    response = requests.get(f"https://restcountries.com/v3.1/alpha/{iso_code}")
    if response.status_code == 200:
        country_data = response.json()
        return country_data[0]['name']['common']
    else:
        return False
    
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
    #print(proxies)
    return proxies

def fetch_socks5_proxies():
    url = "https://freeproxyupdate.com/socks5-proxy/"
    proxies = []

    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error to {url}: {e}")
        return False

    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find("table", class_="list-proxy")
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
        speed = cols[5].text.strip()
        proxies.append((ip, port, country, speed))
    # format proxy_list(ip, port, country, speed)   
    return proxies
def main():
    protocol = input("Select a protocol ([1] HTTPS, [2] SOCKS4), [3] SOCKS5: ").strip().upper()

    if protocol not in ["HTTPS", "SOCKS4", "SOCKS5", "1", "2", "3"]:
        print("Error: invalid protocol. Acceptable values: HTTPS, SOCKS4, SOCKS5")
        main()

    country = input("Select a country (two-letter ISO code, for example 'US', 'RU', 'IT') or 'ALL' for all: ").strip().upper()

    if protocol == "HTTPS" or protocol == "1":
        print("\nFetching HTTPS proxies...")
        proxy_list = fetch_https_proxies()
        result = []
        for ip, port, ctry in proxy_list:
            if country == "ALL" or ctry.upper() == country:
                result.append(f"{ip}:{port}")

    elif protocol == "SOCKS4" or protocol == "2":
        print("\nFetching SOCKS4 proxies...")
        proxy_list = fetch_socks4_proxies()
        result = []
        for ip, port, ctry, version in proxy_list:
            if version.lower() == "SOCKS4".lower():
                if country == "ALL" or ctry.upper() == country:
                    result.append(f"{ip}:{port}")

    elif protocol == "SOCKS5" or protocol == "3":
        print("\nFetching SOCKS5 proxies...")
        country_name = get_country_name(country)
        if not country_name:
            print(f"Error: invalid ISO code '{country}'.")
            return
        proxy_list = fetch_socks5_proxies()
        result = []
        for ip, port, ctry, speed in proxy_list:
            if speed.lower() == "fast":
                if country == "ALL" or ctry.lower() == country_name.lower():
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