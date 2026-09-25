import pandas as pd
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("data/processed")


# ============================================================
# 2. LOAD DATA
# ============================================================

suppliers = pd.read_csv(DATA_DIR / "suppliers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
deliveries = pd.read_csv(DATA_DIR / "deliveries.csv")
quality = pd.read_csv(DATA_DIR / "quality.csv")
quotations = pd.read_csv(DATA_DIR / "quotations.csv")
quotation_items = pd.read_csv(DATA_DIR / "quotation_items.csv")
rfq_items = pd.read_csv(DATA_DIR / "rfq_items.csv")


print("Datasets loaded successfully.")

print("\nDataset shapes:")
print("Suppliers:", suppliers.shape)
print("Orders:", orders.shape)
print("Deliveries:", deliveries.shape)
print("Quality:", quality.shape)
print("Quotations:", quotations.shape)
print("Quotation Items:", quotation_items.shape)
print("RFQ Items:", rfq_items.shape)


# ============================================================
# 3. SUPPLIER BASE FEATURES
# ============================================================

supplier_features = suppliers[
    [
        "supplier_id",
        "supplier_name",
        "category",
        "location",
        "years_in_business"
    ]
].copy()


# ============================================================
# 4. ORDER / SPEND FEATURES
# ============================================================

order_features = (
    orders
    .groupby("supplier_id")
    .agg(
        order_count=("order_id", "count"),
        total_spend=("total_amount", "sum"),
        avg_order_value=("total_amount", "mean")
    )
    .reset_index()
)


# ============================================================
# 5. DELIVERY FEATURES
# ============================================================

deliveries["promised_date"] = pd.to_datetime(
    deliveries["promised_date"]
)

deliveries["actual_delivery_date"] = pd.to_datetime(
    deliveries["actual_delivery_date"]
)


# Calculate how many days late/early the delivery was
deliveries["delivery_delay_days"] = (
    deliveries["actual_delivery_date"]
    - deliveries["promised_date"]
).dt.days


# 1 = late
# 0 = on time or early
deliveries["is_late"] = (
    deliveries["delivery_delay_days"] > 0
).astype(int)


delivery_features = (
    deliveries
    .groupby("order_id")
    .agg(
        avg_delivery_delay=("delivery_delay_days", "mean"),
        late_delivery_rate=("is_late", "mean")
    )
    .reset_index()
)


# Attach supplier_id to delivery information
delivery_features = delivery_features.merge(
    orders[
        [
            "order_id",
            "supplier_id"
        ]
    ],
    on="order_id",
    how="left"
)


# Convert order-level delivery performance
# into supplier-level performance
delivery_features = (
    delivery_features
    .groupby("supplier_id")
    .agg(
        avg_delivery_delay=("avg_delivery_delay", "mean"),
        late_delivery_rate=("late_delivery_rate", "mean")
    )
    .reset_index()
)


# On-time rate = 1 - late rate
delivery_features["on_time_delivery_rate"] = (
    1 - delivery_features["late_delivery_rate"]
)


# ============================================================
# 6. QUALITY FEATURES
# ============================================================

# Avoid division-by-zero
quality["acceptance_rate"] = (
    quality["quantity_accepted"]
    / quality["quantity_inspected"].replace(0, pd.NA)
)

quality["defect_rate"] = (
    quality["defective_quantity"]
    / quality["quantity_inspected"].replace(0, pd.NA)
)


quality_features = (
    quality
    .groupby("order_id")
    .agg(
        quality_acceptance_rate=("acceptance_rate", "mean"),
        defect_rate=("defect_rate", "mean")
    )
    .reset_index()
)


# Attach supplier information
quality_features = quality_features.merge(
    orders[
        [
            "order_id",
            "supplier_id"
        ]
    ],
    on="order_id",
    how="left"
)


# Convert order-level quality performance
# into supplier-level performance
quality_features = (
    quality_features
    .groupby("supplier_id")
    .agg(
        quality_acceptance_rate=("quality_acceptance_rate", "mean"),
        defect_rate=("defect_rate", "mean")
    )
    .reset_index()
)


# ============================================================
# 7. QUOTATION FEATURES
# ============================================================

# Number of quotations submitted by each supplier
quotation_count = (
    quotations
    .groupby("supplier_id")
    .agg(
        quotation_count=("quotation_id", "nunique")
    )
    .reset_index()
)


# ============================================================
# 8. PRICING FEATURES
# ============================================================

pricing_features = (
    quotation_items
    .merge(
        quotations[
            [
                "quotation_id",
                "supplier_id"
            ]
        ],
        on="quotation_id",
        how="left"
    )
    .groupby("supplier_id")
    .agg(
        avg_quoted_price=("unit_price", "mean"),
        min_quoted_price=("unit_price", "min"),
        price_std=("unit_price", "std"),
        avg_discount=("discount_percent", "mean")
    )
    .reset_index()
)


# Combine quotation count
pricing_features = pricing_features.merge(
    quotation_count,
    on="supplier_id",
    how="left"
)


# ============================================================
# 9. PRICE COMPETITIVENESS
# ============================================================

# Connect quotation items to RFQ items
price_data = quotation_items.merge(
    quotations[
        [
            "quotation_id",
            "supplier_id"
        ]
    ],
    on="quotation_id",
    how="left"
)


price_data = price_data.merge(
    rfq_items[
        [
            "rfq_item_id",
            "item_id"
        ]
    ],
    on="rfq_item_id",
    how="left"
)


# Calculate the average market/peer price for each item
item_reference_price = (
    price_data
    .groupby("item_id")["unit_price"]
    .mean()
    .reset_index()
    .rename(
        columns={
            "unit_price": "item_avg_price"
        }
    )
)


price_data = price_data.merge(
    item_reference_price,
    on="item_id",
    how="left"
)


# Compare supplier price against item-level average
#
# Example:
# supplier price = 90
# average item price = 100
#
# price competitiveness = 0.90
#
# Lower value = cheaper relative to peers
price_data["price_vs_market"] = (
    price_data["unit_price"]
    / price_data["item_avg_price"]
)


# Supplier-level average price competitiveness
price_competitiveness = (
    price_data
    .groupby("supplier_id")
    .agg(
        avg_price_vs_market=("price_vs_market", "mean")
    )
    .reset_index()
)


# ============================================================
# 10. COMBINE ALL FEATURES
# ============================================================

supplier_features = supplier_features.merge(
    order_features,
    on="supplier_id",
    how="left"
)

supplier_features = supplier_features.merge(
    delivery_features,
    on="supplier_id",
    how="left"
)

supplier_features = supplier_features.merge(
    quality_features,
    on="supplier_id",
    how="left"
)

supplier_features = supplier_features.merge(
    pricing_features,
    on="supplier_id",
    how="left"
)

supplier_features = supplier_features.merge(
    price_competitiveness,
    on="supplier_id",
    how="left"
)


# ============================================================
# 11. HANDLE MISSING VALUES
# ============================================================

numeric_columns = supplier_features.select_dtypes(
    include="number"
).columns


supplier_features[numeric_columns] = (
    supplier_features[numeric_columns]
    .fillna(0)
)


# ============================================================
# 12. FINAL COLUMN ORDER
# ============================================================

supplier_features = supplier_features[
    [
        "supplier_id",
        "supplier_name",
        "category",
        "location",
        "years_in_business",

        "order_count",
        "total_spend",
        "avg_order_value",

        "avg_delivery_delay",
        "late_delivery_rate",
        "on_time_delivery_rate",

        "quality_acceptance_rate",
        "defect_rate",

        "quotation_count",
        "avg_quoted_price",
        "min_quoted_price",
        "price_std",
        "avg_discount",
        "avg_price_vs_market"
    ]
]


# ============================================================
# 13. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 60)
print("FINAL SUPPLIER FEATURES")
print("=" * 60)

print(supplier_features.head(10))


print("\nFeature dataset shape:")
print(supplier_features.shape)


print("\nFeature columns:")
for column in supplier_features.columns:
    print("-", column)


# ============================================================
# 14. SAVE FEATURE DATASET
# ============================================================

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


output_path = OUTPUT_DIR / "supplier_features.csv"

supplier_features.to_csv(
    output_path,
    index=False
)


print("\nFeature dataset saved to:")
print(output_path)

print("\nRISK FEATURE DISTRIBUTIONS")
print("\nLate delivery rate:")
print(supplier_features["late_delivery_rate"].describe())

print("\nDefect rate:")
print(supplier_features["defect_rate"].describe())

print("\nOn-time delivery rate:")
print(supplier_features["on_time_delivery_rate"].describe())

print("\nQuality acceptance rate:")
print(supplier_features["quality_acceptance_rate"].describe())