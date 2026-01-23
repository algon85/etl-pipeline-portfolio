![Python](https://img.shields.io/badge/python-3.x-blue)
![License](https://img.shields.io/badge/license-MIT-green)
# Automated ETL Pipeline: Global Bank Market Capitalization

This project is what I submitted as a "Final Project" assignment to obtain my IBM Python Project for Data Engineering Certificate. 
It implements an end-to-end **ETL (Extract, Transform, Load)** pipeline in Python that collects real-world financial data, enriches it with currency conversions, and loads it to both CSV and SQLite formats for downstream analysis.

The pipeline is designed with **modularity, logging, and data integrity** in mind, simulating a lightweight production-style workflow.

---

## 📌 Project Overview

**Data Source**
- Archived Wikipedia page listing the world's largest banks by market capitalization

**Pipeline Stages**
1. **Extract** – Scrapes structured HTML data using BeautifulSoup
2. **Transform** – Cleans numeric fields and converts USD values into multiple currencies
3. **Load** – Persists transformed data to:
   - CSV file
   - SQLite database
4. **Query** – Executes validation and analytical SQL queries
5. **Log** – Records progress and operations with timestamps

---

## 🛠 Technologies Used

- **Python 3**
- **Libraries**
  - `requests`
  - `BeautifulSoup4`
  - `pandas`
  - `numpy`
  - `sqlite3`
- **Data Storage**
  - CSV
  - SQLite

---

## 📂 Project Structure

```text
├── banks.py
├── exchange_rate.csv
├── Largest_banks_data.csv
├── Banks.db
├── code_log.txt
└── README.md
```


---

## ⚙️ ETL Workflow

### 1. Extract
- Fetches HTML from an archived Wikipedia page
- Parses the largest banks table
- Extracts:
  - Bank name
  - Market capitalization (USD)

### 2. Transform
- Converts market capitalization to numeric values
- Applies exchange rates from `exchange_rate.csv`
- Generates new columns:
  - `MC_GBP_Billion`
  - `MC_EUR_Billion`
  - `MC_INR_Billion`
- Rounds values for readability

### 3. Load
- Saves transformed data to CSV
- Loads data into a SQLite database table
- Replaces existing data to maintain consistency

### 4. Query
Executes example SQL queries including:
- Full table retrieval
- Average market capitalization (GBP)
- Top 5 banks by row order

---

## 🧾 Logging

All major pipeline steps and queries are logged with timestamps in `code_log.txt`, enabling:
- Execution traceability
- Debugging
- Basic operational monitoring

---

## 🚀 How to Run

```bash
pip install requests beautifulsoup4 pandas numpy
python banks.py

