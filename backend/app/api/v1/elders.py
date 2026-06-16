from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.deps import get_current_user
from app.models.user import User
from app.models.view_event import ViewEvent
from app.models.care_moment import CareMoment
from app.schemas.moment import ElderStatusResponse, ActivityResponse, ActivityDay

router = APIRouter(prefix="/elders", tags=["elders"])

WEEKDAY_LABELS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


@router.get("/{elder_id}/status", response_model=ElderStatusResponse)
async def get_elder_status(elder_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    elder_result = await db.execute(select(User).where(User.id == elder_id))
    elder = elder_result.scalar_one_or_none()
    elder_name = elder.nickname if elder else None

    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    result = await db.execute(
        select(ViewEvent)
        .join(CareMoment, ViewEvent.moment_id == CareMoment.id)
        .where(CareMoment.elder_id == elder_id, ViewEvent.viewer_id == elder_id, ViewEvent.viewed_at >= today_start)
        .limit(1)
    )
    today_read = result.scalar_one_or_none() is not None

    last_result = await db.execute(
        select(ViewEvent.viewed_at)
        .where(ViewEvent.viewer_id == elder_id)
        .order_by(ViewEvent.viewed_at.desc())
        .limit(1)
    )
    last_active = last_result.scalar_one_or_none()
    last_text = last_active.strftime("%m月%d日 %H:%M") if last_active else None

    return ElderStatusResponse(elder_name=elder_name, today_read=today_read, last_active_text=last_text)


@router.get("/{elder_id}/activity", response_model=ActivityResponse)
async def get_elder_activity(
    elder_id: str, days: int = 7,
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
):
    now = datetime.now(timezone.utc)
    start = (now - timedelta(days=days - 1)).replace(hour=0, minute=0, second=0, microsecond=0)

    result = await db.execute(
        select(func.date(ViewEvent.viewed_at))
        .where(ViewEvent.viewer_id == elder_id, ViewEvent.viewed_at >= start)
        .group_by(func.date(ViewEvent.viewed_at))
    )
    active_dates = {row[0] for row in result.all()}

    day_list = []
    for i in range(days):
        d = (start + timedelta(days=i)).date()
        label = WEEKDAY_LABELS[d.weekday()]
        day_list.append(ActivityDay(date=str(d), label=label, active=d in active_dates))

    return ActivityResponse(days=day_list)
