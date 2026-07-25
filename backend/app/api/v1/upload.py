import uuid
from pathlib import Path
from asyncio import get_event_loop
from functools import partial

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException

from app.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = Path(__file__).resolve().parents[3] / "static" / "uploads"
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024  # 1MB

# 允许的魔数（magic bytes）
MAGIC_BYTES = {
    b"\xff\xd8\xff": "jpg",          # JPEG
    b"\x89PNG": "png",                # PNG (89 50 4E 47)
    b"GIF": "gif",                    # GIF (47 49 46)
    b"RIFF": "webp",                  # WebP (RIFF....WEBP)
}


def _check_magic_bytes(header: bytes) -> str | None:
    """检查文件头魔数是否匹配已知图片格式，返回扩展名或 None"""
    for magic, ext in MAGIC_BYTES.items():
        if header.startswith(magic):
            return ext
    return None


def _write_file(filepath: Path, content: bytes) -> None:
    """同步写文件，供 run_in_executor 调用"""
    with open(filepath, "wb") as f:
        f.write(content)


@router.post("")
async def upload_file(file: UploadFile = File(...), user: User = Depends(get_current_user)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="仅支持 jpg/png/gif/webp 图片")

    # 分块读取并校验大小
    chunks: list[bytes] = []
    total_size = 0
    while True:
        chunk = await file.read(CHUNK_SIZE)
        if not chunk:
            break
        total_size += len(chunk)
        if total_size > MAX_SIZE:
            raise HTTPException(status_code=400, detail="图片不能超过 5MB")
        chunks.append(chunk)
    content = b"".join(chunks)

    # 魔数校验
    if len(content) < 4:
        raise HTTPException(status_code=400, detail="文件内容无效")
    detected_ext = _check_magic_bytes(content)
    if detected_ext is None:
        raise HTTPException(status_code=400, detail="文件内容与声明的类型不匹配")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    # 使用 uuid 生成安全文件名，忽略原始文件名中的路径分隔符
    filename = f"{uuid.uuid4().hex}.{detected_ext}"
    filepath = UPLOAD_DIR / filename

    # 异步写文件，不阻塞事件循环
    loop = get_event_loop()
    await loop.run_in_executor(None, partial(_write_file, filepath, content))

    return {"url": f"/static/uploads/{filename}"}
