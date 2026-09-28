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

from supplier_risk import calculate_supplier_risk


def risk_tool(supplier_id):
    """
    Calculate procurement risk for a supplier.
    """

    risk = calculate_supplier_risk(supplier_id)

    if not risk:
        return {
            "status": "error",
            "message": f"No supplier found: {supplier_id}"
        }

    return {
        "status": "success",
        "supplier_id": supplier_id,
        "risk": risk
    }


if __name__ == "__main__":

    result = risk_tool("SUP001")

    print("=" * 70)
    print("PROCURA AI — RISK TOOL")
    print("=" * 70)

    print(f"Status: {result['status']}")
    print(f"Supplier ID: {result['supplier_id']}")

    print("\nRisk Assessment:")

    for key, value in result["risk"].items():
        print(f"{key}: {value}")