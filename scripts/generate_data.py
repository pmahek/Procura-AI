import os
import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

RAW_DATA_DIR = "data/raw"
os.makedirs(RAW_DATA_DIR, exist_ok=True)


# ============================================================
# 1. SUPPLIERS
# ============================================================

supplier_count = 100

supplier_ids = [
    f"SUP{i:03d}"
    for i in range(1, supplier_count + 1)
]

supplier_names = [
    f"{prefix} {suffix}"
    for prefix, suffix in zip(
        rng.choice(
            [
                "Apex",
                "Global",
                "Prime",
                "Metro",
                "United",
                "Reliable",
                "Eastern",
                "Western",
                "National",
                "Dynamic",
            ],
            supplier_count,
        ),
        rng.choice(
            [
                "Industries",
                "Solutions",
                "Supplies",
                "Enterprises",
                "Corporation",
                "Technologies",
                "Traders",
                "Systems",
            ],
            supplier_count,
        ),
    )
]

categories = [
    "IT Equipment",
    "Office Supplies",
    "Industrial",
    "Electrical",
    "Packaging",
    "Safety Equipment",
]

locations = [
    "Bangalore",
    "Mumbai",
    "Pune",
    "Delhi",
    "Hyderabad",
    "Chennai",
    "Ahmedabad",
]

suppliers = pd.DataFrame(
    {
        "supplier_id": supplier_ids,
        "supplier_name": supplier_names,
        "category": rng.choice(categories, supplier_count),
        "location": rng.choice(locations, supplier_count),
        "years_in_business": rng.integers(
            1,
            31,
            supplier_count,
        ),
        "status": rng.choice(
            ["Active", "Inactive"],
            supplier_count,
            p=[0.9, 0.1],
        ),
        "created_date": pd.to_datetime(
            rng.choice(
                pd.date_range(
                    "1995-01-01",
                    "2024-12-31",
                ),
                supplier_count,
            )
        ),
    }
)


# ============================================================
# 2. ITEMS
# ============================================================

item_count = 50

item_ids = [
    f"ITEM{i:03d}"
    for i in range(1, item_count + 1)
]

item_categories = [
    "IT Equipment",
    "Office Supplies",
    "Electrical",
    "Industrial",
    "Safety Equipment",
]

units = [
    "Piece",
    "Box",
    "Kg",
    "Set",
    "Pack",
]

items = pd.DataFrame(
    {
        "item_id": item_ids,
        "item_name": [
            f"Item {i}"
            for i in range(1, item_count + 1)
        ],
        "category": rng.choice(
            item_categories,
            item_count,
        ),
        "unit_of_measure": rng.choice(
            units,
            item_count,
        ),
        "description": [
            f"Procurement item {i}"
            for i in range(1, item_count + 1)
        ],
        "specifications": [
            f"Standard specification for item {i}"
            for i in range(1, item_count + 1)
        ],
    }
)


# ============================================================
# 3. RFQs
# ============================================================

rfq_count = 500

rfq_ids = [
    f"RFQ{i:04d}"
    for i in range(1, rfq_count + 1)
]

rfq_dates = pd.to_datetime(
    rng.choice(
        pd.date_range(
            "2024-01-01",
            "2026-08-31",
        ),
        rfq_count,
    )
)

required_delivery_dates = (
    rfq_dates
    + pd.to_timedelta(
        rng.integers(
            15,
            91,
            rfq_count,
        ),
        unit="D",
    )
)

rfqs = pd.DataFrame(
    {
        "rfq_id": rfq_ids,
        "rfq_date": rfq_dates,
        "department": rng.choice(
            [
                "IT",
                "Finance",
                "HR",
                "Operations",
                "Procurement",
                "Marketing",
            ],
            rfq_count,
        ),
        "required_delivery_date": required_delivery_dates,
        "status": rng.choice(
            [
                "Open",
                "Closed",
                "Awarded",
                "Cancelled",
            ],
            rfq_count,
        ),
        "description": [
            f"Procurement request for {rfq_id}"
            for rfq_id in rfq_ids
        ],
    }
)


# ============================================================
# 4. RFQ ITEMS
# ============================================================

rfq_item_count = 1200

rfq_item_ids = [
    f"RFQI{i:04d}"
    for i in range(1, rfq_item_count + 1)
]

# Guarantee that every RFQ has at least one item.

required_rfq_ids = rfqs["rfq_id"].tolist()

remaining_count = (
    rfq_item_count
    - len(required_rfq_ids)
)

additional_rfq_ids = rng.choice(
    required_rfq_ids,
    remaining_count,
)

rfq_item_rfq_ids = (
    required_rfq_ids
    + additional_rfq_ids.tolist()
)

rng.shuffle(rfq_item_rfq_ids)

rfq_items = pd.DataFrame(
    {
        "rfq_item_id": rfq_item_ids,
        "rfq_id": rfq_item_rfq_ids,
        "item_id": rng.choice(
            item_ids,
            rfq_item_count,
        ),
        "quantity": rng.integers(
            1,
            501,
            rfq_item_count,
        ),
    }
)


# ============================================================
# RFQ ITEM VALIDATION
# ============================================================

rfq_item_counts = (
    rfq_items.groupby("rfq_id")
    .size()
)

missing_rfqs = [
    rfq_id
    for rfq_id in rfq_ids
    if rfq_id not in rfq_item_counts.index
]

if missing_rfqs:
    raise ValueError(
        f"These RFQs have no items: {missing_rfqs}"
    )


# ============================================================
# 5. QUOTATIONS
# ============================================================

quotation_count = 1500

quotation_ids = [
    f"QUO{i:04d}"
    for i in range(1, quotation_count + 1)
]

quotation_rfq_ids = rng.choice(
    rfq_ids,
    quotation_count,
)

quotation_supplier_ids = rng.choice(
    supplier_ids,
    quotation_count,
)

quotation_dates = pd.to_datetime(
    rng.choice(
        pd.date_range(
            "2024-01-01",
            "2026-09-10",
        ),
        quotation_count,
    )
)

valid_until_dates = (
    quotation_dates
    + pd.to_timedelta(
        rng.integers(
            15,
            91,
            quotation_count,
        ),
        unit="D",
    )
)

quotations = pd.DataFrame(
    {
        "quotation_id": quotation_ids,
        "rfq_id": quotation_rfq_ids,
        "supplier_id": quotation_supplier_ids,
        "quotation_date": quotation_dates,
        "valid_until": valid_until_dates,
        "currency": rng.choice(
            ["INR", "USD"],
            quotation_count,
            p=[0.9, 0.1],
        ),
        "payment_terms": rng.choice(
            [
                "Net 15",
                "Net 30",
                "Net 45",
                "Net 60",
            ],
            quotation_count,
        ),
        "status": rng.choice(
            [
                "Submitted",
                "Accepted",
                "Rejected",
                "Expired",
            ],
            quotation_count,
        ),
    }
)


# ============================================================
# 6. QUOTATION ITEMS
# ============================================================

quotation_item_count = 3500

quotation_item_ids = [
    f"QUOI{i:04d}"
    for i in range(1, quotation_item_count + 1)
]

# RFQ -> RFQ items
rfq_to_items = (
    rfq_items
    .groupby("rfq_id")["rfq_item_id"]
    .apply(list)
    .to_dict()
)

# Quotation -> RFQ
quotation_to_rfq = dict(
    zip(
        quotations["quotation_id"],
        quotations["rfq_id"],
    )
)

quotation_item_quotation_ids = rng.choice(
    quotation_ids,
    quotation_item_count,
)

quotation_item_rfq_item_ids = []

for quotation_id in quotation_item_quotation_ids:

    rfq_id = quotation_to_rfq[quotation_id]

    available_rfq_items = rfq_to_items[rfq_id]

    selected_rfq_item = rng.choice(
        available_rfq_items
    )

    quotation_item_rfq_item_ids.append(
        selected_rfq_item
    )


quotation_items = pd.DataFrame(
    {
        "quotation_item_id": quotation_item_ids,
        "quotation_id": quotation_item_quotation_ids,
        "rfq_item_id": quotation_item_rfq_item_ids,
        "unit_price": np.round(
            rng.uniform(
                100,
                100000,
                quotation_item_count,
            ),
            2,
        ),
        "quantity_quoted": rng.integers(
            1,
            501,
            quotation_item_count,
        ),
        "delivery_days": rng.integers(
            5,
            121,
            quotation_item_count,
        ),
        "warranty_months": rng.integers(
            0,
            61,
            quotation_item_count,
        ),
        "discount_percent": np.round(
            rng.uniform(
                0,
                25,
                quotation_item_count,
            ),
            2,
        ),
    }
)


# ============================================================
# QUOTATION RELATIONSHIP VALIDATION
# ============================================================

quotation_item_check = quotation_items.merge(
    quotations[
        [
            "quotation_id",
            "rfq_id",
        ]
    ],
    on="quotation_id",
    how="left",
)

quotation_item_check = quotation_item_check.merge(
    rfq_items[
        [
            "rfq_item_id",
            "rfq_id",
        ]
    ],
    on="rfq_item_id",
    how="left",
    suffixes=(
        "_quotation",
        "_item",
    ),
)

relationship_errors = quotation_item_check[
    quotation_item_check["rfq_id_quotation"]
    != quotation_item_check["rfq_id_item"]
]

if len(relationship_errors) > 0:
    raise ValueError(
        "Quotation/RFQ relationship errors: "
        f"{len(relationship_errors)}"
    )


# ============================================================
# 7. ORDERS
# ============================================================

order_count = 1000

order_ids = [
    f"ORD{i:04d}"
    for i in range(1, order_count + 1)
]

orders = pd.DataFrame(
    {
        "order_id": order_ids,
        "supplier_id": rng.choice(
            supplier_ids,
            order_count,
        ),
        "rfq_id": rng.choice(
            rfq_ids,
            order_count,
        ),
        "order_date": pd.to_datetime(
            rng.choice(
                pd.date_range(
                    "2024-01-01",
                    "2026-08-31",
                ),
                order_count,
            )
        ),
        "total_amount": np.round(
            rng.uniform(
                5000,
                500000,
                order_count,
            ),
            2,
        ),
        "currency": rng.choice(
            ["INR", "USD"],
            order_count,
            p=[0.9, 0.1],
        ),
        "status": rng.choice(
            [
                "Created",
                "Approved",
                "Completed",
                "Cancelled",
            ],
            order_count,
        ),
    }
)


# ============================================================
# 8. ORDER ITEMS
# ============================================================

order_item_count = 2200

order_item_ids = [
    f"ORDI{i:04d}"
    for i in range(1, order_item_count + 1)
]

order_items = pd.DataFrame(
    {
        "order_item_id": order_item_ids,
        "order_id": rng.choice(
            order_ids,
            order_item_count,
        ),
        "item_id": rng.choice(
            item_ids,
            order_item_count,
        ),
        "quantity_ordered": rng.integers(
            1,
            501,
            order_item_count,
        ),
        "unit_price": np.round(
            rng.uniform(
                100,
                100000,
                order_item_count,
            ),
            2,
        ),
        "total_price": np.round(
            rng.uniform(
                100,
                500000,
                order_item_count,
            ),
            2,
        ),
    }
)


# ============================================================
# 9. DELIVERIES
# ============================================================

# Exactly one delivery per order.

delivery_count = len(orders)

delivery_ids = [
    f"DEL{i:04d}"
    for i in range(1, delivery_count + 1)
]

delivery_order_ids = orders[
    "order_id"
].tolist()

promised_dates = (
    pd.to_datetime(orders["order_date"])
    + pd.to_timedelta(
        rng.integers(
            15,
            91,
            delivery_count,
        ),
        unit="D",
    )
)

delay_days = rng.choice(
    [
        0,
        0,
        0,
        1,
        2,
        3,
        5,
        7,
        10,
        15,
        20,
    ],
    delivery_count,
)

actual_delivery_dates = (
    promised_dates
    + pd.to_timedelta(
        delay_days,
        unit="D",
    )
)

delivery_quantity_ordered = rng.integers(
    1,
    501,
    delivery_count,
)

# Make received quantity logically valid:
# it cannot exceed quantity ordered.

delivery_quantity_received = np.array(
    [
        rng.integers(
            1,
            quantity + 1,
        )
        for quantity in delivery_quantity_ordered
    ]
)

deliveries = pd.DataFrame(
    {
        "delivery_id": delivery_ids,
        "order_id": delivery_order_ids,
        "promised_date": promised_dates,
        "actual_delivery_date": actual_delivery_dates,
        "quantity_ordered": delivery_quantity_ordered,
        "quantity_received": delivery_quantity_received,
        "delivery_status": [
            "On Time"
            if delay == 0
            else "Late"
            for delay in delay_days
        ],
    }
)


# ============================================================
# 10. QUALITY
# ============================================================

# Exactly one quality record per order.

quality_count = len(orders)

quality_ids = [
    f"QUAL{i:04d}"
    for i in range(1, quality_count + 1)
]

quality_order_ids = orders[
    "order_id"
].tolist()

# Generate inspected quantity first.
quantity_inspected = rng.integers(
    1,
    501,
    quality_count,
)

# Generate defects based on the inspected quantity.
# Therefore:
#
# defective_quantity <= quantity_inspected

defective_quantity = np.array(
    [
        rng.integers(
            0,
            min(quantity, 20) + 1,
        )
        for quantity in quantity_inspected
    ]
)

# Accepted quantity is always:
#
# inspected - defective

quantity_accepted = (
    quantity_inspected
    - defective_quantity
)

quality = pd.DataFrame(
    {
        "quality_id": quality_ids,
        "order_id": quality_order_ids,
        "inspection_date": pd.to_datetime(
            rng.choice(
                pd.date_range(
                    "2024-01-01",
                    "2026-09-15",
                ),
                quality_count,
            )
        ),
        "quantity_inspected": quantity_inspected,
        "quantity_accepted": quantity_accepted,
        "defective_quantity": defective_quantity,
        "quality_status": [
            "Passed"
            if defect == 0
            else "Passed with Issues"
            if defect <= 5
            else "Failed"
            for defect in defective_quantity
        ],
        "quality_notes": [
            "Routine quality inspection"
            for _ in range(quality_count)
        ],
    }
)


# ============================================================
# 11. FINAL VALIDATION
# ============================================================

print("\nRunning validation checks...")


# ------------------------------------------------------------
# Primary key uniqueness
# ------------------------------------------------------------

assert suppliers["supplier_id"].is_unique
assert items["item_id"].is_unique
assert rfqs["rfq_id"].is_unique
assert rfq_items["rfq_item_id"].is_unique
assert quotations["quotation_id"].is_unique
assert quotation_items["quotation_item_id"].is_unique
assert orders["order_id"].is_unique
assert order_items["order_item_id"].is_unique
assert deliveries["delivery_id"].is_unique
assert quality["quality_id"].is_unique


# ------------------------------------------------------------
# RFQ item coverage
# ------------------------------------------------------------

assert set(
    rfqs["rfq_id"]
) == set(
    rfq_items["rfq_id"]
)


# ------------------------------------------------------------
# Quotation relationships
# ------------------------------------------------------------

assert set(
    quotations["rfq_id"]
).issubset(
    set(rfqs["rfq_id"])
)

assert set(
    quotations["supplier_id"]
).issubset(
    set(suppliers["supplier_id"])
)

assert set(
    quotation_items["quotation_id"]
).issubset(
    set(quotations["quotation_id"])
)

assert set(
    quotation_items["rfq_item_id"]
).issubset(
    set(rfq_items["rfq_item_id"])
)

assert len(relationship_errors) == 0


# ------------------------------------------------------------
# Delivery relationships
# ------------------------------------------------------------

assert set(
    deliveries["order_id"]
) == set(
    orders["order_id"]
)

assert (
    deliveries["order_id"].nunique()
    == len(orders)
)

assert (
    deliveries["quantity_received"]
    <= deliveries["quantity_ordered"]
).all()


# ------------------------------------------------------------
# Quality relationships
# ------------------------------------------------------------

assert set(
    quality["order_id"]
) == set(
    orders["order_id"]
)

assert (
    quality["order_id"].nunique()
    == len(orders)
)


# ------------------------------------------------------------
# Quality quantity validation
# ------------------------------------------------------------

assert (
    quality["quantity_accepted"]
    <= quality["quantity_inspected"]
).all()

assert (
    quality["defective_quantity"]
    <= quality["quantity_inspected"]
).all()

assert (
    quality["quantity_accepted"]
    + quality["defective_quantity"]
    == quality["quantity_inspected"]
).all()


print("All validation checks passed.")


# ============================================================
# 12. SAVE DATASETS
# ============================================================

suppliers.to_csv(
    f"{RAW_DATA_DIR}/suppliers.csv",
    index=False,
)

items.to_csv(
    f"{RAW_DATA_DIR}/items.csv",
    index=False,
)

rfqs.to_csv(
    f"{RAW_DATA_DIR}/rfqs.csv",
    index=False,
)

rfq_items.to_csv(
    f"{RAW_DATA_DIR}/rfq_items.csv",
    index=False,
)

quotations.to_csv(
    f"{RAW_DATA_DIR}/quotations.csv",
    index=False,
)

quotation_items.to_csv(
    f"{RAW_DATA_DIR}/quotation_items.csv",
    index=False,
)

orders.to_csv(
    f"{RAW_DATA_DIR}/orders.csv",
    index=False,
)

order_items.to_csv(
    f"{RAW_DATA_DIR}/order_items.csv",
    index=False,
)

deliveries.to_csv(
    f"{RAW_DATA_DIR}/deliveries.csv",
    index=False,
)

quality.to_csv(
    f"{RAW_DATA_DIR}/quality.csv",
    index=False,
)


# ============================================================
# 13. FINAL SUMMARY
# ============================================================

print("\nData generation completed successfully.")
print()
print("Generated datasets:")
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
print()
print(f"Files saved to: {RAW_DATA_DIR}")