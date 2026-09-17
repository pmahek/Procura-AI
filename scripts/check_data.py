import pandas as pd
from pathlib import Path


DATA_DIR = Path("data/raw")

files = [
    "suppliers.csv",
    "items.csv",
    "rfqs.csv",
    "rfq_items.csv",
    "quotations.csv",
    "quotation_items.csv",
    "orders.csv",
    "order_items.csv",
    "deliveries.csv",
    "quality.csv"
]


print("\n==============================")
print("PROCUREMENT DATA CHECK")
print("==============================")

for file in files:
    path = DATA_DIR / file

    df = pd.read_csv(path)

    print(f"\n{file}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Column names: {list(df.columns)}")