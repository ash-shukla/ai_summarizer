import requests
from bs4 import BeautifulSoup
import time
import streamlit as st

def extract_blog_content(url):
    res = requests.get(url)
    print("res",res)
    soup = BeautifulSoup(res.content,"html.parser")
    paragraph = soup.find_all("p")
    content = "\n".join(p.get_text() for p in paragraph)
    st.toast("Fetching blog content... please ask any question related to the blog",icon="✅")
    time.sleep(1)
    return content.strip()