from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.database import get_db
from app.deps import get_current_worker
from app.models.community import CommunityWorker
from app.models.canteen import CanteenRecord
from app.services.canteen import submit_canteen_record

router = APIRouter(prefix="/community/canteen", tags=["canteen"])


@router.post("/submit")
async def submit_canteen(
    raw_text: str | None = Form(None),
    file: UploadFile | None = File(None),
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    excel_bytes = None
    if file and file.filename.endswith((".xlsx", ".xls")):
        excel_bytes = await file.read()
    elif not raw_text:
        raise HTTPException(status_code=400, detail="请输入文本或上传 Excel 文件")

    record = await submit_canteen_record(
        db,
        worker.community_id,
        worker.id,
        raw_text=raw_text,
        excel_bytes=excel_bytes,
    )
    return {
        "id": str(record.id),
        "parse_status": record.parse_status,
        "parsed_data": record.parsed_data,
    }


@router.get("/records")
async def list_records(
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(CanteenRecord)
        .where(CanteenRecord.community_id == worker.community_id)
        .order_by(CanteenRecord.created_at.desc())
    )
    result = await db.execute(stmt)
    records = result.scalars().all()
    return [
        {
            "id": str(r.id),
            "raw_text": r.raw_text[:100],
            "source_format": r.source_format,
            "parse_status": r.parse_status,
            "parsed_data": r.parsed_data,
            "created_at": r.created_at.isoformat(),
        }
        for r in records
    ]


@router.get("/records/{record_id}")
async def get_record(
    record_id: UUID,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CanteenRecord).where(
        CanteenRecord.id == record_id,
        CanteenRecord.community_id == worker.community_id,
    )
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="食堂记录不存在")
    return {
        "id": str(record.id),
        "raw_text": record.raw_text,
        "source_format": record.source_format,
        "parse_status": record.parse_status,
        "parsed_data": record.parsed_data,
        "parsed_at": record.parsed_at.isoformat() if record.parsed_at else None,
        "created_at": record.created_at.isoformat(),
    }


@router.put("/records/{record_id}")
async def correct_record(
    record_id: UUID,
    parsed_data: dict,
    worker: CommunityWorker = Depends(get_current_worker),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CanteenRecord).where(
        CanteenRecord.id == record_id,
        CanteenRecord.community_id == worker.community_id,
    )
    result = await db.execute(stmt)
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="食堂记录不存在")
    record.parsed_data = parsed_data
    record.parse_status = "success"
    await db.commit()
    await db.refresh(record)
    return {"ok": True}
