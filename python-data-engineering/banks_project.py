import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3
#
def log_progress(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} : {message}\n"
    with open("code_log.txt", "a") as f:
        f.write(log_entry)
log_progress("Preliminaries complete. Initiating ETL process")
#
url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
csvpath = './Largest_banks_data.csv'
xrate = './exchange_rate.csv'
dbnm = 'Banks.db'
tblnm = 'Largest_banks'
tablattr = ["Name", "MC_USD_Billion"]
count = 0
#
def extract(url, tablattr):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all('table')
    table = tables[0]
    tbody = table.find('tbody')
#
    data = []
#
    for row in tbody.find_all('tr'):
        columns = row.find_all('td')
        if len(columns) > 1:
            name = columns[1].get_text(strip=True)
            market_cap = columns[2].get_text(strip=True).replace(',', '')
            data.append((name, market_cap))
    df = pd.DataFrame(data, columns=tablattr)
    return df
df = extract(url, tablattr)
#print(df)
def transform(df, xrate):
    xratedf = pd.read_csv(xrate)
    xratedict = xratedf.set_index('Currency').to_dict()['Rate']
    df['MC_USD_Billion'] = pd.to_numeric(df['MC_USD_Billion'], errors='coerce')
    df['MC_GBP_Billion'] = [np.round(x * xratedict['GBP'], 2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x * xratedict['EUR'], 2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x * xratedict['INR'], 2) for x in df['MC_USD_Billion']]

    return df
df = transform(df, xrate)
#print('Market cap of the 5th largest bank: ' + str(df['MC_EUR_Billion'][4]))
def load_to_csv(df, csvpath):
    df.to_csv(csvpath, index=False)
    log_progress("Transformed data successfully saved to CSV.")
load_to_csv(df, csvpath)
#
def load_to_db(df, conn, tblnm):
    df.to_sql(tblnm, conn, if_exists='replace', index=False)
    log_progress(f"Transformed data successfully loaded to table '{tblnm}' in the database.")
conn = sqlite3.connect(dbnm)
load_to_db(df, conn, tblnm)
#
conn.commit()
conn.close()

def run_queries(query, conn):
    cursor = conn.cursor()
    cursor.execute(query)
    output = cursor.fetchall()
#    
    print(f"\n\n\nYour Query, Sire:\n{query}")
    print("\nOutput for said query... good sir:")
    for row in output:
        print(row)
#
    log_progress(f"Executed query: {query}")
#
conn = sqlite3.connect(dbnm)
#
query_1 = "SELECT * FROM Largest_banks"
run_queries(query_1, conn)
#
query_2 = "SELECT AVG(MC_GBP_Billion) FROM Largest_banks"
run_queries(query_2, conn)
#
query_3 = "SELECT Name from Largest_banks LIMIT 5"
run_queries(query_3, conn)
#
conn.close()
