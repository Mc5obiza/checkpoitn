import requests
import json
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import re
def search(query,num = 5):

    load_dotenv()
    serper_api = os.getenv("SERPER_API_KEY")

    url = "https://google.serper.dev/search"
    header = {
        "X-API-KEY":serper_api,
        "Content-Type" : "application/json"
    }
    payloads = json.dumps({
        "q":query,
        "num":num,
        "gl":"us",
        "hl":"en"
    })
    try:
        response =  requests.post(url=url,headers=header,data=payloads)
        response.raise_for_status()
        search_data = response.json()
        return search_data.get("organic",[])

    except requests.exceptions.RequestException as e:
        return (f"An error occurred: {e}")

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    noise_tag = ["script","style","header","footer","nav","aside","form"]
    for tag in soup(noise_tag):
        tag.decompose()
    raw = soup.get_text(separator=" ")
    clean_text = re.sub(r'\s+', ' ', raw).strip()

    return clean_text