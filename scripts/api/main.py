import sys
import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

SCRIPTS_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, SCRIPTS_DIR)


# ---------------------------------------------------------
# IMPORT PROCURA AI COMPONENTS
# ---------------------------------------------------------

from procurement_agent import analyze_rfq
from supplier_history import get_supplier_history
from supplier_risk import calculate_supplier_risk
from quotation_comparison import compare_quotations
from decision_engine import calculate_decision_scores
from negotiation_email import generate_negotiation_email


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title="ProcuraAI API",
    description="AI-powered procurement decision-support API.",
    version="1.0.0"
)


# ---------------------------------------------------------
# REQUEST MODELS
# ---------------------------------------------------------

class RFQRequest(BaseModel):
    rfq_id: str


class NegotiationRequest(BaseModel):
    rfq_id: str
    supplier_id: str


# ---------------------------------------------------------
# ROOT
# ---------------------------------------------------------

@app.get("/")
def root():

    return {
        "application": "ProcuraAI",
        "status": "running",
        "version": "1.0.0"
    }


# ---------------------------------------------------------
# SUPPLIER HISTORY
# ---------------------------------------------------------

@app.get("/supplier/{supplier_id}")
def supplier_endpoint(supplier_id: str):

    result = get_supplier_history(supplier_id)

    if result is None:

        raise HTTPException(
            status_code=404,
            detail=f"Supplier {supplier_id} not found."
        )

    return {
        "status": "success",
        "supplier": result
    }


# ---------------------------------------------------------
# SUPPLIER RISK
# ---------------------------------------------------------

@app.get("/risk/{supplier_id}")
def risk_endpoint(supplier_id: str):

    result = calculate_supplier_risk(
        supplier_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail=f"Supplier {supplier_id} not found."
        )

    return result


# ---------------------------------------------------------
# QUOTATION COMPARISON
# ---------------------------------------------------------

@app.get("/quotations/{rfq_id}")
def quotations_endpoint(rfq_id: str):

    result = compare_quotations(
        rfq_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail=f"No quotations found for {rfq_id}."
        )

    return {
        "status": "success",
        "rfq_id": rfq_id,
        "quotation_count": len(result),
        "quotations": result
    }


# ---------------------------------------------------------
# DECISION ENGINE
# ---------------------------------------------------------

@app.get("/decision/{rfq_id}")
def decision_endpoint(rfq_id: str):

    result = calculate_decision_scores(
        rfq_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail=f"No decision data found for {rfq_id}."
        )

    return {
        "status": "success",
        "rfq_id": rfq_id,
        "decisions": result
    }


# ---------------------------------------------------------
# COMPLETE RFQ ANALYSIS
# ---------------------------------------------------------

@app.post("/analyze-rfq")
def analyze_rfq_endpoint(
    request: RFQRequest
):

    result = analyze_rfq(
        request.rfq_id
    )

    if result["status"] == "error":

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result


# ---------------------------------------------------------
# NEGOTIATION EMAIL
# ---------------------------------------------------------

@app.post("/negotiation-email")
def negotiation_email_endpoint(
    request: NegotiationRequest
):

    result = generate_negotiation_email(
        request.rfq_id,
        request.supplier_id
    )

    if result["status"] == "error":

        raise HTTPException(
            status_code=404,
            detail=result["message"]
        )

    return result