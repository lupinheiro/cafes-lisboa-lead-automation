import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.lead import LeadStatus


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    place_id: str
    name: str
    business_type: str
    address: str | None
    phone: str | None
    website: str | None
    email: str | None
    rating: float | None
    score: float
    status: LeadStatus
    outreach_draft: str | None
    created_at: datetime


class LeadApprove(BaseModel):
    approved: bool
