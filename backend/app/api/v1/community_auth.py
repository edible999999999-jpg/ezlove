from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from passlib.context import CryptContext

from app.database import get_db
from app.models.community import CommunityWorker
from app.services.auth import create_access_token, create_refresh_token

router = APIRouter(prefix="/community/auth", tags=["community-auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"])


class LoginRequest(BaseModel):
    phone: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    worker: dict


@router.post("/login", response_model=TokenResponse)
async def community_login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    stmt = select(CommunityWorker).where(CommunityWorker.phone == data.phone)
    result = await db.execute(stmt)
    worker = result.scalar_one_or_none()

    if not worker or not pwd_ctx.verify(data.password, worker.password_hash):
        raise HTTPException(status_code=401, detail="手机号或密码错误")

    token_data = {
        "type": "worker",
        "community_id": str(worker.community_id),
    }
    access_token = create_access_token(worker.id, extra_claims=token_data)
    refresh_token = create_refresh_token(worker.id, extra_claims=token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        worker={
            "id": str(worker.id),
            "name": worker.name,
            "phone": worker.phone,
            "role_label": worker.role_label,
            "community_id": str(worker.community_id),
        },
    )
