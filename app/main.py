"""
API de clasificación de tickets de soporte.
Expone el agente L3 de AI Workflows como microservicio HTTP.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.classifier import classify_ticket
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Ticket Classifier API",
    description="Classifies support tickets using AI with tool use",
    version="1.0.0"
)


class TicketRequest(BaseModel):
    ticket: str


class TicketResponse(BaseModel):
    severity: str
    reason: str
    area: str
    requires_escalation: bool
    recommended_action: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify", response_model=TicketResponse)
def classify(request: TicketRequest):
    if not request.ticket.strip():
        raise HTTPException(status_code=400, detail="Ticket cannot be empty")
    try:
        result = classify_ticket(request.ticket)
        return TicketResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))