import requests
from bs4 import BeautifulSoup
import json

# Define the URL to scrape
BASE_URL = "https://chess.stackexchange.com/questions?tab=Votes&page="

# Number of pages to scrape
NUM_PAGES = 627

# List to store scraped Q&A data
chess_data = []

def scrape_page(page_number):
    url = BASE_URL + str(page_number)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page_number}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    questions = soup.select(".s-post-summary")

    for q in questions:
        try:
            question_text = q.select_one(".s-link").get_text(strip=True)
            question_link = "https://chess.stackexchange.com" + q.select_one(".s-link")["href"]
            
            # Fetch the question page for answers
            answer_response = requests.get(question_link, headers={"User-Agent": "Mozilla/5.0"})
            answer_soup = BeautifulSoup(answer_response.text, "html.parser")
            
            # Get the top accepted answer
            answer = answer_soup.select_one(".js-post-body")
            answer_text = answer.get_text(strip=True) if answer else "No answer found"

            # Store in dictionary
            chess_data.append({"question": question_text, "answer": answer_text})
            print(f"✅ Scraped: {question_text}")

        except Exception as e:
            print(f"❌ Error scraping a question: {e}")

# Scrape multiple pages
for i in range(1, NUM_PAGES + 1):
    print(f"Scraping page {i}...")
    scrape_page(i)

# Save scraped data to JSON
with open("chess_qa.json", "w", encoding="utf-8") as f:
    json.dump(chess_data, f, indent=4)

print("✅ Scraping complete! Data saved to chess_qa.json")
