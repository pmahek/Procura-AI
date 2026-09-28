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

from supplier_history import get_supplier_history


def supplier_tool(supplier_id):
    """
    Retrieve historical performance information
    for a supplier.
    """

    history = get_supplier_history(supplier_id)

    if not history:
        return {
            "status": "error",
            "message": f"No supplier found: {supplier_id}"
        }

    return {
        "status": "success",
        "supplier_id": supplier_id,
        "supplier": history
    }


if __name__ == "__main__":

    result = supplier_tool("SUP001")

    print("=" * 70)
    print("PROCURA AI — SUPPLIER TOOL")
    print("=" * 70)

    print(f"Status: {result['status']}")
    print(f"Supplier ID: {result['supplier_id']}")

    print("\nSupplier History:")

    for key, value in result["supplier"].items():
        print(f"{key}: {value}")