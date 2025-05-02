import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Define the URL to scrape
BASE_URL = "https://www.chess.com/forum/hot-topics"
response = requests.get(BASE_URL)

soup = BeautifulSoup(response.text, "html.parser")

# Extract forum questions and their answers
questions = soup.find_all("div", class_="forums-most-recent-item")
for question in questions:
    question_title = question.find("a", class_="forums-most-recent-title")
    question_user = question.find("a", class_="forums-most-recent-username")
    question_time = question.find("time").text.strip()
    
    if question_title and question_user:
        title = question_title.text.strip()
        user = question_user.text.strip()
        url = urljoin(BASE_URL, question_title['href'])
        print(f"Question: {title}\nUser: {user}\nTime: {question_time}\nURL: {url}\n")
        
        # Follow the link to the question page to extract answers
        question_response = requests.get(url)
        question_soup = BeautifulSoup(question_response.text, "html.parser")
        
        # Extract answers and find the one with the highest upvotes
        answers = question_soup.find_all("div", class_="comment-post-actions-component")
        top_answer = None
        max_upvotes = -1
        for answer in answers:
            answer_user = answer.find("a", class_="username")
            answer_text = answer.find("div", class_="post-message")
            upvotes = answer.find("span", class_="vote-container-count")  # Assuming upvotes are stored in a span with class 'vote-container-count'
            if answer_user and answer_text and upvotes:
                upvote_count = int(upvotes.text.strip())
                if upvote_count > max_upvotes:
                    max_upvotes = upvote_count
                    top_answer = (answer_user.text.strip(), answer_text.text.strip())
        
        if top_answer:
            answer_user_text, answer_text_content = top_answer
            print(f"Top Answer by {answer_user_text}: {answer_text_content}\nUpvotes: {max_upvotes}\n")