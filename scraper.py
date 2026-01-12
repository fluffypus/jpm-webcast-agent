import requests
from bs4 import BeautifulSoup

def fetch_page(url):
    headers = {"User-Agent": "JPM-Webcast-Agent/1.0"}
    r = requests.get(url, timeout=15, headers=headers)
    r.raise_for_status()
    return r.text

def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ").lower()

def extract_links(html):
    soup = BeautifulSoup(html, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]
