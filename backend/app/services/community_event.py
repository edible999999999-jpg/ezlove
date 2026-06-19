import uuid
from datetime import datetime, timezone, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community_event import CommunityEvent
from app.models.community import CommunityElder, CommunityWorker


async def list_events(
    db: AsyncSession,
    community_id: uuid.UUID,
    severity: str | None = None,
    event_type: str | None = None,
    is_resolved: bool | None = None,
) -> list[CommunityEvent]:
    stmt = select(CommunityEvent).where(CommunityEvent.community_id == community_id)
    if severity:
        stmt = stmt.where(CommunityEvent.severity == severity)
    if event_type:
        stmt = stmt.where(CommunityEvent.event_type == event_type)
    if is_resolved is not None:
        stmt = stmt.where(CommunityEvent.is_resolved == is_resolved)
    stmt = stmt.order_by(CommunityEvent.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def create_event(
    db: AsyncSession,
    community_id: uuid.UUID,
    data: dict,
) -> CommunityEvent:
    event = CommunityEvent(community_id=community_id, **data)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def resolve_event(
    db: AsyncSession,
    event_id: uuid.UUID,
    worker_id: uuid.UUID,
) -> CommunityEvent:
    stmt = select(CommunityEvent).where(CommunityEvent.id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    if not event:
        raise ValueError("事件不存在")
    event.is_resolved = True
    event.resolved_by = worker_id
    event.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(event)
    return event


async def get_dashboard_data(
    db: AsyncSession,
    community_id: uuid.UUID,
) -> dict:
    stmt = select(
        CommunityElder.care_level,
        func.count(CommunityElder.id),
    ).where(
        CommunityElder.community_id == community_id
    ).group_by(CommunityElder.care_level)
    result = await db.execute(stmt)
    level_counts = {row[0]: row[1] for row in result.all()}

    total = sum(level_counts.values())

    today_start = datetime.combine(date.today(), datetime.min.time())
    elder_stmt = select(CommunityElder.elder_id).where(
        CommunityElder.community_id == community_id
    )
    elder_result = await db.execute(elder_stmt)
    elder_ids = elder_result.scalars().all()

    from app.models.view_event import ViewEvent
    active_stmt = select(func.count(func.distinct(ViewEvent.viewer_id))).where(
        ViewEvent.viewer_id.in_(elder_ids),
        ViewEvent.viewed_at >= today_start,
    )
    active_result = await db.execute(active_stmt)
    today_active = active_result.scalar() or 0

    pending_stmt = select(func.count(CommunityEvent.id)).where(
        CommunityEvent.community_id == community_id,
        CommunityEvent.is_resolved == False,
        CommunityEvent.severity.in_(["urgent", "warning"]),
    )
    pending_result = await db.execute(pending_stmt)
    pending_events = pending_result.scalar() or 0

    heatmap = await _build_heatmap(db, community_id, today_start)

    return {
        "total_elders": total,
        "level_a": level_counts.get("A", 0),
        "level_b": level_counts.get("B", 0),
        "level_c": level_counts.get("C", 0),
        "today_active_count": today_active,
        "today_active_rate": round(today_active / total * 100, 1) if total > 0 else 0,
        "pending_events": pending_events,
        "heatmap": heatmap,
    }


async def _build_heatmap(
    db: AsyncSession,
    community_id: uuid.UUID,
    today_start: datetime,
) -> list[dict]:
    from app.models.user import User
    from app.models.view_event import ViewEvent

    stmt = (
        select(CommunityElder, User.nickname)
        .join(User, CommunityElder.elder_id == User.id)
        .where(CommunityElder.community_id == community_id)
        .order_by(CommunityElder.address)
    )
    result = await db.execute(stmt)
    elders = result.all()

    elder_ids = [e[0].elder_id for e in elders]
    active_stmt = select(ViewEvent.viewer_id).where(
        ViewEvent.viewer_id.in_(elder_ids),
        ViewEvent.viewed_at >= today_start,
    ).distinct()
    active_result = await db.execute(active_stmt)
    active_ids = set(active_result.scalars().all())

    heatmap = []
    for elder, name in elders:
        heatmap.append({
            "elder_id": str(elder.elder_id),
            "name": name,
            "care_level": elder.care_level,
            "address": elder.address or "未分配",
            "today_active": elder.elder_id in active_ids,
        })
    return heatmap
