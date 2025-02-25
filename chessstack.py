import requests
from bs4 import BeautifulSoup
import json
import itertools

# Define the URL to scrape
BASE_URL = "https://chess.stackexchange.com/questions?tab=votes&pagesize=50"

# Number of pages to scrape
NUM_PAGES = 627

# List to store scraped Q&A data
chess_data = []

# List of user agents to cycle through
USER_AGENTS = [
    # Chrome
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    # Firefox
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    # Safari
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.172",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 OPR/78.0.4093.112"
]

# Create an iterator to cycle through the user agents
user_agent_cycle = itertools.cycle(USER_AGENTS)

def scrape_page(page_number, user_agent):
    url = BASE_URL + str(page_number)
    response = requests.get(url, headers={"User-Agent": user_agent})
    
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
            answer_response = requests.get(question_link, headers={"User-Agent": user_agent})
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
for i in range(190, NUM_PAGES + 1):
    if (i - 190) % 2 == 0:
        user_agent = next(user_agent_cycle)
    print(f"Scraping page {i} with user agent: {user_agent}")
    scrape_page(i, user_agent)

# Save scraped data to JSON
try:
    with open("chess_qa.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)
except FileNotFoundError:
    existing_data = []

existing_data.extend(chess_data)

with open("chess_qa.json", "w", encoding="utf-8") as f:
    json.dump(existing_data, f, indent=4)

print("✅ Scraping complete! Data saved to chess_qa.json")