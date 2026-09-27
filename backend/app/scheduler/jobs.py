import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import async_session_factory
from app.models.lead import Lead, LeadStatus
from app.services.ai_generation.email_generator import EmailGenerator
from app.services.ingestion.google_places import GooglePlacesSource
from app.services.scoring.scorer import score_lead

logger = logging.getLogger(__name__)

BUSINESS_TYPES = ["pastelaria", "café", "bar", "restaurante"]

# Leads com pontuação abaixo deste limiar não geram rascunho de email —
# ficam apenas registados para referência futura.
MIN_SCORE_FOR_OUTREACH = 60.0


async def run_prospecting_cycle() -> None:
    """Job periódico: recolhe, pontua e prepara rascunhos de novos leads."""
    settings = get_settings()
    source = GooglePlacesSource(settings.google_places_api_key)
    generator = EmailGenerator(settings.anthropic_api_key)

    raw_leads = await source.search(settings.prospecting_region, BUSINESS_TYPES)

    async with async_session_factory() as session:
        for raw_lead in raw_leads:
            existing = await session.execute(
                select(Lead).where(Lead.place_id == raw_lead["place_id"])
            )
            if existing.scalar_one_or_none():
                continue

            lead = Lead(**raw_lead, score=score_lead(raw_lead))
            lead.status = LeadStatus.SCORED

            if lead.score >= MIN_SCORE_FOR_OUTREACH:
                lead.outreach_draft = await generator.draft_outreach_email(
                    lead.name, lead.business_type, lead.address
                )
                lead.status = LeadStatus.PENDING_REVIEW

            session.add(lead)
            logger.info("Novo lead: %s (score=%.1f)", lead.name, lead.score)

        await session.commit()


def create_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_prospecting_cycle, "cron", day_of_week="mon", hour=7)
    return scheduler
