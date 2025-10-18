import pandas as pd
import numpy as np
from datetime import datetime
import os

# === Setup ===
base_path = r"C:\Users\sharp\projects\BrightCart_Ecommerce_Dashboard"
raw_path = os.path.join(base_path, "data", "raw")
os.makedirs(raw_path, exist_ok=True)
print(f"📁 Writing CSVs to: {raw_path}\n")

# === Parameters ===
np.random.seed(42)
start_date = datetime(2025, 1, 1)
weeks = pd.date_range(start_date, periods=26, freq="W")

channels = ["Google Ads", "Meta Ads", "Email", "Organic Search"]
categories = ["Home Decor", "Kitchen", "Outdoor", "Electronics", "Furniture"]
products = [f"P{str(i).zfill(3)}" for i in range(101, 121)]

# === sales_raw.csv ===
sales_rows = []
for week in weeks:
    for category in categories:
        for _ in range(np.random.randint(5, 10)):
            product = np.random.choice(products)
            channel = np.random.choice(channels, p=[0.3, 0.3, 0.2, 0.2])
            units = np.random.randint(5, 50)
            price = np.random.uniform(15, 120)
            discount = np.random.choice([0, 5, 10, 15], p=[0.6, 0.2, 0.15, 0.05])
            sales_rows.append([week.date(), product, category, units, price, discount, channel])

sales_df = pd.DataFrame(
    sales_rows,
    columns=["Date", "Product_ID", "Category", "Units_Sold", "Unit_Price", "Discount", "Channel"]
)
sales_path = os.path.join(raw_path, "sales_raw.csv")
sales_df.to_csv(sales_path, index=False)
print(f"✅ Created: {sales_path} ({len(sales_df)} rows)")

# === ad_spend.csv ===
ad_rows = []
for week in weeks:
    for ch in channels:
        spend = np.random.uniform(500, 2500)
        clicks = np.random.randint(100, 500)
        impressions = clicks * np.random.randint(10, 25)
        ad_rows.append([week.date(), ch, spend, clicks, impressions])

ad_df = pd.DataFrame(ad_rows, columns=["Week", "Channel", "Spend", "Clicks", "Impressions"])
ad_path = os.path.join(raw_path, "ad_spend.csv")
ad_df.to_csv(ad_path, index=False)
print(f"✅ Created: {ad_path} ({len(ad_df)} rows)")

# === website_sessions.csv ===
session_rows = []
for week in weeks:
    for ch in channels:
        sessions = np.random.randint(800, 4000)
        conversions = int(sessions * np.random.uniform(0.01, 0.06))
        session_rows.append([week.date(), ch, sessions, conversions])

sessions_df = pd.DataFrame(
    session_rows,
    columns=["Week", "Source", "Sessions", "Conversions"]
)
sessions_path = os.path.join(raw_path, "website_sessions.csv")
sessions_df.to_csv(sessions_path, index=False)
print(f"✅ Created: {sessions_path} ({len(sessions_df)} rows)")

print("\n🎉 All 3 CSVs generated successfully!")
