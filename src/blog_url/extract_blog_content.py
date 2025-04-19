import requests
from bs4 import BeautifulSoup

def extract_blog_content(url):
    res = requests.get(url)
    print("res",res)
    soup = BeautifulSoup(res.content,"html.parser")
    paragraph = soup.find_all("p")
    content = "\n".join(p.get_text() for p in paragraph)
    return content.strip()