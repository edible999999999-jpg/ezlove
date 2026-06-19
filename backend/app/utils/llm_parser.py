import json
import re
from app.config import settings


async def parse_canteen_text(
    raw_text: str,
    elder_list: list[dict],
) -> dict:
    """
    调用 LLM 将非结构化食堂文本解析为结构化 JSON。
    失败时返回 {"error": "原因", "fallback": True}。
    """
    if not settings.ANTHROPIC_API_KEY:
        return {"error": "LLM API 未配置", "fallback": True}

    elder_context = "\n".join(
        f"- {e['name']} (id: {e['id']}, {e['care_level']}级)"
        for e in elder_list
    )

    system_prompt = f"""你是社区食堂就餐记录解析助手。
以下是该社区的老人名单：
{elder_context}

请将输入的就餐记录解析为以下 JSON 格式（只返回 JSON，不要其他文字）：
{{
  "date": "YYYY-MM-DD",
  "meal_type": "breakfast|lunch|dinner",
  "attendees": [
    {{"elder_id": "uuid", "elder_name": "姓名", "present": true, "notes": "备注"}}
  ],
  "parse_notes": "解析说明"
}}

规则：
1. present 为 true 表示就餐，false 表示未就餐
2. 如果无法判断，present 设为 null
3. elder_id 必须从名单中匹配，名字模糊匹配
4. 名单外的老人单独列出，elder_id 设为 null"""

    try:
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": raw_text}],
        )
        text = response.content[0].text
        match = re.search(r'```(?:json)?\s*(.*?)```', text, re.DOTALL)
        if match:
            text = match.group(1)
        return json.loads(text.strip())
    except Exception as e:
        return {"error": str(e), "fallback": True}
