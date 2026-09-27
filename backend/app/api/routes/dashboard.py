from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.lead import Lead, LeadStatus

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/metrics")
async def get_metrics(db: AsyncSession = Depends(get_db)) -> dict:
    total = await db.scalar(select(func.count(Lead.id)))
    by_status_result = await db.execute(
        select(Lead.status, func.count(Lead.id)).group_by(Lead.status)
    )
    by_status = {status.value: count for status, count in by_status_result.all()}
    avg_score = await db.scalar(select(func.avg(Lead.score)))

    return {
        "total_leads": total or 0,
        "by_status": by_status,
        "average_score": round(avg_score, 1) if avg_score else 0,
        "pending_review": by_status.get(LeadStatus.PENDING_REVIEW.value, 0),
        "sent": by_status.get(LeadStatus.SENT.value, 0),
    }
