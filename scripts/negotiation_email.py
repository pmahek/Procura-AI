import sys
import os


# ---------------------------------------------------------
# PATH SETUP
# ---------------------------------------------------------

SCRIPTS_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(0, SCRIPTS_DIR)


# ---------------------------------------------------------
# IMPORT PROCURA AI COMPONENTS
# ---------------------------------------------------------

from quotation_comparison import compare_quotations
from supplier_risk import calculate_supplier_risk
from decision_engine import calculate_decision_scores


# ---------------------------------------------------------
# NEGOTIATION EMAIL GENERATOR
# ---------------------------------------------------------

def generate_negotiation_email(rfq_id, supplier_id):

    quotations = compare_quotations(rfq_id)

    supplier_quotations = [
        quotation
        for quotation in quotations
        if quotation["supplier_id"] == supplier_id
    ]

    if not supplier_quotations:
        return {
            "status": "error",
            "message": (
                f"No quotation found for supplier "
                f"{supplier_id} in {rfq_id}"
            )
        }


    # -----------------------------------------------------
    # SUPPLIER INFORMATION
    # -----------------------------------------------------

    supplier_name = supplier_quotations[0][
        "supplier_name"
    ]


    # -----------------------------------------------------
    # QUOTATION METRICS
    # -----------------------------------------------------

    total_net_value = sum(
        quotation["net_value"]
        for quotation in supplier_quotations
    )

    average_delivery = sum(
        quotation["delivery_days"]
        for quotation in supplier_quotations
    ) / len(supplier_quotations)

    average_warranty = sum(
        quotation["warranty_months"]
        for quotation in supplier_quotations
    ) / len(supplier_quotations)

    discount = max(
        quotation["discount_percent"]
        for quotation in supplier_quotations
    )

    payment_terms = supplier_quotations[0][
        "payment_terms"
    ]


    # -----------------------------------------------------
    # SUPPLIER RISK
    # -----------------------------------------------------

    risk = calculate_supplier_risk(
        supplier_id
    )

    risk_level = risk["risk_level"]


    # -----------------------------------------------------
    # DECISION ENGINE
    # -----------------------------------------------------

    decisions = calculate_decision_scores(
        rfq_id
    )

    supplier_decision = next(
        (
            decision
            for decision in decisions
            if decision["supplier_id"] == supplier_id
        ),
        None
    )


    if supplier_decision:

        rank = supplier_decision["rank"]
        final_score = supplier_decision["final_score"]

    else:

        rank = None
        final_score = None


    # -----------------------------------------------------
    # NEGOTIATION POINTS
    # -----------------------------------------------------

    negotiation_points = []


    # Price negotiation
    negotiation_points.append(
        "Request improved pricing for the quoted items."
    )


    # Delivery negotiation
    if average_delivery > 10:

        negotiation_points.append(
            "Request a shorter delivery timeline."
        )


    # Warranty negotiation
    if average_warranty < 18:

        negotiation_points.append(
            "Request an extended warranty period."
        )


    # Discount negotiation
    if discount < 10:

        negotiation_points.append(
            "Request an improved volume discount."
        )


    # Payment terms
    if payment_terms:

        negotiation_points.append(
            "Request more favorable payment terms."
        )


    # Risk consideration
    if risk_level == "High":

        negotiation_points.append(
            "Request stronger delivery and quality commitments "
            "because supplier performance requires additional "
            "procurement consideration."
        )


    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    email_body = f"""
Subject: Request for Revised Commercial Terms — {rfq_id}

Dear {supplier_name} Team,

Thank you for submitting your quotation for {rfq_id}.

We have reviewed the quotation and would like to discuss
some commercial and delivery terms before proceeding.

Our current understanding of your quotation is:

- Total quoted value after discount: INR {total_net_value:,.2f}
- Average delivery time: {average_delivery:.1f} days
- Average warranty: {average_warranty:.1f} months
- Discount offered: {discount:.1f}%
- Payment terms: {payment_terms}

To help us move forward, could you please review the
following points and provide your best revised offer:

1. Improved pricing for the quoted items.
2. A shorter delivery timeline where possible.
3. An extended warranty period where possible.
4. An improved commercial discount.
5. More favorable payment terms, if available.

Please share your revised quotation and confirm the
updated commercial terms.

We look forward to your response.

Best regards,
Procurement Team
ProcuraAI
""".strip()


    # -----------------------------------------------------
    # RETURN NEGOTIATION PACKAGE
    # -----------------------------------------------------

    return {
        "status": "success",
        "rfq_id": rfq_id,
        "supplier_id": supplier_id,
        "supplier_name": supplier_name,
        "rank": rank,
        "final_score": final_score,
        "risk_level": risk_level,
        "risk_score": risk["risk_score"],
        "total_net_value": round(
            total_net_value,
            2
        ),
        "average_delivery_days": round(
            average_delivery,
            2
        ),
        "average_warranty_months": round(
            average_warranty,
            2
        ),
        "discount_percent": discount,
        "payment_terms": payment_terms,
        "negotiation_points": negotiation_points,
        "email": email_body
    }


# ---------------------------------------------------------
# HUMAN APPROVAL
# ---------------------------------------------------------

def request_human_approval(email_data):

    print()
    print("=" * 70)
    print("PROCURA AI — NEGOTIATION EMAIL")
    print("=" * 70)

    print()
    print("Supplier:", email_data["supplier_name"])
    print("RFQ:", email_data["rfq_id"])
    print("Supplier Rank:", email_data["rank"])
    print("Decision Score:", email_data["final_score"])
    print("Risk Level:", email_data["risk_level"])
    print("Risk Score:", email_data["risk_score"])

    print()
    print("-" * 70)
    print("DRAFT EMAIL")
    print("-" * 70)

    print()
    print(email_data["email"])

    print()
    print("-" * 70)
    print("HUMAN APPROVAL REQUIRED")
    print("-" * 70)

    while True:

        approval = input(
            "\nApprove this email? (yes/no/edit): "
        ).strip().lower()


        if approval == "yes":

            return {
                "status": "approved",
                "email": email_data["email"]
            }


        elif approval == "no":

            return {
                "status": "rejected",
                "email": email_data["email"]
            }


        elif approval == "edit":

            print()
            print("Enter the revised email.")
            print("Type END on a new line when finished.")
            print()

            lines = []

            while True:

                line = input()

                if line == "END":
                    break

                lines.append(line)


            revised_email = "\n".join(lines)

            return {
                "status": "edited",
                "email": revised_email
            }


        else:

            print(
                "Please enter yes, no, or edit."
            )


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    rfq_id = "RFQ0256"

    # Change this supplier when testing
    supplier_id = "SUP097"


    result = generate_negotiation_email(
        rfq_id,
        supplier_id
    )


    if result["status"] == "error":

        print(result["message"])

        sys.exit()


    approval_result = request_human_approval(
        result
    )


    print()
    print("=" * 70)
    print("NEGOTIATION WORKFLOW RESULT")
    print("=" * 70)

    print(
        f"Status: {approval_result['status']}"
    )

    print()
    print("Final Email:")
    print("-" * 70)

    print(
        approval_result["email"]
    )