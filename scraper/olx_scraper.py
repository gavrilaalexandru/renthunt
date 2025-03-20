import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from config import BASE_URL, HEADERS, REQUEST_DELAY, OUTPUT_FILE


def get_page_url(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retreive page: {url}")
        return None
