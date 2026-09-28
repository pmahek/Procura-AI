from supplier_history import get_supplier_history


# ============================================================
# RISK THRESHOLDS
# ============================================================

LATE_DELIVERY_THRESHOLD = 0.50
DEFECT_RATE_THRESHOLD = 0.05
FULFILLMENT_THRESHOLD = 0.80


def calculate_supplier_risk(supplier_id):

    history = get_supplier_history(supplier_id)

    if history is None:
        return None

    late_delivery_rate = history["late_delivery_rate"]
    defect_rate = history["defect_rate"]
    fulfillment_rate = history["fulfillment_rate"]

    # --------------------------------------------------------
    # Calculate individual risk scores
    # --------------------------------------------------------

    late_risk = min(
        late_delivery_rate / LATE_DELIVERY_THRESHOLD,
        1
    )

    defect_risk = min(
        defect_rate / DEFECT_RATE_THRESHOLD,
        1
    )

    fulfillment_risk = min(
        max(
            (FULFILLMENT_THRESHOLD - fulfillment_rate)
            / FULFILLMENT_THRESHOLD,
            0
        ),
        1
    )

    # --------------------------------------------------------
    # Weighted risk score
    # --------------------------------------------------------

    risk_score = (
        late_risk * 0.50
        + defect_risk * 0.30
        + fulfillment_risk * 0.20
    )

    risk_score = round(
        risk_score * 100,
        2
    )

    # --------------------------------------------------------
    # Risk level
    # --------------------------------------------------------

    if risk_score < 30:
        risk_level = "Low"

    elif risk_score < 60:
        risk_level = "Medium"

    else:
        risk_level = "High"

    return {
        "supplier_id": supplier_id,
        "supplier_name": history["supplier_name"],
        "late_delivery_rate": late_delivery_rate,
        "defect_rate": defect_rate,
        "fulfillment_rate": fulfillment_rate,
        "risk_score": risk_score,
        "risk_level": risk_level,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    supplier_id = "SUP001"

    print("=" * 60)
    print("PROCURA AI — SUPPLIER RISK ASSESSMENT")
    print("=" * 60)

    result = calculate_supplier_risk(
        supplier_id
    )

    if result is None:

        print(
            f"No supplier found: {supplier_id}"
        )

    else:

        for key, value in result.items():

            print(
                f"{key}: {value}"
            )