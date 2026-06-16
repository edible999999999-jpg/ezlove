from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class MomentCreate(BaseModel):
    elder_id: UUID
    text_content: str | None = None
    media_urls: list[str] | None = None
    is_ai_generated: bool = False


class MomentResponse(BaseModel):
    id: UUID
    sender_id: UUID
    elder_id: UUID
    content_type: str
    text_content: str | None
    media_urls: list | None
    is_ai_generated: bool
    created_at: datetime
    is_read: bool = False

    model_config = {"from_attributes": True}


class ViewRequest(BaseModel):
    view_duration: int | None = None


class ResponseCreate(BaseModel):
    response_type: str
    content: str


class ElderStatusResponse(BaseModel):
    elder_name: str | None
    today_read: bool
    last_active_text: str | None


class ActivityDay(BaseModel):
    date: str
    label: str
    active: bool


class ActivityResponse(BaseModel):
    days: list[ActivityDay]
