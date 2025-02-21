import requests
from bs4 import BeautifulSoup
import logging

def fetch_and_preprocess_content(url):

    headers = {"User-Agent": "Mozilla/5.0"}  # Avoids bot detection
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch webpage: {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract all paragraphs
    paragraphs = [p.get_text().strip() for p in soup.find_all("p")]
    content = " ".join(paragraphs)

    # Basic cleaning
    content = content.replace("\n", " ").strip()
    
    if not content:
        raise ValueError("No content extracted from the page.")

    logging.info(f"Extracted {len(content.split())} words.")
    
    return content
