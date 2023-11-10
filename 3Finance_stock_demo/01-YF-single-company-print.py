import requests
from bs4 import BeautifulSoup
import time

company_codes = ["AMZN"]

# Search for amzn in https://finance.yahoo.com/lookup
# https://finance.yahoo.com/quote/amzn?p=amzn&.tsrc=fin-srch

def scrape_yahoo_finance_data(code):
    url = f"https://finance.yahoo.com/quote/{code}?p={code}&.tsrc=fin-srch"
    try:
        response = requests.get(
            url, timeout=5
        )  # Add a 5-second timeout for the request
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            company_name_elem = soup.find("h1", class_="D(ib) Fz(18px)")
            stock_price_elem = soup.find(
                "fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)"
            )
            stock_change_elem = soup.find(
                "fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)"
            )

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


while True:
    for code in company_codes:
        scrape_yahoo_finance_data(code)
    time.sleep(5)  # Wait for 5 seconds before the next request
