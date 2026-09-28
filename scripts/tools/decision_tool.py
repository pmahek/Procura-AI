import sys
import os

sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from decision_engine import calculate_decision_scores


def decision_tool(rfq_id):
    """
    Run the procurement decision engine
    for an RFQ.
    """

    decisions = calculate_decision_scores(rfq_id)

    if not decisions:
        return {
            "status": "error",
            "message": f"No decision data found for {rfq_id}"
        }

    return {
        "status": "success",
        "rfq_id": rfq_id,
        "decisions": decisions
    }


if __name__ == "__main__":

    result = decision_tool("RFQ0256")

    print("=" * 70)
    print("PROCURA AI — DECISION TOOL")
    print("=" * 70)

    print(f"Status: {result['status']}")
    print(f"RFQ: {result['rfq_id']}")

    print("\nSupplier Decisions:")

    for decision in result["decisions"]:

        print("-" * 70)

        print(
            f"Rank: {decision['rank']}"
        )

        print(
            f"Supplier: "
            f"{decision['supplier_name']}"
        )

        print(
            f"Final Score: "
            f"{decision['final_score']}"
        )

        print(
            f"Risk Level: "
            f"{decision['risk_level']}"
        )