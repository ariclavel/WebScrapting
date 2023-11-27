import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
from fake_useragent import UserAgent
import csv
from datetime import datetime

company_codes = ["AMZN", "AAPL", "TSLA", "META", "GOOG", "NFLX"]

# Search for amzn in https://finance.yahoo.com/lookup
# https://finance.yahoo.com/quote/amzn?p=amzn&.tsrc=fin-srch

# Create a UserAgent object to generate random user agents
user_agent = UserAgent()

# Specify the CSV file name
csv_filename = "finance_data_type_01.csv"


def scrape_yahoo_finance_data(code):
    data = {"Company": "N/A", "Stock Price": "N/A", "Stock Change": "N/A"}
    url = f"https://finance.yahoo.com/quote/{code}?p={code}&.tsrc=fin-srch"
    try:
        headers = {"User-Agent": user_agent.random}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            company_name_elem = soup.find("h1", class_="D(ib) Fz(18px)")
            stock_price_elem = soup.find(
                "fin-streamer", class_="Fw(b) Fz(36px) Mb(-4px) D(ib)"
            )
            stock_change_elem = soup.find(
                "fin-streamer", class_="Fw(500) Pstart(8px) Fz(24px)"
            )
            data["Company"] = company_name_elem.text if company_name_elem else "N/A"
            data["Stock Price"] = stock_price_elem.text if stock_price_elem else "N/A"
            data["Stock Change"] = (
                stock_change_elem.text if stock_change_elem else "N/A"
            )
        else:
            print(f"Failed to retrieve data for {code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {code}: {e}")
    return data


def save_to_csv(data, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Timestamp", "Company", "Stock Price", "Stock Change"])
        writer.writerow(
            (timestamp, data["Company"], data["Stock Price"], data["Stock Change"])
        )


def scrape_data_for_companies(company_codes, csv_filename):
    with ThreadPoolExecutor(max_workers=len(company_codes)) as executor:
        data = list(executor.map(scrape_yahoo_finance_data, company_codes))
        for item in data:
            save_to_csv(item, csv_filename)


while True:
    scrape_data_for_companies(company_codes, csv_filename)
    time.sleep(5)  # Wait for 5 minutes (5 seconds) before the next request