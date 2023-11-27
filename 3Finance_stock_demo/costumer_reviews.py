# Import required libraries
import requests
from bs4 import BeautifulSoup
import csv
#from user_agent import generate_user_agent
import time
import random
import hashlib
import MySQLdb

db = MySQLdb.connect(host="localhost",   
                     user="root",        
                     passwd="",  
                     db="rendezvous") 
query_apply = ("INSERT INTO reviews"
               "(user_id, heading, message, date_review, rating, date_experience)"
               "VALUES (%s,%s,%s,%s,%s,%s)")

 
#cur = db.cursor()
cur = db.cursor()
#csv
def save_to_bd():
    try:
        #print("done")
    
        for index, review in enumerate(reviews, start=1):
            data = (review['User_id'],review['Heading'],review['Message'],review['Date'],review['Rating'],review['Data_review'])
            print(data)
            cur.execute(query_apply, data)
            db.commit()
                        
        
    except ValueError:
        #print("oops")
        print(ValueError)

def save_to_csv(h):
    try:
        with open('reviews.csv', 'w', newline='') as csvfile:
            fieldnames = h
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            for index, review in enumerate(reviews, start=1): 
                writer.writerow(review)
            
    except ValueError:
        #print("oops")
        print(ValueError)


#Input url
trustpilot_urls = [
    "https://fr.trustpilot.com/review/www.doctolib.fr"
]


def get_reviews(url):
    try:
        # Create a user agent
        #user_agent = generate_user_agent()

        # Send a GET request with a user agent
        #headers = {"User-Agent": user_agent}
        response = requests.get(url)

        # Check if the request was successful
        response.raise_for_status()

        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        #Exctracting info last excercises
        #div class="styles_header__yrrqf"
        #new_elem = soup.find_all("div", class_="styles_header__yrrqf")
        new_elem = soup.find_all("span", class_="typography_heading-m__T_L_X typography_appearance-default__AAY17")[0]
        new_elem2 = soup.find_all("p", class_="typography_body-l__KUYFJ typography_appearance-default__AAY17")[0]
        new_elem3 = soup.find_all("p" ,class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_cell__qnPHy styles_labelCell__vLP9S" )
        new_elem4 = soup.find_all("p" ,class_="typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_cell__qnPHy styles_percentageCell__cHAnb" )
        new_elem5 = soup.find_all("span", class_="typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM")
        #print("aaaaaaaaaaa")
        
        #print(new_elem2.text.split())
        print("Company Name: ",new_elem5[0].text)
        print("Company Overall Rating:",new_elem.text)
        for i in range(0,len(new_elem3)):
            print(new_elem3[i].text, ": ",new_elem4[i].text)
        
        
        # Extract review information
        reviews = []
        # Input tag and class
        review_elements = soup.find_all("div", class_="styles_reviewCardInner__EwDq2")
    
        for review in review_elements:
            # Input functions, tag and class
            user = review.find(
                "span",
                class_="typography_heading-xxs__QKBS8",
            ).text
            #print(user)
            
            # Hash user
            user_id = int(hashlib.sha256(user.encode("utf-16")).hexdigest(), 16) % (10 ** 8)
            
            heading = review.find(
                "h2",
                class_="typography_heading-s__f7029 typography_appearance-default__AAY17",
            ).text
            
            message = review.find(
                "p",
                class_="typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn",
            )
            if not message:
                message=""
            else:
                message = message.text
            date = review.find(
                "time"
            ).text
            rating = review.find(
                "div",
                class_='star-rating_starRating__4rrcf star-rating_medium__iN6Ty'
            ).img['alt']
            date_review = review.find(
                "p",
                class_ ="typography_body-m__xgxZ_ typography_appearance-default__AAY17" 
            ).text
            date_review = date_review.split(":")[1]
            reviews.append(
                {
                    "User_id": user_id,
                    "Heading": heading,
                    "Message": message,
                    "Date": date,
                    "Rating": rating,
                    "Data_review": date_review
                }
            )
            
        return reviews

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page {url}. Exception: {e}")
        return None


if __name__ == "__main__":
    for url in trustpilot_urls:
        print(f"\nScraping reviews for {url}")
        # Input url
        #reviews = get_reviews('https://fr.trustpilot.com/review/www.doctolib.fr')

        
        #Input url
        base_url = "?"
        num_pages = 1  # Set the desired number of pages to scrape the data

        #Input base url and page
        for page in range(1, num_pages + 1):
            # Input base url and page
            page_url = f"{url}?page={page}"
            print(f"\nScraping reviews for {page_url}")

            # Introduce a random delay between 5 and 15 seconds
            delay_seconds = random.uniform(5, 15)
            time.sleep(delay_seconds)

            reviews = get_reviews(page_url)

            # Input reviews to enumerate
            # Input reviews
            if reviews:
                for index, review in enumerate( reviews, start=1):
                    print("holi")
                    """print(f"\nReview #{index}:")
                    print(f"Userid: {review['User_id']}")
                    print(f"Heading: {review['Heading']}")
                    print(f"Message: {review['Message']}")
                    print(f"Date: {review['Date']}")
                    print(f"Rating: {review['Rating']}")
                    print(f"Data review: {review['Data_review']}")"""
            else:
                print(f"No reviews found for {url}")
        #save_to_bd()
        h = []
        for key in reviews[0].keys():
            #print(key)
            h.append(key)
       
        save_to_csv(h)
        
    
