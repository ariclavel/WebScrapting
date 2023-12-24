import requests
from bs4 import BeautifulSoup
#from user_agent import generate_user_agent
import time
import random
import sqlite3

# Set the base URL
base_url = "https://www.residences-immobilier.com/en/search.html?lang=EN&tri=RELEVANCE&keywords=&fromGG=&TypeAnnonce=VEN&TypeBien=&departement=75&district=&villes=&bdgMin=&bdgMax=&surfMin=&surfMax=&nb_piece=&keywords="

# Number of pages to scrape
num_pages = 30  # Adjust as needed

# Function to create a SQLite database and table
def create_database():
    conn = sqlite3.connect("house_listing_dbase.db")
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS house_listing (
            property_type TEXT,
            place TEXT,
            price TEXT
        )
    ''')

    conn.commit()
    conn.close()

# Function to insert data into the SQLite database
def insert_into_database(property_type, place, price):
    conn = sqlite3.connect("house_listing_dbase.db")
    cursor = conn.cursor()

    # Insert data into the table
    cursor.execute('''
        INSERT INTO house_listing (property_type, place, price)
        VALUES (?, ?, ?)
    ''', (property_type, place, price))

    conn.commit()
    conn.close()

# Function to scrape data from a single page
def scrape_page(url):
    #agent = generate_user_agent()
    #headers = {"User-Agent": agent}
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("div", class_="row no-gutters px-3 px-sm-0")
        for row in rows:
            # Find the value inside the span with itemprop "name"
            property_type_elem = row.find("span", itemprop="name")
            property_type = property_type_elem.text.strip() if property_type_elem else "N/A"
            
            # Find the value of class "hthin ville"
            place_elem = row.find("span", class_="hthin ville")
            place = place_elem.text.strip() if place_elem else "N/A"

            # Find the price Span with class "prix"
            price_elem = row.find("span", class_="prix")
            price = price_elem.text.strip() if price_elem else "N/A"

            # Insert data into SQLite database
            insert_into_database(property_type, place, price)
        wait_time = end_time - start_time
        print(f"Waiting Time: {wait_time:.2f} seconds")

    else:
        print(f"Failed to retrieve page. Status code: {response.status_code}")


# Create the SQLite database and table
create_database()

# Iterate through pages
for page_num in range(1, num_pages + 1):
    page_url = f"{base_url}&page={page_num}"

    # Scrape data from the page and save to SQLite database
    scrape_page(page_url)

    # Wait for a random time (between 10 and 30 seconds) before making the next request
    wait_time = random.uniform(10, 30)
    
    print(f"Data appended to the database file")
    print(f"Waiting for {wait_time:.2f} seconds before the next request...")
    time.sleep(wait_time)
