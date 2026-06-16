from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.care_moment import CareMoment
from app.models.view_event import ViewEvent
from app.models.response import Response


async def create_moment(db: AsyncSession, sender_id: UUID, elder_id: UUID, text_content: str | None,
                        media_urls: list | None, is_ai_generated: bool = False) -> CareMoment:
    content_type = "text"
    if media_urls and text_content:
        content_type = "mixed"
    elif media_urls:
        content_type = "image"

    moment = CareMoment(
        sender_id=sender_id,
        elder_id=elder_id,
        content_type=content_type,
        text_content=text_content,
        media_urls=media_urls,
        is_ai_generated=is_ai_generated,
    )
    db.add(moment)
    await db.commit()
    await db.refresh(moment)
    return moment


async def get_moments_for_user(db: AsyncSession, user_id: UUID, role: str) -> list[CareMoment]:
    if role == "family":
        stmt = select(CareMoment).where(CareMoment.sender_id == user_id).order_by(CareMoment.created_at.desc())
    else:
        stmt = select(CareMoment).where(CareMoment.elder_id == user_id).order_by(CareMoment.created_at.desc())
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def record_view(db: AsyncSession, moment_id: UUID, viewer_id: UUID, duration: int | None = None) -> ViewEvent:
    event = ViewEvent(moment_id=moment_id, viewer_id=viewer_id, view_duration=duration)
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def is_moment_read(db: AsyncSession, moment_id: UUID) -> bool:
    result = await db.execute(select(ViewEvent).where(ViewEvent.moment_id == moment_id).limit(1))
    return result.scalar_one_or_none() is not None


async def create_response(db: AsyncSession, moment_id: UUID, responder_id: UUID,
                          response_type: str, content: str) -> Response:
    resp = Response(moment_id=moment_id, responder_id=responder_id, response_type=response_type, content=content)
    db.add(resp)
    await db.commit()
    await db.refresh(resp)
    return resp
