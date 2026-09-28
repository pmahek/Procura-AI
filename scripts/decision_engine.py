from quotation_comparison import compare_quotations
from supplier_history import get_supplier_history
from supplier_risk import calculate_supplier_risk


# ============================================================
# CONFIGURABLE BUSINESS WEIGHTS
# ============================================================

WEIGHTS = {
    "price": 0.30,
    "delivery": 0.20,
    "warranty": 0.15,
    "reliability": 0.15,
    "quality": 0.10,
    "risk": 0.10,
}


# ============================================================
# NORMALIZATION FUNCTIONS
# ============================================================

def normalize_lower_better(values):

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [100.0] * len(values)

    return [
        round(
            ((maximum - value) / (maximum - minimum)) * 100,
            2
        )
        for value in values
    ]


def normalize_higher_better(values):

    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [100.0] * len(values)

    return [
        round(
            ((value - minimum) / (maximum - minimum)) * 100,
            2
        )
        for value in values
    ]


# ============================================================
# DECISION ENGINE
# ============================================================

def calculate_decision_scores(rfq_id):

    quotations = compare_quotations(rfq_id)

    if not quotations:
        return []

    suppliers = {}

    # --------------------------------------------------------
    # 1. Aggregate quotation information
    # --------------------------------------------------------

    for quotation in quotations:

        supplier_id = quotation["supplier_id"]

        if supplier_id not in suppliers:

            suppliers[supplier_id] = {
                "quotation_id": quotation["quotation_id"],
                "supplier_id": supplier_id,
                "supplier_name": quotation["supplier_name"],
                "payment_terms": quotation["payment_terms"],
                "net_value": 0,
                "delivery_days": [],
                "warranty_months": [],
            }

        suppliers[supplier_id]["net_value"] += (
            quotation["net_value"]
        )

        suppliers[supplier_id]["delivery_days"].append(
            quotation["delivery_days"]
        )

        suppliers[supplier_id]["warranty_months"].append(
            quotation["warranty_months"]
        )

    supplier_list = list(suppliers.values())

    # --------------------------------------------------------
    # 2. Convert quotation data to supplier-level metrics
    # --------------------------------------------------------

    for supplier in supplier_list:

        supplier["net_value"] = round(
            supplier["net_value"],
            2
        )

        supplier["delivery_days"] = round(
            sum(supplier["delivery_days"])
            / len(supplier["delivery_days"]),
            2
        )

        supplier["warranty_months"] = round(
            sum(supplier["warranty_months"])
            / len(supplier["warranty_months"]),
            2
        )

    # --------------------------------------------------------
    # 3. Retrieve supplier history + risk
    # --------------------------------------------------------

    for supplier in supplier_list:

        history = get_supplier_history(
            supplier["supplier_id"]
        )

        risk = calculate_supplier_risk(
            supplier["supplier_id"]
        )

        if history:

            supplier["late_delivery_rate"] = (
                history["late_delivery_rate"]
            )

            supplier["fulfillment_rate"] = (
                history["fulfillment_rate"]
            )

            supplier["defect_rate"] = (
                history["defect_rate"]
            )

        else:

            supplier["late_delivery_rate"] = 0
            supplier["fulfillment_rate"] = 0
            supplier["defect_rate"] = 0

        if risk:

            supplier["risk_score"] = risk["risk_score"]

            supplier["risk_level"] = risk["risk_level"]

        else:

            supplier["risk_score"] = 50.0

            supplier["risk_level"] = "Unknown"

    # --------------------------------------------------------
    # 4. Create comparison scores
    # --------------------------------------------------------

    prices = [
        supplier["net_value"]
        for supplier in supplier_list
    ]

    deliveries = [
        supplier["delivery_days"]
        for supplier in supplier_list
    ]

    warranties = [
        supplier["warranty_months"]
        for supplier in supplier_list
    ]

    late_rates = [
        supplier["late_delivery_rate"]
        for supplier in supplier_list
    ]

    defect_rates = [
        supplier["defect_rate"]
        for supplier in supplier_list
    ]

    risk_scores = [
        supplier["risk_score"]
        for supplier in supplier_list
    ]

    # --------------------------------------------------------
    # Lower is better
    # --------------------------------------------------------

    price_scores = normalize_lower_better(prices)

    delivery_scores = normalize_lower_better(
        deliveries
    )

    reliability_scores = normalize_lower_better(
        late_rates
    )

    quality_scores = normalize_lower_better(
        defect_rates
    )

    risk_component_scores = normalize_lower_better(
        risk_scores
    )

    # --------------------------------------------------------
    # Higher is better
    # --------------------------------------------------------

    warranty_scores = normalize_higher_better(
        warranties
    )

    # --------------------------------------------------------
    # 5. Calculate final weighted score
    # --------------------------------------------------------

    for index, supplier in enumerate(supplier_list):

        supplier["price_score"] = price_scores[index]

        supplier["delivery_score"] = (
            delivery_scores[index]
        )

        supplier["warranty_score"] = (
            warranty_scores[index]
        )

        supplier["reliability_score"] = (
            reliability_scores[index]
        )

        supplier["quality_score"] = (
            quality_scores[index]
        )

        supplier["risk_component_score"] = (
            risk_component_scores[index]
        )

        supplier["final_score"] = round(

            supplier["price_score"]
            * WEIGHTS["price"]

            + supplier["delivery_score"]
            * WEIGHTS["delivery"]

            + supplier["warranty_score"]
            * WEIGHTS["warranty"]

            + supplier["reliability_score"]
            * WEIGHTS["reliability"]

            + supplier["quality_score"]
            * WEIGHTS["quality"]

            + supplier["risk_component_score"]
            * WEIGHTS["risk"],

            2
        )

    # --------------------------------------------------------
    # 6. Sort by final score
    # --------------------------------------------------------

    supplier_list.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    # --------------------------------------------------------
    # 7. Generate explanations
    # --------------------------------------------------------

    for position, supplier in enumerate(
        supplier_list,
        start=1
    ):

        supplier["rank"] = position

        reasons = []

        if supplier["price_score"] >= 75:
            reasons.append(
                "competitive quotation price"
            )

        if supplier["delivery_score"] >= 75:
            reasons.append(
                "strong quoted delivery performance"
            )

        if supplier["warranty_score"] >= 75:
            reasons.append(
                "strong warranty coverage"
            )

        if supplier["reliability_score"] >= 75:
            reasons.append(
                "good historical delivery reliability"
            )

        if supplier["quality_score"] >= 75:
            reasons.append(
                "good historical quality performance"
            )

        if supplier["risk_level"] == "Low":
            reasons.append(
                "low historical supplier risk"
            )

        elif supplier["risk_level"] == "High":
            reasons.append(
                "high historical supplier risk"
            )

        supplier["reasons"] = reasons

    return supplier_list


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    rfq_id = "RFQ0256"

    print("=" * 70)
    print("PROCURA AI — RISK-AWARE DECISION ENGINE")
    print("=" * 70)
    print(f"RFQ: {rfq_id}")

    results = calculate_decision_scores(
        rfq_id
    )

    if not results:

        print("No supplier quotations found.")

    else:

        for supplier in results:

            print("-" * 70)

            print(
                f"Rank: {supplier['rank']}"
            )

            print(
                f"Supplier: "
                f"{supplier['supplier_name']}"
            )

            print(
                f"Net Value: "
                f"{supplier['net_value']}"
            )

            print(
                f"Delivery: "
                f"{supplier['delivery_days']} days"
            )

            print(
                f"Warranty: "
                f"{supplier['warranty_months']} months"
            )

            print(
                f"Late Delivery Rate: "
                f"{supplier['late_delivery_rate']}"
            )

            print(
                f"Defect Rate: "
                f"{supplier['defect_rate']}"
            )

            print(
                f"Risk Score: "
                f"{supplier['risk_score']}"
            )

            print(
                f"Risk Level: "
                f"{supplier['risk_level']}"
            )

            print()

            print(
                f"Price Score: "
                f"{supplier['price_score']}"
            )

            print(
                f"Delivery Score: "
                f"{supplier['delivery_score']}"
            )

            print(
                f"Warranty Score: "
                f"{supplier['warranty_score']}"
            )

            print(
                f"Reliability Score: "
                f"{supplier['reliability_score']}"
            )

            print(
                f"Quality Score: "
                f"{supplier['quality_score']}"
            )

            print(
                f"Risk Score Component: "
                f"{supplier['risk_component_score']}"
            )

            print()

            print(
                f"FINAL SCORE: "
                f"{supplier['final_score']}"
            )

            print(
                "Reasons: "
                + (
                    ", ".join(
                        supplier["reasons"]
                    )
                    if supplier["reasons"]
                    else "No strong positive factors"
                )
            )