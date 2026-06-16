from uuid import UUID
from pydantic import BaseModel


class InviteResponse(BaseModel):
    invite_code: str


class BindRequest(BaseModel):
    invite_code: str


class RelationUpdate(BaseModel):
    relation_label: str | None = None
    alert_threshold: int | None = None


class RelationResponse(BaseModel):
    id: UUID
    family_user_id: UUID
    elder_user_id: UUID | None
    relation_label: str | None
    alert_threshold: int
    status: str

    model_config = {"from_attributes": True}
