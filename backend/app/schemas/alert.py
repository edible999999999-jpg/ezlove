from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: UUID
    care_relation_id: UUID
    alert_type: str
    alert_level: str
    message: str
    is_resolved: bool
    resolved_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
