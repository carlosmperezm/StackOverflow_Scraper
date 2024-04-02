""" Importing requests and BeautifulSoup modules"""
import requests
from bs4 import BeautifulSoup

URL: str = "https://stackoverflow.com"
QUESTIONS_URL: str = "https://stackoverflow.com/questions"
URL_PART: str = URL.split("//")
DOMAIN: str = URL_PART[1]
# Creating the list which will keep all data
data_list: list[str] = []

NAME:str = """
         __                 __                             _____ 
  _______/  |______    ____ |  | _________  __ ____________/ ____\\
 /  ___/\\   __\\__  \\ _/ ___\\|  |/ /  _ \\  \\/ // __ \\_  __ \\   __\\ 
 \\___ \\  |  |  / __ \\\\  \\___|    <  <_> )   /\\  ___/|  | \\/|  |   
/____  > |__| (____  /\\___  >__|_ \\____/ \\_/  \\___  >__|   |__|   
     \\/            \\/     \\/     \\/               \\/              
.__                 
|  |   ______  _  __
|  |  /  _ \\ \\/ \\/ /
|  |_(  <_> )     / 
|____/\\____/ \\/\\_/ 

 __      __      ___.    
/  \\    /  \\ ____\\_ |__  
\\   \\/\\/   // __ \\| __ \\ 
 \\        /\\  ___/| \\_\\ \\
  \\__/\\  /  \\___  >___  /
       \\/       \\/    \\/ 

  _________                                 .__                
 /   _____/ ________________  ______ ______ |__| ____    ____  
 \_____  \_/ ___\_  __ \__  \ \____ \\____ \|  |/    \  / ___\ 
 /        \  \___|  | \// __ \|  |_> >  |_> >  |   |  \/ /_/  >
/_______  /\___  >__|  (____  /   __/|   __/|__|___|  /\___  / 
        \/     \/           \/|__|   |__|           \//_____/                      

    S t a c k o v e r f l o w   W e b   S c r a p p i n g
"""


print('Welcome to:',NAME)

kw: str = input(
    f"Give us a keyword and we will find the first three posts with answers for you in {DOMAIN}: "
)


def find_questions(url: str, keyword: str) -> None:

    """Pass a word to works as keyword
    and will return the first three matches in stackoverflow's questions"""

    #  Getting current index page
    part_url = url.split("=")
    index_page = part_url[-1]
    # Creating a variable for button next link
    next_button_link: str = ""
    # Getting the page and transforming it to text
    page = requests.get(url, timeout=10)
    page_text = page.text
    # Creating the object SOUP from the BeautifulSoup class that we imported already
    SOUP = BeautifulSoup(page_text, "html.parser")
    # Getting th pagination items to get the link to go to next page
    PAGINATION_ITEMS = SOUP.select(".s-pagination--item")
    # Getting all the questions in a page
    QUESTIONS = SOUP.select(".s-post-summary")

    # if we are on page /questions we print number 1, else we print the pages numbers
    if "question" in index_page:
        print(f'Looking for a question with "{keyword}" in {DOMAIN} page number 1...')
    else:
        print(
            f'Looking for a question with "{keyword}" in {DOMAIN} page number {index_page}...'
        )
    #  Getting  question by question, and its title, link, we also get the username who posted the question
    for QUESTION in QUESTIONS:
        TITLE_QUESTION = QUESTION.select_one(".s-link").get_text()
        LINK_QUESTION = URL + QUESTION.select_one(".s-link")["href"]
        USER_NAME = QUESTION.select_one(".s-user-card--link").get_text()
        responses = QUESTION.select_one(".s-post-summary--stats-item-number").get_text()
        # Saving the data in a variable
        data: str = f"User👤: >{USER_NAME.strip()}<< Asks: ''{TITLE_QUESTION}''    link----> {LINK_QUESTION}"
        # If the keyword is in the question title and the question has any responses
        if " " + keyword + " " in TITLE_QUESTION and int(responses) > 0:
            # We add the data collected to the data list
            data_list.append(data)

    # Getting the link to go to the nex page
    for item in PAGINATION_ITEMS:
        if item.get_text().strip().lower() == "next":
            next_button_link = item["href"]

    next_url: str = URL + next_button_link

    if len(data_list) < 3:
        return find_questions(next_url, keyword)
    for count, _data in enumerate(data_list):
        print(f"{count+1}--{_data}")


find_questions(QUESTIONS_URL, kw.strip().lower())
