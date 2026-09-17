import pandas as pd
import numpy as np


# Reproducible random generator
rng = np.random.default_rng(42)


# ============================================================
# 1. SUPPLIERS
# ============================================================

supplier_count = 100

supplier_ids = [f"SUP{i:03d}" for i in range(1, supplier_count + 1)]

supplier_names = [
    f"{prefix} {suffix}"
    for prefix, suffix in zip(
        rng.choice(
            ["Alpha", "Beta", "Gamma", "Delta", "Nova",
             "Prime", "Vertex", "Global", "Tech", "Apex"],
            supplier_count
        ),
        rng.choice(
            ["Technologies", "Solutions", "Industries", "Systems",
             "Enterprises", "Supplies"],
            supplier_count
        )
    )
]

categories = rng.choice(
    ["Electronics", "Office Supplies", "IT Equipment",
     "Furniture", "Industrial Equipment"],
    supplier_count
)

cities = rng.choice(
    ["Bengaluru", "Mumbai", "Pune", "Delhi",
     "Hyderabad", "Chennai", "Ahmedabad"],
    supplier_count
)

years_in_business = rng.integers(2, 26, supplier_count)

status = rng.choice(
    ["Active", "Active", "Active", "Inactive"],
    supplier_count
)

created_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2000-01-01", "2024-12-31"),
        supplier_count
    )
)

suppliers = pd.DataFrame({
    "supplier_id": supplier_ids,
    "supplier_name": supplier_names,
    "category": categories,
    "location": cities,
    "years_in_business": years_in_business,
    "status": status,
    "created_date": created_dates
})


# ============================================================
# 2. ITEMS
# ============================================================

item_count = 50

item_ids = [f"ITEM{i:03d}" for i in range(1, item_count + 1)]

item_names = rng.choice(
    [
        "Business Laptop",
        "Desktop Computer",
        "Monitor",
        "Keyboard",
        "Mouse",
        "Printer",
        "Office Chair",
        "Desk",
        "Network Switch",
        "Router",
        "Server",
        "UPS",
        "Projector",
        "Tablet",
        "Barcode Scanner"
    ],
    item_count
)

item_categories = rng.choice(
    ["Electronics", "IT Equipment", "Office Supplies", "Furniture"],
    item_count
)

descriptions = [
    f"Business procurement item {i}"
    for i in range(1, item_count + 1)
]

units = rng.choice(
    ["Each", "Box", "Unit"],
    item_count
)

specifications = rng.choice(
    [
        "Standard specification",
        "Enterprise specification",
        "Premium specification",
        "Basic specification"
    ],
    item_count
)

items = pd.DataFrame({
    "item_id": item_ids,
    "item_name": item_names,
    "category": item_categories,
    "description": descriptions,
    "unit_of_measure": units,
    "specifications": specifications
})


# ============================================================
# 3. SAVE
# ============================================================

suppliers.to_csv("data/raw/suppliers.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)

print("Supplier records:", len(suppliers))
print("Item records:", len(items))

print("\nSuppliers:")
print(suppliers.head())

print("\nItems:")
print(items.head())

print("\nData generation completed.")

# ============================================================
# 3. RFQs
# ============================================================

rfq_count = 500

rfq_ids = [f"RFQ{i:04d}" for i in range(1, rfq_count + 1)]

rfq_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2024-01-01", "2026-09-01"),
        rfq_count
    )
)

required_delivery_dates = rfq_dates + pd.to_timedelta(
    rng.integers(15, 90, rfq_count),
    unit="D"
)

departments = rng.choice(
    ["IT", "Finance", "Operations", "HR", "Procurement"],
    rfq_count
)

rfq_status = rng.choice(
    ["Open", "Closed", "Awarded", "Cancelled"],
    rfq_count
)

rfq_descriptions = [
    f"Procurement requirement for RFQ {rfq_id}"
    for rfq_id in rfq_ids
]

rfqs = pd.DataFrame({
    "rfq_id": rfq_ids,
    "rfq_date": rfq_dates,
    "required_delivery_date": required_delivery_dates,
    "department": departments,
    "status": rfq_status,
    "description": rfq_descriptions
})
# ============================================================
# 4. SAVE
# ============================================================

suppliers.to_csv("data/raw/suppliers.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)
rfqs.to_csv("data/raw/rfqs.csv", index=False)

print("Supplier records:", len(suppliers))
print("Item records:", len(items))
print("RFQ records:", len(rfqs))

print("\nRFQs:")
print(rfqs.head())

print("\nData generation completed.")

# ============================================================
# 4. RFQ ITEMS
# ============================================================

rfq_item_count = 1200

rfq_item_ids = [
    f"RFQI{i:05d}" for i in range(1, rfq_item_count + 1)
]

rfq_item_rfq_ids = rng.choice(
    rfq_ids,
    rfq_item_count
)

rfq_item_ids_selected = rng.choice(
    item_ids,
    rfq_item_count
)

quantities = rng.integers(
    10,
    1000,
    rfq_item_count
)

rfq_items = pd.DataFrame({
    "rfq_item_id": rfq_item_ids,
    "rfq_id": rfq_item_rfq_ids,
    "item_id": rfq_item_ids_selected,
    "quantity": quantities
})

# ============================================================
# 5. SAVE
# ============================================================

suppliers.to_csv("data/raw/suppliers.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)
rfqs.to_csv("data/raw/rfqs.csv", index=False)
rfq_items.to_csv("data/raw/rfq_items.csv", index=False)

print("Supplier records:", len(suppliers))
print("Item records:", len(items))
print("RFQ records:", len(rfqs))
print("RFQ item records:", len(rfq_items))

print("\nRFQ Items:")
print(rfq_items.head())

print("\nData generation completed.")

# ============================================================
# 5. QUOTATIONS
# ============================================================

quotation_count = 1500

quotation_ids = [
    f"QUO{i:05d}" for i in range(1, quotation_count + 1)
]

quotation_rfq_ids = rng.choice(
    rfq_ids,
    quotation_count
)

quotation_supplier_ids = rng.choice(
    supplier_ids,
    quotation_count
)

quotation_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2024-01-01", "2026-09-10"),
        quotation_count
    )
)

valid_until_dates = quotation_dates + pd.to_timedelta(
    rng.integers(15, 90, quotation_count),
    unit="D"
)

currencies = rng.choice(
    ["INR", "INR", "INR", "USD"],
    quotation_count
)

payment_terms = rng.choice(
    [
        "Net 30",
        "Net 45",
        "Net 60",
        "Advance 30%",
        "50% Advance"
    ],
    quotation_count
)

quotation_status = rng.choice(
    ["Submitted", "Accepted", "Rejected", "Expired"],
    quotation_count
)

quotations = pd.DataFrame({
    "quotation_id": quotation_ids,
    "rfq_id": quotation_rfq_ids,
    "supplier_id": quotation_supplier_ids,
    "quotation_date": quotation_dates,
    "valid_until": valid_until_dates,
    "currency": currencies,
    "payment_terms": payment_terms,
    "status": quotation_status
})

# ============================================================
# 6. QUOTATION ITEMS
# ============================================================

quotation_item_count = 3500

quotation_item_ids = [
    f"QUOI{i:05d}"
    for i in range(1, quotation_item_count + 1)
]

quotation_item_quotation_ids = rng.choice(
    quotation_ids,
    quotation_item_count
)

quotation_item_rfq_item_ids = rng.choice(
    rfq_item_ids,
    quotation_item_count
)

unit_prices = np.round(
    rng.uniform(500, 150000, quotation_item_count),
    2
)

quantities_quoted = rng.integers(
    10,
    1000,
    quotation_item_count
)

delivery_days = rng.integers(
    5,
    90,
    quotation_item_count
)

warranty_months = rng.choice(
    [6, 12, 18, 24, 36],
    quotation_item_count
)

discount_percent = np.round(
    rng.uniform(0, 20, quotation_item_count),
    2
)

quotation_items = pd.DataFrame({
    "quotation_item_id": quotation_item_ids,
    "quotation_id": quotation_item_quotation_ids,
    "rfq_item_id": quotation_item_rfq_item_ids,
    "unit_price": unit_prices,
    "quantity_quoted": quantities_quoted,
    "delivery_days": delivery_days,
    "warranty_months": warranty_months,
    "discount_percent": discount_percent
})

# ============================================================
# 7. SAVE
# ============================================================

suppliers.to_csv("data/raw/suppliers.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)
rfqs.to_csv("data/raw/rfqs.csv", index=False)
rfq_items.to_csv("data/raw/rfq_items.csv", index=False)
quotations.to_csv("data/raw/quotations.csv", index=False)
quotation_items.to_csv(
    "data/raw/quotation_items.csv",
    index=False
)

print("Supplier records:", len(suppliers))
print("Item records:", len(items))
print("RFQ records:", len(rfqs))
print("RFQ item records:", len(rfq_items))
print("Quotation records:", len(quotations))
print("Quotation item records:", len(quotation_items))

print("\nQuotations:")
print(quotations.head())

print("\nQuotation Items:")
print(quotation_items.head())

print("\nData generation completed.")

# ============================================================
# 7. ORDERS
# ============================================================

order_count = 1000

order_ids = [
    f"ORD{i:05d}"
    for i in range(1, order_count + 1)
]

order_supplier_ids = rng.choice(
    supplier_ids,
    order_count
)

order_rfq_ids = rng.choice(
    rfq_ids,
    order_count
)

order_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2024-01-01", "2026-08-31"),
        order_count
    )
)

order_amounts = np.round(
    rng.uniform(10000, 5000000, order_count),
    2
)

order_currencies = rng.choice(
    ["INR", "INR", "INR", "USD"],
    order_count
)

order_status = rng.choice(
    ["Completed", "In Progress", "Cancelled"],
    order_count
)

orders = pd.DataFrame({
    "order_id": order_ids,
    "supplier_id": order_supplier_ids,
    "rfq_id": order_rfq_ids,
    "order_date": order_dates,
    "total_amount": order_amounts,
    "currency": order_currencies,
    "status": order_status
})
# ============================================================
# 8. ORDER ITEMS
# ============================================================

order_item_count = 2200

order_item_ids = [
    f"ORDI{i:05d}"
    for i in range(1, order_item_count + 1)
]

order_item_order_ids = rng.choice(
    order_ids,
    order_item_count
)

order_item_ids_selected = rng.choice(
    item_ids,
    order_item_count
)

quantities_ordered = rng.integers(
    10,
    1000,
    order_item_count
)

order_unit_prices = np.round(
    rng.uniform(500, 150000, order_item_count),
    2
)

total_prices = np.round(
    quantities_ordered * order_unit_prices,
    2
)

order_items = pd.DataFrame({
    "order_item_id": order_item_ids,
    "order_id": order_item_order_ids,
    "item_id": order_item_ids_selected,
    "quantity_ordered": quantities_ordered,
    "unit_price": order_unit_prices,
    "total_price": total_prices
})

# ============================================================
# 9. DELIVERIES
# ============================================================

delivery_count = 1000

delivery_ids = [
    f"DEL{i:05d}"
    for i in range(1, delivery_count + 1)
]

delivery_order_ids = rng.choice(
    order_ids,
    delivery_count
)

promised_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2024-02-01", "2026-09-30"),
        delivery_count
    )
)

delay_days = rng.choice(
    [0, 0, 0, 1, 2, 3, 5, 7, 10, 15, 30],
    delivery_count
)

actual_delivery_dates = (
    promised_dates
    + pd.to_timedelta(delay_days, unit="D")
)

quantity_ordered_delivery = rng.integers(
    10,
    1000,
    delivery_count
)

quantity_received = np.maximum(
    quantity_ordered_delivery
    - rng.integers(0, 30, delivery_count),
    0
)

delivery_status = np.where(
    actual_delivery_dates <= promised_dates,
    "On Time",
    "Late"
)

deliveries = pd.DataFrame({
    "delivery_id": delivery_ids,
    "order_id": delivery_order_ids,
    "promised_date": promised_dates,
    "actual_delivery_date": actual_delivery_dates,
    "quantity_ordered": quantity_ordered_delivery,
    "quantity_received": quantity_received,
    "delivery_status": delivery_status
})
# ============================================================
# 10. QUALITY
# ============================================================

quality_count = 1000

quality_ids = [
    f"QLT{i:05d}"
    for i in range(1, quality_count + 1)
]

quality_order_ids = rng.choice(
    order_ids,
    quality_count
)

inspection_dates = pd.to_datetime(
    rng.choice(
        pd.date_range("2024-02-01", "2026-09-30"),
        quality_count
    )
)

quantity_inspected = rng.integers(
    10,
    1000,
    quality_count
)

defect_rates = rng.uniform(
    0,
    0.15,
    quality_count
)

defective_quantity = (
    quantity_inspected * defect_rates
).astype(int)

quantity_accepted = (
    quantity_inspected - defective_quantity
)

quality_status = np.where(
    defective_quantity == 0,
    "Passed",
    np.where(
        defective_quantity / quantity_inspected < 0.05,
        "Minor Issues",
        "Failed"
    )
)

quality_notes = np.where(
    defective_quantity == 0,
    "No major quality issues",
    "Quality issues detected during inspection"
)

quality = pd.DataFrame({
    "quality_id": quality_ids,
    "order_id": quality_order_ids,
    "inspection_date": inspection_dates,
    "quantity_inspected": quantity_inspected,
    "quantity_accepted": quantity_accepted,
    "defective_quantity": defective_quantity,
    "quality_status": quality_status,
    "quality_notes": quality_notes
})

# ============================================================
# 11. SAVE ALL DATA
# ============================================================

suppliers.to_csv("data/raw/suppliers.csv", index=False)
items.to_csv("data/raw/items.csv", index=False)
rfqs.to_csv("data/raw/rfqs.csv", index=False)
rfq_items.to_csv("data/raw/rfq_items.csv", index=False)
quotations.to_csv("data/raw/quotations.csv", index=False)
quotation_items.to_csv(
    "data/raw/quotation_items.csv",
    index=False
)
orders.to_csv("data/raw/orders.csv", index=False)
order_items.to_csv(
    "data/raw/order_items.csv",
    index=False
)
deliveries.to_csv(
    "data/raw/deliveries.csv",
    index=False
)
quality.to_csv(
    "data/raw/quality.csv",
    index=False
)


print("\n==============================")
print("PROCUREMENT DATA GENERATED")
print("==============================")

print("Suppliers:", len(suppliers))
print("Items:", len(items))
print("RFQs:", len(rfqs))
print("RFQ Items:", len(rfq_items))
print("Quotations:", len(quotations))
print("Quotation Items:", len(quotation_items))
print("Orders:", len(orders))
print("Order Items:", len(order_items))
print("Deliveries:", len(deliveries))
print("Quality Records:", len(quality))

print("\nData generation completed.")

