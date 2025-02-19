import requests
from bs4 import BeautifulSoup
import json
import logging

# Configure logging
logging.basicConfig(filename="scraper.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# URL (Chess.com forums don't have page numbers in URLs)
BASE_URL = "https://www.chess.com/forum/category/general?page="

# Number of pages to scrape
NUM_PAGES = 3

# List to store scraped Q&A data
chess_data = []

def scrape_chess_com(page_number):
    url = BASE_URL + str(page_number)
    logging.info(f"Fetching URL: {url}")
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
    except requests.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all forum threads
    threads = soup.select(".post-preview-title a")  # Updated CSS selector
    if not threads:
        logging.warning(f"No forum threads found on page {page_number}")
    
    for thread in threads:
        try:
            thread_title = thread.get_text(strip=True)
            thread_link = "https://www.chess.com" + thread["href"]

            logging.info(f"Scraping thread: {thread_title} ({thread_link})")

            # Fetch thread page
            thread_response = requests.get(thread_link, headers={"User-Agent": "Mozilla/5.0"})
            thread_soup = BeautifulSoup(thread_response.text, "html.parser")
            
            # Extract first response
            first_response = thread_soup.select_one(".post-content")  # Check if this class exists
            response_text = first_response.get_text(strip=True) if first_response else "No response found"

            chess_data.append({"question": thread_title, "answer": response_text})
            logging.info(f"✅ Scraped: {thread_title}")

        except Exception as e:
            logging.error(f"❌ Error scraping thread: {e}")

# Scrape multiple pages
for i in range(1, NUM_PAGES + 1):
    print(f"Scraping page {i} of Chess.com Forum...")
    scrape_chess_com(i)

# Save data
with open("chess_com_qa.json", "w", encoding="utf-8") as f:
    json.dump(chess_data, f, indent=4)

print("✅ Chess.com forum scraping complete! Check scraper.log for details.")
