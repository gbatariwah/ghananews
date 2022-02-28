import requests
from bs4 import BeautifulSoup


def fetch_page(url):
    response = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }, timeout=5)

    response.close()
    html = response.text

    soup = BeautifulSoup(html, 'lxml')

    return soup
