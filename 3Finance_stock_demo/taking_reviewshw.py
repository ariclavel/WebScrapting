# Import required libraries
import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import hashlib

# Extract review information
reviews_sb = []
h = []
def save_to_csv(h):
    try:
        with open('reviews_hw.csv', 'w', encoding='utf-16', newline='') as csvfile:
            fieldnames = h
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
            if csvfile.tell() == 0:
                writer.writeheader()
            for index, review in enumerate(reviews_sb, start=1): 
                print(review)
                writer.writerow(review)
            
    except ValueError:
        print(ValueError.text())


#Input url
trustpilot_urls = [
    "https://www.babelio.com/livres/Flaubert-Madame-Bovary/894329/critiques"
]


def get_reviews(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser",from_encoding='utf-16')
        review_elements = soup.find_all("div", class_="post post_con" )
        reviews = []
        #print(review_elements[0])
        
        
        for review in review_elements:
            # Input functions, tag and class
            user = review.find(
                "a",
                class_="lien_croco",
            ).text
            user_id = int(hashlib.sha256(user.encode("utf-16")).hexdigest(), 16) % (10 ** 8)
            
           
            message = review_elements[0].find(
                "div",
                class_="cri_corps_critique shrinkable text br_150_de_hauteur",
            )
            if not message:
                message=""
            else:
                message = message.text

            date = review.find(
                "span",
                class_="gris",
            )
            if not date:
                date=""
            else:
                date = date.text
            rating = review.find(
                attrs={'itemprop': 'ratingValue' }  
            )['content']
            reviews.append(
                {
                    "User_id": user_id,
                    "Message": message,
                    "Date": date,
                    "Rating": rating
                }
            )
            reviews_sb.append(
                {
                    "User_id": user_id,
                    "Message": message,
                    "Date": date,
                    "Rating": rating
                }
            )
            

            
        return reviews

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve page {url}. Exception: {e}")
        return None


if __name__ == "__main__":
    for url in trustpilot_urls:
        base_url = "?"
        num_pages = 2
        #179
        for page in range(1, num_pages + 1):
            page_url = f"{url}?page={page}"
            print(f"\nScraping reviews for {page_url}")
            delay_seconds = random.uniform(0.1, 1)
            time.sleep(delay_seconds)

            reviews = get_reviews(page_url)
            #save_to_csv(reviews,h)
            # Input reviews
            if reviews:
                #reviews_sb.append(reviews)
                print(f"\nlength {len(reviews)}:")
                """for index, review in enumerate( reviews, start=1):
                    print(f"\nReview #{index}:")
                    print(f"Userid: {review['User_id']}")
                    print(f"Heading: {review['Heading']}")
                    print(f"Message: {review['Message']}")
                    print(f"Date: {review['Date']}")
                    print(f"Rating: {review['Rating']}")
                    print(f"Data review: {review['Data_review']}")"""
                   
            else:
                print(f"No reviews found for {url}")

        
        for key in reviews_sb[0].keys():
            h.append(key)
        print(h)
        save_to_csv(h)
        
        
        