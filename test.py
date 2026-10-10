import requests
from bs4 import BeautifulSoup

r = requests.get("https://books.toscrape.com", timeout=10)
sopa = BeautifulSoup(r.text, "html.parser")
print(sopa.title.text.strip())
print(r.status_code)