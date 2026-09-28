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

from quotation_comparison import compare_quotations


def quotation_tool(rfq_id):
    """
    Compare supplier quotations for an RFQ.
    """

    quotations = compare_quotations(rfq_id)

    if not quotations:
        return {
            "status": "error",
            "message": f"No quotations found for {rfq_id}"
        }

    return {
        "status": "success",
        "rfq_id": rfq_id,
        "quotation_count": len(quotations),
        "quotations": quotations
    }


if __name__ == "__main__":

    result = quotation_tool("RFQ0256")

    print("=" * 70)
    print("PROCURA AI — QUOTATION TOOL")
    print("=" * 70)

    print(f"Status: {result['status']}")
    print(f"RFQ: {result['rfq_id']}")
    print(f"Quotation records: {result['quotation_count']}")