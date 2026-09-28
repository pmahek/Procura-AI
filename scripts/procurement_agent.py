from quotation_comparison import compare_quotations
from supplier_history import get_supplier_history
from supplier_risk import calculate_supplier_risk
from decision_engine import calculate_decision_scores
from rag import build_context, generate_answer


def analyze_rfq(rfq_id):
    """
    Orchestrates the ProcuraAI procurement analysis workflow.
    """

    print("=" * 70)
    print("PROCURA AI — PROCUREMENT AGENT")
    print("=" * 70)
    print(f"RFQ: {rfq_id}")
    print()

    # ---------------------------------------------------------
    # 1. QUOTATION ANALYSIS
    # ---------------------------------------------------------

    print("Step 1: Comparing supplier quotations...")

    quotations = compare_quotations(rfq_id)

    if not quotations:
        return {
            "status": "error",
            "message": f"No quotations found for {rfq_id}"
        }

    print(f"Found {len(quotations)} quotation records.")
    print()

    # ---------------------------------------------------------
    # 2. SUPPLIER ANALYSIS
    # ---------------------------------------------------------

    print("Step 2: Analyzing supplier history and risk...")

    supplier_ids = list({
        quotation["supplier_id"]
        for quotation in quotations
    })

    supplier_analysis = []

    for supplier_id in supplier_ids:

        history = get_supplier_history(
            supplier_id
        )

        risk = calculate_supplier_risk(
            supplier_id
        )

        supplier_analysis.append({
            "supplier_id": supplier_id,
            "history": history,
            "risk": risk
        })

    print(
        f"Analyzed {len(supplier_analysis)} suppliers."
    )
    print()

    # ---------------------------------------------------------
    # 3. DECISION ENGINE
    # ---------------------------------------------------------

    print(
        "Step 3: Running procurement decision engine..."
    )

    decisions = calculate_decision_scores(
        rfq_id
    )

    print("Decision engine completed.")
    print()

    # ---------------------------------------------------------
    # 4. DOCUMENT / RAG ANALYSIS
    # ---------------------------------------------------------

    print("Step 4: Checking procurement documents...")

    document_question = (
        f"What quotation terms, payment terms, discounts, "
        f"delivery conditions, and warranty information are "
        f"available for {rfq_id}?"
    )

    document_context = build_context(
        query=document_question,
        top_k=3
    )

    document_analysis = generate_answer(
        query=document_question,
        context=document_context
    )

    print("Document analysis completed.")
    print()

    # ---------------------------------------------------------
    # 5. FINAL RESULT
    # ---------------------------------------------------------

    return {
        "status": "success",
        "rfq_id": rfq_id,
        "quotations": quotations,
        "supplier_analysis": supplier_analysis,
        "decisions": decisions,
        "document_analysis": document_analysis
    }


# =============================================================
# TEST
# =============================================================

if __name__ == "__main__":

    rfq_id = "RFQ0256"

    result = analyze_rfq(
        rfq_id
    )

    print("=" * 70)
    print("PROCUREMENT ANALYSIS COMPLETE")
    print("=" * 70)

    print(
        f"Status: {result['status']}"
    )

    print(
        f"RFQ: {result['rfq_id']}"
    )

    print()
    print("Suppliers analyzed:")

    for supplier in result["supplier_analysis"]:

        risk = supplier["risk"]

        print(
            f"- {supplier['supplier_id']} | "
            f"Risk: {risk['risk_level']} | "
            f"Score: {risk['risk_score']}"
        )