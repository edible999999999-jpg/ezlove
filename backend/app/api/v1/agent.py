import json
import logging
from typing import AsyncGenerator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, async_session
from app.deps import get_current_worker
from app.models.community import CommunityWorker
from app.config import settings

logger = logging.getLogger("ezlove.agent")

router = APIRouter(prefix="/community", tags=["agent"])

SYSTEM_PROMPT = """你是溪东社区老人关怀助手「小溪」。你帮助社区工作者查询老人状态、活跃情况和告警信息。

回答要求：
- 简洁直接，用中文回答
- 优先使用工具获取实时数据，不要凭空编造数据
- 对于涉及老人隐私的信息，仅提供必要的工作信息
- 语气温暖专业，体现对老人的关怀
- 当回复涉及特定老人时，用 [[elder:老人社区档案ID:老人姓名]] 标记，例如 [[elder:abc123:王秀英]]
- 确认活跃操作完成后，告知工作者已记录
- 展示趋势数据时用简洁的文字描述变化方向"""


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


@router.post("/agent/chat")
async def agent_chat(
    data: ChatRequest,
    worker: CommunityWorker = Depends(get_current_worker),
):
    if not settings.ANTHROPIC_API_KEY:
        async def no_key():
            yield f"data: {json.dumps({'type': 'text_delta', 'content': 'AI 功能未配置，请联系管理员设置 ANTHROPIC_API_KEY。'})}\n\n"
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        return StreamingResponse(no_key(), media_type="text/event-stream")

    return StreamingResponse(
        _stream_response(data.messages, worker),
        media_type="text/event-stream",
    )


async def _stream_response(
    messages: list[ChatMessage],
    worker: CommunityWorker,
) -> AsyncGenerator[str, None]:
    import anthropic
    from app.services.agent import TOOLS, execute_tool

    client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

    api_messages = [{"role": m.role, "content": m.content} for m in messages]

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=api_messages,
        )

        while response.stop_reason == "tool_use":
            tool_blocks = [b for b in response.content if b.type == "tool_use"]

            for text_block in response.content:
                if text_block.type == "text" and text_block.text:
                    yield f"data: {json.dumps({'type': 'text_delta', 'content': text_block.text}, ensure_ascii=False)}\n\n"

            tool_results = []
            for tb in tool_blocks:
                yield f"data: {json.dumps({'type': 'tool_use', 'name': tb.name}, ensure_ascii=False)}\n\n"

                async with async_session() as db:
                    result_str = await execute_tool(db, worker.community_id, tb.name, tb.input, worker_id=worker.id)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tb.id,
                    "content": result_str,
                })

            api_messages.append({"role": "assistant", "content": [b.model_dump() for b in response.content]})
            api_messages.append({"role": "user", "content": tool_results})

            response = await client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=api_messages,
            )

        for block in response.content:
            if block.type == "text":
                yield f"data: {json.dumps({'type': 'text_delta', 'content': block.text}, ensure_ascii=False)}\n\n"

    except Exception as e:
        logger.exception("Agent chat error")
        yield f"data: {json.dumps({'type': 'error', 'content': f'AI 服务暂时不可用: {str(e)}'}, ensure_ascii=False)}\n\n"

    yield f"data: {json.dumps({'type': 'done'})}\n\n"
