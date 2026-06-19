import logging
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.care_relation import CareRelation
from app.models.care_moment import CareMoment
from app.models.view_event import ViewEvent
from app.models.alert import Alert

logger = logging.getLogger("ezlove.alert_checker")
scheduler = AsyncIOScheduler()


async def check_unread_alerts():
    async with async_session() as db:
        result = await db.execute(
            select(CareRelation).where(CareRelation.status == "active")
        )
        relations = result.scalars().all()

        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        for rel in relations:
            moments_result = await db.execute(
                select(CareMoment).where(
                    CareMoment.sender_id == rel.family_user_id,
                    CareMoment.elder_id == rel.elder_user_id,
                    CareMoment.created_at >= today_start,
                )
            )
            today_moments = moments_result.scalars().all()
            if not today_moments:
                continue

            has_view = False
            for m in today_moments:
                view_result = await db.execute(
                    select(ViewEvent).where(
                        ViewEvent.moment_id == m.id,
                        ViewEvent.viewer_id == rel.elder_user_id,
                    ).limit(1)
                )
                if view_result.scalar_one_or_none():
                    has_view = True
                    break

            if has_view:
                continue

            earliest_moment = min(today_moments, key=lambda m: m.created_at)
            hours_since = (now - earliest_moment.created_at).total_seconds() / 3600

            if hours_since < rel.alert_threshold:
                continue

            existing = await db.execute(
                select(Alert).where(
                    Alert.care_relation_id == rel.id,
                    Alert.alert_type == "unread",
                    Alert.is_resolved == False,
                    Alert.created_at >= today_start,
                )
            )
            if existing.scalar_one_or_none():
                continue

            level = "info"
            if hours_since >= 48:
                level = "urgent"
            elif hours_since >= 24:
                level = "warning"

            message = f"已发送的牵挂内容超过{int(hours_since)}小时未被查看，建议联系确认"
            alert = Alert(
                care_relation_id=rel.id,
                alert_type="unread",
                alert_level=level,
                message=message,
            )
            db.add(alert)

        await db.commit()
    logger.info("告警检测完成")


def start_scheduler():
    scheduler.add_job(check_unread_alerts, "interval", hours=1, id="alert_checker")
    scheduler.start()
    logger.info("告警检测定时任务已启动")


def shutdown_scheduler():
    scheduler.shutdown()
