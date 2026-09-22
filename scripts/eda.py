# ============================================================
# IMPORT LIBRARIES
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


# ============================================================
# PATHS
# ============================================================

DATA_DIR = Path("data/processed")
OUTPUT_DIR = Path("outputs/eda")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATASETS
# ============================================================

suppliers = pd.read_csv(
    DATA_DIR / "suppliers.csv"
)

items = pd.read_csv(
    DATA_DIR / "items.csv"
)

rfqs = pd.read_csv(
    DATA_DIR / "rfqs.csv"
)

rfq_items = pd.read_csv(
    DATA_DIR / "rfq_items.csv"
)

quotations = pd.read_csv(
    DATA_DIR / "quotations.csv"
)

quotation_items = pd.read_csv(
    DATA_DIR / "quotation_items.csv"
)

orders = pd.read_csv(
    DATA_DIR / "orders.csv"
)

order_items = pd.read_csv(
    DATA_DIR / "order_items.csv"
)

deliveries = pd.read_csv(
    DATA_DIR / "deliveries.csv"
)

quality = pd.read_csv(
    DATA_DIR / "quality.csv"
)


# ============================================================
# CONVERT DATE COLUMNS
# ============================================================

suppliers["created_date"] = pd.to_datetime(
    suppliers["created_date"]
)

rfqs["rfq_date"] = pd.to_datetime(
    rfqs["rfq_date"]
)

rfqs["required_delivery_date"] = pd.to_datetime(
    rfqs["required_delivery_date"]
)

quotations["quotation_date"] = pd.to_datetime(
    quotations["quotation_date"]
)

quotations["valid_until"] = pd.to_datetime(
    quotations["valid_until"]
)

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

deliveries["promised_date"] = pd.to_datetime(
    deliveries["promised_date"]
)

deliveries["actual_delivery_date"] = pd.to_datetime(
    deliveries["actual_delivery_date"]
)

quality["inspection_date"] = pd.to_datetime(
    quality["inspection_date"]
)


# ============================================================
# CREATE DATASET DICTIONARY
# ============================================================

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


# ============================================================
# DATASET OVERVIEW
# ============================================================

print("\n==============================")
print("DATASET OVERVIEW")
print("==============================")

for name, df in datasets.items():

    print(
        f"{name}: "
        f"{df.shape[0]} rows x "
        f"{df.shape[1]} columns"
    )


# ============================================================
# STATISTICAL SUMMARY
# ============================================================

print("\n==============================")
print("STATISTICAL SUMMARY")
print("==============================")

for name, df in datasets.items():

    print(f"\n{name}")

    print(
        df.describe(
            include="all"
        )
    )


# ============================================================
# SUPPLIER ANALYSIS
# ============================================================

print("\n==============================")
print("SUPPLIER CATEGORY")
print("==============================")

print(
    suppliers["category"]
    .value_counts()
)

print("\n==============================")
print("SUPPLIER STATUS")
print("==============================")

print(
    suppliers["status"]
    .value_counts()
)

print("\n==============================")
print("SUPPLIER EXPERIENCE")
print("==============================")

print(
    suppliers["years_in_business"]
    .describe()
)


# ============================================================
# SUPPLIER EXPERIENCE DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    suppliers["years_in_business"],
    bins=10
)

plt.title(
    "Distribution of Supplier Experience"
)

plt.xlabel(
    "Years in Business"
)

plt.ylabel(
    "Number of Suppliers"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "supplier_experience_distribution.png"
)

plt.show()


# ============================================================
# RFQ STATUS ANALYSIS
# ============================================================

print("\n==============================")
print("RFQ STATUS")
print("==============================")

print(
    rfqs["status"]
    .value_counts()
)

print("\n==============================")
print("RFQ DEPARTMENT")
print("==============================")

print(
    rfqs["department"]
    .value_counts()
)


# ============================================================
# MONTHLY RFQ VOLUME
# ============================================================

rfqs["rfq_month"] = (
    rfqs["rfq_date"]
    .dt.to_period("M")
    .astype(str)
)

rfq_monthly = (
    rfqs
    .groupby("rfq_month")
    .size()
    .sort_index()
)

print("\n==============================")
print("MONTHLY RFQ VOLUME")
print("==============================")

print(
    rfq_monthly
)


# ============================================================
# MONTHLY RFQ VOLUME VISUALIZATION
# ============================================================

plt.figure(figsize=(10, 5))

rfq_monthly.plot()

plt.title(
    "Monthly RFQ Volume"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Number of RFQs"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "monthly_rfq_volume.png"
)

plt.show()


# ============================================================
# QUOTATION STATUS
# ============================================================

print("\n==============================")
print("QUOTATION STATUS")
print("==============================")

print(
    quotations["status"]
    .value_counts()
)

print("\n==============================")
print("QUOTATION CURRENCY")
print("==============================")

print(
    quotations["currency"]
    .value_counts()
)

print("\n==============================")
print("PAYMENT TERMS")
print("==============================")

print(
    quotations["payment_terms"]
    .value_counts()
)


# ============================================================
# QUOTATION PRICE DISTRIBUTION
# ============================================================

print("\n==============================")
print("QUOTATION PRICE SUMMARY")
print("==============================")

print(
    quotation_items["unit_price"]
    .describe()
)


plt.figure(figsize=(8, 5))

plt.hist(
    quotation_items["unit_price"],
    bins=15
)

plt.title(
    "Distribution of Quoted Unit Prices"
)

plt.xlabel(
    "Unit Price"
)

plt.ylabel(
    "Number of Quotation Items"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "quotation_price_distribution.png"
)

plt.show()


# ============================================================
# DISCOUNT DISTRIBUTION
# ============================================================

print("\n==============================")
print("DISCOUNT SUMMARY")
print("==============================")

print(
    quotation_items["discount_percent"]
    .describe()
)


plt.figure(figsize=(8, 5))

plt.hist(
    quotation_items["discount_percent"],
    bins=10
)

plt.title(
    "Distribution of Quotation Discounts"
)

plt.xlabel(
    "Discount (%)"
)

plt.ylabel(
    "Number of Quotation Items"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "discount_distribution.png"
)

plt.show()


# ============================================================
# DELIVERY DAYS DISTRIBUTION
# ============================================================

print("\n==============================")
print("DELIVERY DAYS SUMMARY")
print("==============================")

print(
    quotation_items["delivery_days"]
    .describe()
)


plt.figure(figsize=(8, 5))

plt.hist(
    quotation_items["delivery_days"],
    bins=15
)

plt.title(
    "Distribution of Quoted Delivery Time"
)

plt.xlabel(
    "Delivery Days"
)

plt.ylabel(
    "Number of Quotation Items"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "delivery_days_distribution.png"
)

plt.show()


# ============================================================
# WARRANTY DISTRIBUTION
# ============================================================

print("\n==============================")
print("WARRANTY SUMMARY")
print("==============================")

print(
    quotation_items["warranty_months"]
    .describe()
)


plt.figure(figsize=(8, 5))

plt.hist(
    quotation_items["warranty_months"],
    bins=10
)

plt.title(
    "Distribution of Warranty Period"
)

plt.xlabel(
    "Warranty (Months)"
)

plt.ylabel(
    "Number of Quotation Items"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "warranty_distribution.png"
)

plt.show()


# ============================================================
# ORDER ANALYSIS
# ============================================================

print("\n==============================")
print("ORDER STATUS")
print("==============================")

print(
    orders["status"]
    .value_counts()
)

print("\n==============================")
print("TOTAL PROCUREMENT SPEND")
print("==============================")

print(
    orders["total_amount"].sum()
)

print("\n==============================")
print("AVERAGE ORDER VALUE")
print("==============================")

print(
    orders["total_amount"].mean()
)


# ============================================================
# ORDER VALUE DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    orders["total_amount"],
    bins=15
)

plt.title(
    "Distribution of Order Values"
)

plt.xlabel(
    "Order Amount"
)

plt.ylabel(
    "Number of Orders"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "order_value_distribution.png"
)

plt.show()


# ============================================================
# MONTHLY PROCUREMENT SPENDING
# ============================================================

orders["order_month"] = (
    orders["order_date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_spend = (
    orders
    .groupby("order_month")["total_amount"]
    .sum()
    .sort_index()
)

print("\n==============================")
print("MONTHLY PROCUREMENT SPEND")
print("==============================")

print(
    monthly_spend
)


plt.figure(figsize=(10, 5))

monthly_spend.plot()

plt.title(
    "Monthly Procurement Spend"
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Total Spend"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "monthly_procurement_spend.png"
)

plt.show()


# ============================================================
# SUPPLIER SPENDING ANALYSIS
# ============================================================

supplier_orders = orders.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name",
            "category"
        ]
    ],
    on="supplier_id",
    how="left"
)

supplier_spend = (
    supplier_orders
    .groupby("supplier_name")["total_amount"]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\n==============================")
print("SPEND BY SUPPLIER")
print("==============================")

print(
    supplier_spend
)


# ============================================================
# TOP 10 SUPPLIERS BY SPEND
# ============================================================

top_supplier_spend = (
    supplier_spend
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_supplier_spend.index,
    top_supplier_spend.values
)

plt.title(
    "Top 10 Suppliers by Procurement Spend"
)

plt.xlabel(
    "Total Spend"
)

plt.ylabel(
    "Supplier"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "top_10_suppliers_by_spend.png"
)

plt.show()


# ============================================================
# SUPPLIER ORDER VOLUME
# ============================================================

supplier_order_count = (
    supplier_orders
    .groupby("supplier_name")["order_id"]
    .count()
    .sort_values(
        ascending=False
    )
)

print("\n==============================")
print("ORDERS BY SUPPLIER")
print("==============================")

print(
    supplier_order_count
)


# ============================================================
# TOP 10 SUPPLIERS BY ORDER COUNT
# ============================================================

top_supplier_orders = (
    supplier_order_count
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_supplier_orders.index,
    top_supplier_orders.values
)

plt.title(
    "Top 10 Suppliers by Order Count"
)

plt.xlabel(
    "Number of Orders"
)

plt.ylabel(
    "Supplier"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "top_10_suppliers_by_order_count.png"
)

plt.show()


# ============================================================
# DELIVERY PERFORMANCE
# ============================================================

deliveries["delivery_delay_days"] = (
    deliveries["actual_delivery_date"]
    -
    deliveries["promised_date"]
).dt.days

print("\n==============================")
print("DELIVERY PERFORMANCE")
print("==============================")

print(
    deliveries["delivery_delay_days"]
    .describe()
)

late_deliveries = deliveries[
    deliveries["delivery_delay_days"] > 0
]

early_deliveries = deliveries[
    deliveries["delivery_delay_days"] < 0
]

on_time_deliveries = deliveries[
    deliveries["delivery_delay_days"] == 0
]

print(
    "\nLate deliveries:",
    len(late_deliveries)
)

print(
    "Early deliveries:",
    len(early_deliveries)
)

print(
    "On-time deliveries:",
    len(on_time_deliveries)
)


# ============================================================
# DELIVERY PERFORMANCE BREAKDOWN
# ============================================================

delivery_status_counts = pd.Series(
    {
        "Late": len(late_deliveries),
        "On Time": len(on_time_deliveries),
        "Early": len(early_deliveries)
    }
)

print("\n==============================")
print("DELIVERY STATUS BREAKDOWN")
print("==============================")

print(
    delivery_status_counts
)


plt.figure(figsize=(8, 5))

plt.bar(
    delivery_status_counts.index,
    delivery_status_counts.values
)

plt.title(
    "Delivery Performance Breakdown"
)

plt.xlabel(
    "Delivery Status"
)

plt.ylabel(
    "Number of Deliveries"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "delivery_status_breakdown.png"
)

plt.show()


# ============================================================
# DELIVERY DELAY DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    deliveries["delivery_delay_days"],
    bins=15
)

plt.title(
    "Distribution of Delivery Delays"
)

plt.xlabel(
    "Delay (Days)"
)

plt.ylabel(
    "Number of Deliveries"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "delivery_delay_distribution.png"
)

plt.show()


# ============================================================
# SUPPLIER DELIVERY PERFORMANCE
# ============================================================

supplier_deliveries = deliveries.merge(
    orders[
        [
            "order_id",
            "supplier_id"
        ]
    ],
    on="order_id",
    how="left"
)

supplier_delivery_performance = (
    supplier_deliveries
    .groupby("supplier_id")["delivery_delay_days"]
    .agg(
        average_delay="mean",
        median_delay="median",
        maximum_delay="max",
        delivery_count="count"
    )
    .sort_values(
        "average_delay",
        ascending=False
    )
)

print("\n==============================")
print("SUPPLIER DELIVERY PERFORMANCE")
print("==============================")

print(
    supplier_delivery_performance
)


# ============================================================
# SUPPLIER LATE DELIVERY RATE
# ============================================================

supplier_deliveries["is_late"] = (
    supplier_deliveries["delivery_delay_days"] > 0
)

supplier_late_rate = (
    supplier_deliveries
    .groupby("supplier_id")["is_late"]
    .mean()
    .mul(100)
    .sort_values(
        ascending=False
    )
)

print("\n==============================")
print("SUPPLIER LATE DELIVERY RATE")
print("==============================")

print(
    supplier_late_rate
)


# ============================================================
# TOP 10 SUPPLIERS BY LATE DELIVERY RATE
# ============================================================

top_late_suppliers = (
    supplier_late_rate
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_late_suppliers.index.astype(str),
    top_late_suppliers.values
)

plt.title(
    "Top 10 Suppliers by Late Delivery Rate"
)

plt.xlabel(
    "Late Delivery Rate (%)"
)

plt.ylabel(
    "Supplier ID"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "top_10_suppliers_late_delivery_rate.png"
)

plt.show()


# ============================================================
# QUALITY ANALYSIS
# ============================================================

print("\n==============================")
print("QUALITY STATUS")
print("==============================")

print(
    quality["quality_status"]
    .value_counts()
)


# ============================================================
# DEFECT RATE
# ============================================================

quality["defect_rate"] = np.divide(
    quality["defective_quantity"],
    quality["quantity_inspected"],
    out=np.full(
        len(quality),
        np.nan
    ),
    where=quality["quantity_inspected"] > 0
)

quality["defect_rate_percent"] = (
    quality["defect_rate"] * 100
)

print("\n==============================")
print("DEFECT RATE")
print("==============================")

print(
    quality["defect_rate_percent"]
    .describe()
)


# ============================================================
# QUALITY DISTRIBUTION
# ============================================================

plt.figure(figsize=(8, 5))

plt.hist(
    quality["defect_rate_percent"],
    bins=10
)

plt.title(
    "Distribution of Defect Rates"
)

plt.xlabel(
    "Defect Rate (%)"
)

plt.ylabel(
    "Number of Inspections"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "defect_rate_distribution.png"
)

plt.show()


# ============================================================
# QUALITY ACCEPTANCE RATE
# ============================================================

quality["acceptance_rate_percent"] = np.divide(
    quality["quantity_accepted"],
    quality["quantity_inspected"],
    out=np.full(
        len(quality),
        np.nan
    ),
    where=quality["quantity_inspected"] > 0
) * 100

print("\n==============================")
print("QUALITY ACCEPTANCE RATE")
print("==============================")

print(
    quality["acceptance_rate_percent"]
    .describe()
)


# ============================================================
# SUPPLIER QUALITY PERFORMANCE
# ============================================================

supplier_quality = quality.merge(
    orders[
        [
            "order_id",
            "supplier_id"
        ]
    ],
    on="order_id",
    how="left"
)

supplier_quality_performance = (
    supplier_quality
    .groupby("supplier_id")["defect_rate_percent"]
    .agg(
        average_defect_rate="mean",
        median_defect_rate="median",
        maximum_defect_rate="max",
        inspection_count="count"
    )
    .sort_values(
        "average_defect_rate",
        ascending=False
    )
)

print("\n==============================")
print("SUPPLIER QUALITY PERFORMANCE")
print("==============================")

print(
    supplier_quality_performance
)


# ============================================================
# TOP 10 SUPPLIERS BY DEFECT RATE
# ============================================================

top_defect_suppliers = (
    supplier_quality_performance[
        "average_defect_rate"
    ]
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_defect_suppliers.index.astype(str),
    top_defect_suppliers.values
)

plt.title(
    "Top 10 Suppliers by Average Defect Rate"
)

plt.xlabel(
    "Average Defect Rate (%)"
)

plt.ylabel(
    "Supplier ID"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "top_10_suppliers_defect_rate.png"
)

plt.show()


# ============================================================
# SUPPLIER QUOTATION PARTICIPATION
# ============================================================

supplier_quotations = quotations.merge(
    suppliers[
        [
            "supplier_id",
            "supplier_name"
        ]
    ],
    on="supplier_id",
    how="left"
)

quotation_count_by_supplier = (
    supplier_quotations
    .groupby("supplier_name")["quotation_id"]
    .count()
    .sort_values(
        ascending=False
    )
)

print("\n==============================")
print("QUOTATIONS BY SUPPLIER")
print("==============================")

print(
    quotation_count_by_supplier
)


# ============================================================
# TOP 10 SUPPLIERS BY QUOTATION COUNT
# ============================================================

top_quotation_suppliers = (
    quotation_count_by_supplier
    .head(10)
    .sort_values()
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_quotation_suppliers.index,
    top_quotation_suppliers.values
)

plt.title(
    "Top 10 Suppliers by Quotation Count"
)

plt.xlabel(
    "Number of Quotations"
)

plt.ylabel(
    "Supplier"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "top_10_suppliers_quotation_count.png"
)

plt.show()


# ============================================================
# QUOTATION PRICE ANALYSIS
# ============================================================

quotation_price_analysis = quotation_items.merge(
    quotations[
        [
            "quotation_id",
            "supplier_id"
        ]
    ],
    on="quotation_id",
    how="left"
)

supplier_average_price = (
    quotation_price_analysis
    .groupby("supplier_id")["unit_price"]
    .mean()
    .sort_values()
)

print("\n==============================")
print("AVERAGE QUOTED PRICE BY SUPPLIER")
print("==============================")

print(
    supplier_average_price
)


# ============================================================
# PRICE VS DELIVERY RELATIONSHIP
# ============================================================

price_delivery_correlation = (
    quotation_items[
        [
            "unit_price",
            "delivery_days"
        ]
    ]
    .corr()
)

print("\n==============================")
print("PRICE VS DELIVERY CORRELATION")
print("==============================")

print(
    price_delivery_correlation
)


# ============================================================
# PRICE VS DELIVERY VISUALIZATION
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    quotation_items["unit_price"],
    quotation_items["delivery_days"],
    alpha=0.25,
    s=15
)

plt.title(
    "Quoted Price vs Delivery Time"
)

plt.xlabel(
    "Unit Price"
)

plt.ylabel(
    "Delivery Days"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "price_vs_delivery.png"
)

plt.show()


# ============================================================
# PRICE VS DELIVERY BY PRICE BAND
# ============================================================

quotation_items["price_band"] = pd.qcut(
    quotation_items["unit_price"],
    q=5,
    duplicates="drop"
)

price_band_delivery = (
    quotation_items
    .groupby(
        "price_band",
        observed=True
    )["delivery_days"]
    .mean()
)

print("\n==============================")
print("AVERAGE DELIVERY BY PRICE BAND")
print("==============================")

print(
    price_band_delivery
)


plt.figure(figsize=(9, 5))

plt.bar(
    price_band_delivery.index.astype(str),
    price_band_delivery.values
)

plt.title(
    "Average Delivery Time by Price Band"
)

plt.xlabel(
    "Price Band"
)

plt.ylabel(
    "Average Delivery Days"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "delivery_by_price_band.png"
)

plt.show()


# ============================================================
# PRICE VS WARRANTY
# ============================================================

price_warranty_correlation = (
    quotation_items[
        [
            "unit_price",
            "warranty_months"
        ]
    ]
    .corr()
)

print("\n==============================")
print("PRICE VS WARRANTY CORRELATION")
print("==============================")

print(
    price_warranty_correlation
)


# ============================================================
# PRICE VS WARRANTY VISUALIZATION
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    quotation_items["unit_price"],
    quotation_items["warranty_months"],
    alpha=0.25,
    s=15
)

plt.title(
    "Quoted Price vs Warranty Period"
)

plt.xlabel(
    "Unit Price"
)

plt.ylabel(
    "Warranty (Months)"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "price_vs_warranty.png"
)

plt.show()


# ============================================================
# DISCOUNT VS PRICE
# ============================================================

discount_price_correlation = (
    quotation_items[
        [
            "discount_percent",
            "unit_price"
        ]
    ]
    .corr()
)

print("\n==============================")
print("DISCOUNT VS PRICE CORRELATION")
print("==============================")

print(
    discount_price_correlation
)


# ============================================================
# DISCOUNT VS PRICE VISUALIZATION
# ============================================================

plt.figure(figsize=(8, 5))

plt.scatter(
    quotation_items["discount_percent"],
    quotation_items["unit_price"],
    alpha=0.25,
    s=15
)

plt.title(
    "Discount vs Unit Price"
)

plt.xlabel(
    "Discount (%)"
)

plt.ylabel(
    "Unit Price"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "discount_vs_price.png"
)

plt.show()
# ============================================================
# ITEM-LEVEL PRICE ANALYSIS
# ============================================================

quotation_item_analysis = quotation_items.merge(
    rfq_items[
        [
            "rfq_item_id",
            "item_id"
        ]
    ],
    on="rfq_item_id",
    how="left"
)

quotation_item_analysis = quotation_item_analysis.merge(
    items[
        [
            "item_id",
            "item_name",
            "category"
        ]
    ],
    on="item_id",
    how="left"
)

item_price_summary = (
    quotation_item_analysis
    .groupby(
        [
            "item_id",
            "item_name"
        ]
    )["unit_price"]
    .agg(
        average_price="mean",
        minimum_price="min",
        maximum_price="max",
        price_std="std",
        quotation_count="count"
    )
    .reset_index()
    .sort_values(
        "average_price",
        ascending=False
    )
)

print("\n==============================")
print("ITEM PRICE ANALYSIS")
print("==============================")

print(
    item_price_summary.head(20)
)


# ============================================================
# PRICE VARIABILITY BY ITEM
# ============================================================

top_variable_items = (
    item_price_summary
    .sort_values(
        "price_std",
        ascending=False
    )
    .head(10)
    .sort_values(
        "price_std"
    )
)

plt.figure(figsize=(9, 6))

plt.barh(
    top_variable_items["item_name"],
    top_variable_items["price_std"]
)

plt.title(
    "Top 10 Items by Quoted Price Variability"
)

plt.xlabel(
    "Price Standard Deviation"
)

plt.ylabel(
    "Item"
)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR /
    "top_10_items_price_variability.png"
)

plt.show()

# ============================================================
# BUILD SUPPLIER PERFORMANCE DATASET
# ============================================================

supplier_summary = suppliers[
    [
        "supplier_id",
        "supplier_name",
        "category",
        "years_in_business",
        "status"
    ]
].copy()


# ============================================================
# ORDER FEATURES
# ============================================================

supplier_order_summary = (
    orders
    .groupby("supplier_id")
    .agg(
        order_count=(
            "order_id",
            "count"
        ),
        total_spend=(
            "total_amount",
            "sum"
        ),
        average_order_value=(
            "total_amount",
            "mean"
        )
    )
    .reset_index()
)

supplier_summary = supplier_summary.merge(
    supplier_order_summary,
    on="supplier_id",
    how="left"
)


# ============================================================
# DELIVERY FEATURES
# ============================================================

supplier_delivery_summary = (
    supplier_deliveries
    .groupby("supplier_id")
    .agg(
        average_delivery_delay=(
            "delivery_delay_days",
            "mean"
        ),
        median_delivery_delay=(
            "delivery_delay_days",
            "median"
        ),
        maximum_delivery_delay=(
            "delivery_delay_days",
            "max"
        ),
        delivery_count=(
            "delivery_id",
            "count"
        ),
        late_delivery_rate=(
            "is_late",
            "mean"
        )
    )
    .reset_index()
)

supplier_delivery_summary[
    "late_delivery_rate"
] = (
    supplier_delivery_summary[
        "late_delivery_rate"
    ] * 100
)

supplier_summary = supplier_summary.merge(
    supplier_delivery_summary,
    on="supplier_id",
    how="left"
)


# ============================================================
# QUALITY FEATURES
# ============================================================

supplier_quality_summary = (
    supplier_quality
    .groupby("supplier_id")
    .agg(
        average_defect_rate=(
            "defect_rate_percent",
            "mean"
        ),
        maximum_defect_rate=(
            "defect_rate_percent",
            "max"
        ),
        average_acceptance_rate=(
            "acceptance_rate_percent",
            "mean"
        ),
        inspection_count=(
            "quality_id",
            "count"
        )
    )
    .reset_index()
)

supplier_summary = supplier_summary.merge(
    supplier_quality_summary,
    on="supplier_id",
    how="left"
)


# ============================================================
# QUOTATION FEATURES
# ============================================================

supplier_quotation_summary = (
    quotation_price_analysis
    .groupby("supplier_id")
    .agg(
        quotation_item_count=(
            "quotation_item_id",
            "count"
        ),
        average_unit_price=(
            "unit_price",
            "mean"
        ),
        average_delivery_days=(
            "delivery_days",
            "mean"
        ),
        average_warranty_months=(
            "warranty_months",
            "mean"
        ),
        average_discount=(
            "discount_percent",
            "mean"
        )
    )
    .reset_index()
)

supplier_summary = supplier_summary.merge(
    supplier_quotation_summary,
    on="supplier_id",
    how="left"
)


# ============================================================
# VIEW SUPPLIER PERFORMANCE DATASET
# ============================================================

print("\n==============================")
print("SUPPLIER PERFORMANCE SUMMARY")
print("==============================")

print(
    supplier_summary.head(20)
)

print("\nSupplier summary statistics:")

print(
    supplier_summary.describe(
        include="all"
    )
)


# ============================================================
# SAVE SUPPLIER PERFORMANCE DATASET
# ============================================================

supplier_summary.to_csv(
    OUTPUT_DIR /
    "supplier_performance_summary.csv",
    index=False
)

print(
    "\nSupplier performance summary saved."
)


# ============================================================
# SAVE EDA SUMMARY TABLES
# ============================================================

rfq_monthly.to_csv(
    OUTPUT_DIR /
    "monthly_rfq_volume.csv"
)

monthly_spend.to_csv(
    OUTPUT_DIR /
    "monthly_procurement_spend.csv"
)

supplier_spend.to_csv(
    OUTPUT_DIR /
    "supplier_spend.csv"
)

supplier_order_count.to_csv(
    OUTPUT_DIR /
    "supplier_order_count.csv"
)

supplier_delivery_performance.to_csv(
    OUTPUT_DIR /
    "supplier_delivery_performance.csv"
)

supplier_late_rate.to_csv(
    OUTPUT_DIR /
    "supplier_late_delivery_rate.csv"
)

supplier_quality_performance.to_csv(
    OUTPUT_DIR /
    "supplier_quality_performance.csv"
)

item_price_summary.to_csv(
    OUTPUT_DIR /
    "item_price_summary.csv"
)

price_band_delivery.to_csv(
    OUTPUT_DIR /
    "delivery_by_price_band.csv"
)


# ============================================================
# FINAL EDA SUMMARY
# ============================================================

print("\n==============================")
print("EDA COMPLETE")
print("==============================")

print(
    "\nKey analytical outputs created:"
)

print(
    "- Supplier analysis"
)

print(
    "- RFQ analysis"
)

print(
    "- Monthly RFQ volume"
)

print(
    "- Procurement spending analysis"
)

print(
    "- Supplier spending analysis"
)

print(
    "- Supplier order volume"
)

print(
    "- Delivery performance"
)

print(
    "- Supplier late delivery rate"
)

print(
    "- Quality performance"
)

print(
    "- Supplier defect rate"
)

print(
    "- Quotation participation"
)

print(
    "- Quoted price analysis"
)

print(
    "- Price vs delivery analysis"
)

print(
    "- Price vs warranty analysis"
)

print(
    "- Discount vs price analysis"
)

print(
    "- Item-level price variability"
)

print(
    "- Supplier performance summary"
)

print(
    "\nCharts and analysis files saved to:"
)

print(
    OUTPUT_DIR
)