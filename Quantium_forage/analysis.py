# Import libraries
import pandas as pd
import matplotlib as plt
from datetime import date

# Set file path (replace with your actual path)
file_path = "C:/Users/Suyash/OneDrive/Desktop/Quantium_forage"

# Read data files
transaction_data = pd.read_csv(f"{"C:/Users/Suyash/OneDrive/Desktop/Quantium_forage"},QVI_transaction_data.csv")
customer_data = pd.read_csv(f"{"C:/Users/Suyash/OneDrive/Desktop/Quantium_forage"}QVI_purchase_behaviour.csv")

# Examine transaction data
print(transaction_data.head())  # View the first few rows
print(transaction_data.dtypes)  # Check data types

# Convert DATE to datetime format
transaction_data["DATE"] = pd.to_datetime(transaction_data["DATE"], origin="1899-12-30")

# Examine product names
product_words = (
    transaction_data["PROD_NAME"]
    .str.split()
    .explode()
    .str.lower()
    .replace("[^/w/s]", "", regex=True)
    .value_counts()
    .reset_index()
    .rename(columns={"index": "words", "PROD_NAME": "count"})
)

# Remove non-chip products (modify list as needed)
not_chips = ["salsa"]
transaction_data = transaction_data[~transaction_data["PROD_NAME"].str.contains("|".join(not_chips), case=False)]

# Check for outliers and nulls
print(transaction_data.describe())  # Summary statistics

# Investigate outlier purchase
large_purchase = transaction_data[transaction_data["QUANTITY"] == 200]
print(large_purchase)

# Filter based on loyalty card number (if applicable)
loyalty_card_to_remove = "..."  # Replace with actual card number
transaction_data = transaction_data[transaction_data["LOYALTY_CARD_NO"] != loyalty_card_to_remove]

# Count transactions by date
transactions_by_day = (
    transaction_data.groupby("DATE")
    .size()
    .to_frame(name="N")
    .reset_index()
    .sort_values(by=["DATE"])
)

# Create a date range for missing data
start_date = date(2018, 7, 1)
end_date = date(2019, 6, 30)
date_range = pd.date_range(start_date, end_date)

# Combine data with date range
data = pd.merge(left=transactions_by_day, right=date_range.to_frame(name="DATE"), how="right")
data.fillna(0, inplace=True)  # Fill missing dates with 0 transactions

# Plot transactions over time
plt.figure(figsize=(10, 6))
plt.plot(data["DATE"], data["N"], marker="o", linestyle="-")
plt.title("Transactions Over Time")
plt.xlabel("Date")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()

# Focus on December transactions
dec_data = data[data["DATE"].dt.month == 12]
plt.figure(figsize=(10, 6))
plt.plot(dec_data["DATE"], dec_data["N"], marker="o", linestyle="-")
plt.title("Transactions in December")
plt.xlabel("Date")
plt.ylabel("Number of Transactions")
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.show()

# Create pack size
transaction_data["PACK_SIZE"] = pd.to_numeric(transaction_data["PROD_NAME"].str.extract("(\d+)", expand=False), errors="coerce")

# Plot pack size distribution
plt.figure(figsize=(8, 6))
plt.hist(transaction_data["PACK_SIZE"], bins=10, edgecolor="black")
plt.title("Pack Size Distribution")
plt.xlabel("Pack Size (g)")
plt.ylabel("Number of Transactions")
plt.grid(True)
plt.tight_layout()
plt.show()

# Create brand name
transaction_data["BRAND"] = transaction_data["PROD_NAME"].str.split().str[0]

# Clean brand names (modify as needed)