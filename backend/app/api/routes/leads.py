import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.models.lead import Lead, LeadStatus
from app.schemas.lead import LeadApprove, LeadRead
from app.services.email.resend_client import EmailSender

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("", response_model=list[LeadRead])
async def list_leads(
    status: LeadStatus | None = None, db: AsyncSession = Depends(get_db)
) -> list[Lead]:
    query = select(Lead).order_by(Lead.score.desc())
    if status:
        query = query.where(Lead.status == status)
    result = await db.execute(query)
    return list(result.scalars().all())


@router.post("/{lead_id}/review", response_model=LeadRead)
async def review_lead(
    lead_id: uuid.UUID, decision: LeadApprove, db: AsyncSession = Depends(get_db)
) -> Lead:
    """Aprova ou rejeita um rascunho de email pendente de revisão humana."""
    lead = await db.get(Lead, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    if lead.status != LeadStatus.PENDING_REVIEW:
        raise HTTPException(status_code=409, detail="Lead não está pendente de revisão")

    if not decision.approved:
        lead.status = LeadStatus.REJECTED
        await db.commit()
        return lead

    settings = get_settings()
    if lead.email:
        sender = EmailSender(settings.resend_api_key, settings.email_from)
        sender.send(lead.email, f"Café em grão para {lead.name}", lead.outreach_draft or "")

    lead.status = LeadStatus.SENT
    await db.commit()
    return lead
