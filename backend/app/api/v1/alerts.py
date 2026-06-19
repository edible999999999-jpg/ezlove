from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.models.alert import Alert
from app.models.care_relation import CareRelation
from app.schemas.alert import AlertResponse

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get("", response_model=list[AlertResponse])
async def list_alerts(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    relation_ids_result = await db.execute(
        select(CareRelation.id).where(
            (CareRelation.family_user_id == user.id) | (CareRelation.elder_user_id == user.id)
        )
    )
    relation_ids = [r[0] for r in relation_ids_result.all()]
    if not relation_ids:
        return []

    result = await db.execute(
        select(Alert).where(Alert.care_relation_id.in_(relation_ids)).order_by(Alert.created_at.desc())
    )
    return result.scalars().all()


@router.put("/{alert_id}/resolve")
async def resolve_alert(alert_id: UUID, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.id == alert_id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(status_code=404, detail="告警不存在")

    relation_ids_result = await db.execute(
        select(CareRelation.id).where(
            (CareRelation.family_user_id == user.id) | (CareRelation.elder_user_id == user.id)
        )
    )
    relation_ids = [r[0] for r in relation_ids_result.all()]
    if alert.care_relation_id not in relation_ids:
        raise HTTPException(status_code=403, detail="无权操作此告警")

    alert.is_resolved = True
    alert.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    return {"ok": True}
