import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
items = pd.read_csv(DATA_DIR / "items.csv")
rfqs = pd.read_csv(DATA_DIR / "rfqs.csv")
rfq_items = pd.read_csv(DATA_DIR / "rfq_items.csv")
quotations = pd.read_csv(DATA_DIR / "quotations.csv")
quotation_items = pd.read_csv(DATA_DIR / "quotation_items.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
order_items = pd.read_csv(DATA_DIR / "order_items.csv")
deliveries = pd.read_csv(DATA_DIR / "deliveries.csv")
quality = pd.read_csv(DATA_DIR / "quality.csv")

datasets = {
    "suppliers": suppliers,
    "items": items,
    "rfqs": rfqs,
    "rfq_items": rfq_items,
    "quotations": quotations,
    "quotation_items": quotation_items,
    "orders": orders,
    "order_items": order_items,
    "deliveries": deliveries,
    "quality": quality
}

#profiling
#get number of rows and columns
for name, df in datasets.items():
    print(f"\n{name}")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

#check for column names
for name, df in datasets.items():
    print(f"\n{name}")
    print(df.columns.tolist())

#check for data types of the columns
for name, df in datasets.items():
    print(f"\n{name}")
    print(df.dtypes)
#we see quotation_date,valid_until,supplier_id,quotation_id,rfq_id is a str which is a mistake 

#check for missing values
for name, df in datasets.items():
    print(f"\n{name}")
    print(df.isnull().sum())

#check for duplicates
for name, df in datasets.items():
    print(f"\n{name}")
    print("Duplicate rows:", df.duplicated().sum())

#check for unique values
print(suppliers["status"].unique())
print(suppliers["status"].unique())
print(quotations["currency"].unique())
print(quality["quality_status"].unique())

#numerical profiling
print(suppliers.describe())
print(quotation_items.describe())

#date profiling
print(rfqs[["rfq_date", "required_delivery_date"]].dtypes)
#making sure the dates are in right format
rfqs["rfq_date"] = pd.to_datetime(
    rfqs["rfq_date"],
    errors="coerce"
)

rfqs["required_delivery_date"] = pd.to_datetime(
    rfqs["required_delivery_date"],
    errors="coerce"
)
print(rfqs[["rfq_date", "required_delivery_date"]].isna().sum())

#checking if the dates are calid for business
invalid_dates = rfqs[
    rfqs["required_delivery_date"] < rfqs["rfq_date"]
]

print(invalid_dates)

#data type cleaning
for name, df in datasets.items():
    print(f"\n{name}")
    print(df.dtypes)
#convert the date columns
suppliers["created_date"] = pd.to_datetime(
    suppliers["created_date"],
    errors="coerce"
)

rfqs["rfq_date"] = pd.to_datetime(
    rfqs["rfq_date"],
    errors="coerce"
)

rfqs["required_delivery_date"] = pd.to_datetime(
    rfqs["required_delivery_date"],
    errors="coerce"
)

quotations["quotation_date"] = pd.to_datetime(
    quotations["quotation_date"],
    errors="coerce"
)

quotations["valid_until"] = pd.to_datetime(
    quotations["valid_until"],
    errors="coerce"
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

deliveries["promised_date"] = pd.to_datetime(
    deliveries["promised_date"],
    errors="coerce"
)

deliveries["actual_delivery_date"] = pd.to_datetime(
    deliveries["actual_delivery_date"],
    errors="coerce"
)

quality["inspection_date"] = pd.to_datetime(
    quality["inspection_date"],
    errors="coerce"
)

#converting numerical columns
suppliers["years_in_business"] = pd.to_numeric(
    suppliers["years_in_business"],
    errors="coerce"
)

rfq_items["quantity"] = pd.to_numeric(
    rfq_items["quantity"],
    errors="coerce"
)

quotation_items["unit_price"] = pd.to_numeric(
    quotation_items["unit_price"],
    errors="coerce"
)

quotation_items["quantity_quoted"] = pd.to_numeric(
    quotation_items["quantity_quoted"],
    errors="coerce"
)

quotation_items["delivery_days"] = pd.to_numeric(
    quotation_items["delivery_days"],
    errors="coerce"
)

quotation_items["warranty_months"] = pd.to_numeric(
    quotation_items["warranty_months"],
    errors="coerce"
)

quotation_items["discount_percent"] = pd.to_numeric(
    quotation_items["discount_percent"],
    errors="coerce"
)

orders["total_amount"] = pd.to_numeric(
    orders["total_amount"],
    errors="coerce"
)

order_items["quantity_ordered"] = pd.to_numeric(
    order_items["quantity_ordered"],
    errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)

order_items["total_price"] = pd.to_numeric(
    order_items["total_price"],
    errors="coerce"
)

deliveries["quantity_ordered"] = pd.to_numeric(
    deliveries["quantity_ordered"],
    errors="coerce"
)

deliveries["quantity_received"] = pd.to_numeric(
    deliveries["quantity_received"],
    errors="coerce"
)

quality["quantity_inspected"] = pd.to_numeric(
    quality["quantity_inspected"],
    errors="coerce"
)

quality["quantity_accepted"] = pd.to_numeric(
    quality["quantity_accepted"],
    errors="coerce"
)

quality["defective_quantity"] = pd.to_numeric(
    quality["defective_quantity"],
    errors="coerce"
)

#missing value analysis
for name, df in datasets.items():

    print(f"\n{name}")

    missing = df.isna().sum()

    print(missing[missing > 0])

#missing percentage
for name, df in datasets.items():

    print(f"\n{name}")

    missing_percentage = (
        df.isna().mean() * 100
    )

    print(
        missing_percentage[
            missing_percentage > 0
        ].sort_values(ascending=False)
    
    )
#duplicate Analysis
for name, df in datasets.items():

    duplicate_count = df.duplicated().sum()

    print(
        f"{name}: "
        f"{duplicate_count} exact duplicate rows"
    )
#displaying duplicate rows if present
for name, df in datasets.items():

    duplicates = df[df.duplicated(keep=False)]

    if not duplicates.empty:

        print(f"\n{name} duplicates:")
        print(duplicates)

#primary key duplication detection
primary_keys = {
    "suppliers": "supplier_id",
    "items": "item_id",
    "rfqs": "rfq_id",
    "rfq_items": "rfq_item_id",
    "quotations": "quotation_id",
    "quotation_items": "quotation_item_id",
    "orders": "order_id",
    "order_items": "order_item_id",
    "deliveries": "delivery_id",
    "quality": "quality_id"
}



print("PRIMARY KEY DUPLICATES")



for name, key in primary_keys.items():

    duplicate_count = datasets[name][key].duplicated().sum()

    print(
        f"{name}: "
        f"{duplicate_count} duplicate {key} values"
    )

#Categorical Consistency
categorical_columns = {
    "suppliers": [
        "category",
        "location",
        "status"
    ],

    "rfqs": [
        "department",
        "status"
    ],

    "quotations": [
        "currency",
        "payment_terms",
        "status"
    ],

    "orders": [
        "currency",
        "status"
    ],

    "deliveries": [
        "delivery_status"
    ],

    "quality": [
        "quality_status"
    ]
}

print("CATEGORICAL VALUES")

for dataset_name, columns in categorical_columns.items():

    print(f"\n{dataset_name}")

    df = datasets[dataset_name]

    for column in columns:

        print(f"\n{column}")
        print(df[column].value_counts(dropna=False))

#Standardize text formatting
for dataset_name, columns in categorical_columns.items():

    df = datasets[dataset_name]

    for column in columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )
for dataset_name, columns in categorical_columns.items():

    print(f"\n{dataset_name}")

    df = datasets[dataset_name]

    for column in columns:

        print(f"\n{column}")
        print(df[column].value_counts(dropna=False))

#Supplier name Consistency
print(
    suppliers["supplier_name"]
    .value_counts()
)

suppliers["supplier_name_normalized"] = (
    suppliers["supplier_name"]
    .astype("string")
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
)

print(
    suppliers[
        [
            "supplier_name",
            "supplier_name_normalized"
        ]
    ].drop_duplicates()
)

#Date Validation
invalid_rfq_dates = rfqs[
    rfqs["required_delivery_date"]
    < rfqs["rfq_date"]
]

print("\nInvalid RFQ date relationships:")
print(invalid_rfq_dates)

invalid_quotation_dates = quotations[
    quotations["valid_until"]
    < quotations["quotation_date"]
]

print("\nInvalid quotation dates:")
print(invalid_quotation_dates)

invalid_delivery_dates = deliveries[
    deliveries["actual_delivery_date"]
    < deliveries["promised_date"]
]

print("\nDeliveries completed before promised date:")
print(invalid_delivery_dates)

#Numerical Validation

negative_prices = quotation_items[
    quotation_items["unit_price"] < 0
]

print("\nNegative quotation prices:")
print(negative_prices)

negative_quantities = quotation_items[
    quotation_items["quantity_quoted"] < 0
]

print("\nNegative quoted quantities:")
print(negative_quantities)

negative_delivery_days = quotation_items[
    quotation_items["delivery_days"] < 0
]

print("\nNegative delivery days:")
print(negative_delivery_days)

invalid_discounts = quotation_items[
    (quotation_items["discount_percent"] < 0)
    |
    (quotation_items["discount_percent"] > 100)
]

print("\nInvalid discounts:")
print(invalid_discounts)

#Quantity Validation
invalid_discounts = quotation_items[
    (quotation_items["discount_percent"] < 0)
    |
    (quotation_items["discount_percent"] > 100)
]

print("\nInvalid discounts:")
print(invalid_discounts)

#Quality Validation
quality["calculated_inspected"] = (
    quality["quantity_accepted"]
    +
    quality["defective_quantity"]
)
quality_mismatch = quality[
    quality["calculated_inspected"]
    != quality["quantity_inspected"]
]

print("\nQuality quantity mismatches:")
print(quality_mismatch)


#Outlier Analysis
Q1 = quotation_items["unit_price"].quantile(0.25)
Q3 = quotation_items["unit_price"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

price_outliers = quotation_items[
    (quotation_items["unit_price"] < lower_bound)
    |
    (quotation_items["unit_price"] > upper_bound)
]

print("\nPrice outliers:")
print(price_outliers)

#Referential Integrity
invalid_rfq_references = rfq_items[
    ~rfq_items["rfq_id"].isin(
        rfqs["rfq_id"]
    )
]

print("\nInvalid RFQ references:")
print(invalid_rfq_references)

invalid_item_references = rfq_items[
    ~rfq_items["item_id"].isin(
        items["item_id"]
    )
]

print("\nInvalid item references:")
print(invalid_item_references)

invalid_supplier_references = quotations[
    ~quotations["supplier_id"].isin(
        suppliers["supplier_id"]
    )
]

print("\nInvalid supplier references:")
print(invalid_supplier_references)

invalid_quotation_rfq_references = quotations[
    ~quotations["rfq_id"].isin(
        rfqs["rfq_id"]
    )
]

print("\nInvalid quotation RFQ references:")
print(invalid_quotation_rfq_references)

#Additional Business Relationship Validation
quotation_item_check = quotation_items.merge(
    quotations[
        ["quotation_id", "rfq_id"]
    ],
    on="quotation_id",
    how="left"
)

quotation_item_check = quotation_item_check.merge(
    rfq_items[
        ["rfq_item_id", "rfq_id"]
    ],
    on="rfq_item_id",
    how="left",
    suffixes=("_quotation", "_rfq_item")
)

relationship_errors = quotation_item_check[
    quotation_item_check["rfq_id_quotation"]
    !=
    quotation_item_check["rfq_id_rfq_item"]
]

print("\nQuotation/RFQ relationship errors:")
print(relationship_errors)

#Cleaning Decision
issue_summary = { "negative_prices": len(negative_prices), "negative_quantities": len(negative_quantities),"invalid_discounts": len(invalid_discounts),"invalid_rfq_dates": len(invalid_rfq_dates),"invalid_quotation_dates": len(invalid_quotation_dates),"invalid_supplier_references": len(invalid_supplier_references),"relationship_errors": len(relationship_errors)}

print("\n==============================")
print("DATA QUALITY ISSUE SUMMARY")
print("==============================")

for issue, count in issue_summary.items():
    print(f"{issue}: {count}")

#cleaning functions
def clean_text_columns(df, columns):
    for column in columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    return df

suppliers = clean_text_columns(
    suppliers,
    ["supplier_name", "category", "location", "status"]
)

#data cleaning function
def convert_date_columns(df, columns):

    for column in columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce"
        )

    return df

suppliers = convert_date_columns(
    suppliers,
    ["created_date"]
)

rfqs = convert_date_columns(
    rfqs,
    ["rfq_date", "required_delivery_date"]
)

quotations = convert_date_columns(
    quotations,
    ["quotation_date", "valid_until"]
)

orders = convert_date_columns(
    orders,
    ["order_date"]
)

deliveries = convert_date_columns(
    deliveries,
    ["promised_date", "actual_delivery_date"]
)

quality = convert_date_columns(
    quality,
    ["inspection_date"]
)
#saved cleaned data
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(
    parents=True,
    exist_ok=True
)

for name, df in datasets.items():

    output_path = PROCESSED_DIR / f"{name}.csv"

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Saved: {output_path}")

quality_report = []

for name, df in datasets.items():

    quality_report.append({
        "dataset": name,
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": df.isna().sum().sum(),
        "duplicate_rows": df.duplicated().sum()
    })


quality_report = pd.DataFrame(quality_report)

print("\n==============================")
print("DATA QUALITY REPORT")
print("==============================")

print(quality_report)

