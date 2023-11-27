from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
import time
from concurrent.futures import ThreadPoolExecutor
import MySQLdb

db = MySQLdb.connect(host="localhost",   
                     user="root",        
                     passwd="",  
                     db="rendezvous")        
#cur = db.cursor()
cur = db.cursor()
add_yahoo = ("INSERT INTO yahoo"
               "(pre_close, op, bid, mark, day_range, week_range, volume, avg_volume, market, beta, pe, eps, earnings_date, forward, exdividend, target_est, company, timestamp_) "
               "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")

company_codes = ["AMZN", "AAPL", "TSLA", "META", "GOOG", "NFLX"]

import csv
from datetime import datetime

# Search for amzn in https://finance.yahoo.com/lookup
# https://finance.yahoo.com/quote/amzn?p=amzn&.tsrc=fin-srch

# Create a UserAgent object to generate random user agents
user_agent = UserAgent()
h = []
r = []
header = False
def save_to_csv(data):
    # If required milli-seconds
    print(data)
    # field names  
    
    fields = h 
    
    # data rows of csv file  
    rows = data
        
    # name of csv file  
    filename = "university_records.csv"
        
    # writing to csv file  
    with open(filename, 'w') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
            
        # writing the fields  
        if csvfile.tell() == 0:
            csvwriter.writerow(fields)  
            
        # writing the data rows  
        csvwriter.writerows(rows) 


def scrape_yahoo_finance_data(code):
    url = f"https://finance.yahoo.com/quote/{code}?p={code}&.tsrc=fin-srch"
    try:
        headers = {"User-Agent": user_agent.random}  # Randomly select a user agent
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract relevant data
            #company_name_elem = soup.find("h1", class_="D(ib) Fz(18px)")
            values = soup.find_all("td", class_="Ta(end) Fw(600) Lh(14px)")
            labels = soup.find_all("td", class_="C($primaryColor) W(51%)")
            dummy = []
            
            if (len(labels) > 0) and (len(values) > 0):
                #r.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
                
                for label, value in zip(labels, values):
                                
                    l = label.text.strip()
                    v = value.text.strip()
                    #print(l, ": ", v) 
                    if(len(h)<=15):
                        h.append(l)
                    if(len(h) == 16):
                        h.append("Company Name")
                        h.append("timestamp")
                        

                    
                    dummy.append(v) 
                dummy.append(code)
                today = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                dummy.append(today)
                #inserting some values
                print(len(dummy))
                
                #cur.execute("SELECT * FROM esc1_apointments")
                r.append(dummy)
                #print(r)
                save_to_csv(r)
                print("-----------------------------------------------------------")
                try:
                    #print("done")
                    data = (float(dummy[0]),float(dummy[1]),dummy[2],dummy[3],dummy[4],dummy[5],dummy[6],dummy[7],dummy[8], float(dummy[9]),float(dummy[10]),float(dummy[11]),dummy[12],dummy[13],dummy[14],float(dummy[15]),dummy[16],dummy[17])
                    print(data)
                    db.commit()
                    
                    cur.execute(add_yahoo, data)
                except ValueError:
                    #print("oops")
                    print(ValueError)

           
            
        else:
            print(f"Failed to retrieve data for {code}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {code}: {e}")


def scrape_data_for_companies(company_codes):
    with ThreadPoolExecutor(max_workers=len(company_codes)) as executor:
        executor.map(scrape_yahoo_finance_data, company_codes)

"""
while True:
    scrape_data_for_companies(company_codes)
    time.sleep(5)  # Wait for 5 seconds before the next request
"""

scrape_data_for_companies(company_codes)
time.sleep(5)  # Wait for 5 seconds before the next request


db.close()