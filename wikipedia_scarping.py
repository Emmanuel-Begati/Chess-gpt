import requests
from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# URL to scrape
url = "https://en.wikipedia.org/wiki/Chess"

# Function to fetch and save content
def fetch_chess_content(url):
    logging.info(f"Fetching content from URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        logging.info("Successfully retrieved the page")
        soup = BeautifulSoup(response.text, "html.parser")
        content = soup.find("div", {"class": "mw-parser-output"})
        if content:
            logging.info("Found the main content div")
            paragraphs = content.find_all("p")
            text_content = "\n".join([para.get_text() for para in paragraphs])
            with open("Chess.txt", "w", encoding="utf-8") as file:
                file.write(text_content)
            logging.info("Saved content for topic: Chess")
        else:
            logging.warning("Content not found for topic: Chess")
    else:
        logging.error(f"Failed to retrieve page for topic: Chess, status code: {response.status_code}")

# Fetch and save content for the topic
fetch_chess_content(url)



