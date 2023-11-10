import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent

company_codes = ["AMZN", "AAPL", "TSLA", "META", "GOOG", "NFLX"]

# Search for amzn in https://finance.yahoo.com/lookup
# https://finance.yahoo.com/quote/amzn?p=amzn&.tsrc=fin-srch

# Create a UserAgent object to generate random user agents
user_agent = UserAgent()


def scrape_yahoo_finance_data(code):
    url = f"https://finance.yahoo.com/quote/{code}?p={code}&.tsrc=fin-srch"
    try:
        headers = {"User-Agent": user_agent.random}  # Randomly select a user agent
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract relevant data
            company_name_elem = soup.find("h1", class_="D(ib) Fz(18px)")
            stock_price_elem = soup.find(
                "fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)"
            )
            stock_change_elem = soup.find(
                "fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)"
            )

            # Get company name, stock price, and stock change
            company_name = company_name_elem.text if company_name_elem else "N/A"
            stock_price = stock_price_elem.text if stock_price_elem else "N/A"
            stock_change = stock_change_elem.text if stock_change_elem else "N/A"

            print(f"Company: {company_name}")
            print(f"Stock Price: {stock_price}")
            print(f"Stock Change: {stock_change}")
        else:
            print(f"Failed to retrieve data for {code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {code}: {e}")


def scrape_data_for_companies(company_codes):
    with ThreadPoolExecutor(max_workers=len(company_codes)) as executor:
        executor.map(scrape_yahoo_finance_data, company_codes)


while True:
    scrape_data_for_companies(company_codes)
    time.sleep(5)  # Wait for 5 seconds before the next request
