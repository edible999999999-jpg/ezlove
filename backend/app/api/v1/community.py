from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.database import get_db
from app.deps import get_current_worker
from app.models.community import CommunityWorker
from app.schemas.community import ElderCreate, ElderUpdate, ElderResponse
from app.services import community as community_service
from app.services.community_elder_detail import get_elder_full_detail

router = APIRouter(prefix="/community", tags=["community"])


@router.get("/elders")
async def list_elders(
    care_level: str | None = None,
    search: str | None = None,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    elders = await community_service.list_elders(
        db, worker.community_id, care_level=care_level, search=search
    )
    return elders


@router.post("/elders", response_model=ElderResponse)
async def create_elder(
    data: ElderCreate,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    elder = await community_service.create_elder_record(
        db, worker.community_id, data.model_dump()
    )
    return elder


@router.put("/elders/{elder_id}", response_model=ElderResponse)
async def update_elder(
    elder_id: UUID,
    data: ElderUpdate,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    try:
        elder = await community_service.update_elder_record(
            db, elder_id, data.model_dump(exclude_unset=True)
        )
        return elder
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/elders/{elder_id}")
async def get_elder(
    elder_id: UUID,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    detail = await community_service.get_elder_detail(db, elder_id, worker.community_id)
    if not detail:
        raise HTTPException(status_code=404, detail="老人档案不存在")
    return detail


@router.get("/elders/{elder_id}/full")
async def get_elder_full(
    elder_id: UUID,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    detail = await get_elder_full_detail(db, elder_id, worker.community_id)
    if not detail:
        raise HTTPException(status_code=404, detail="老人档案不存在")
    return detail


@router.get("/dashboard")
async def dashboard(
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    from app.services import community_event as event_service
    data = await event_service.get_dashboard_data(db, worker.community_id)
    return data
