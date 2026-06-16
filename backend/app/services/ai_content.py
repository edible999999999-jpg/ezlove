import json
from datetime import datetime

from app.config import settings


PROMPT_TEMPLATE = """你是一个温暖的家庭关怀助手。请为一位子女生成3条可以发给独居老人的温暖问候。

当前信息：
- 时间：{time}
- 日期：{date}

要求：
1. 每条不超过100字
2. 语气温暖、口语化，像孩子跟父母说话
3. 内容类型多样：天气问候、养生提示、日常分享、回忆触发
4. 不要使用"亲爱的"等过于正式的称呼，用"妈"、"爸"等口语

请严格按以下JSON格式返回：
[
  {{"tag": "内容类型", "text": "问候内容"}},
  {{"tag": "内容类型", "text": "问候内容"}},
  {{"tag": "内容类型", "text": "问候内容"}}
]
"""


async def generate_suggestions() -> list[dict]:
    now = datetime.now()
    prompt = PROMPT_TEMPLATE.format(
        time=now.strftime("%H:%M"),
        date=now.strftime("%Y年%m月%d日"),
    )

    if not settings.ANTHROPIC_API_KEY:
        return _fallback_suggestions()

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = message.content[0].text
        return json.loads(text)
    except Exception:
        return _fallback_suggestions()


def _fallback_suggestions() -> list[dict]:
    hour = datetime.now().hour
    if hour < 12:
        return [
            {"tag": "早安", "text": "妈，早上好！今天天气不错，记得出去走走，别老闷在家里。"},
            {"tag": "养生", "text": "爸，早饭吃了吗？别光喝粥，煮个鸡蛋吃，营养要跟上。"},
            {"tag": "日常", "text": "妈，我今天上班路上看到桂花开了，特别香，想起小时候你带我在楼下摘桂花。"},
        ]
    elif hour < 18:
        return [
            {"tag": "午安", "text": "爸，中午别忘了午休一会儿，别一直看电视。"},
            {"tag": "日常", "text": "妈，我今天中午自己做了番茄炒蛋，味道越来越像你做的了！"},
            {"tag": "关心", "text": "爸，天气热了，记得多喝水。冰箱里的西瓜别放太久了啊。"},
        ]
    else:
        return [
            {"tag": "晚安", "text": "妈，早点休息，别看手机太晚了，对眼睛不好。"},
            {"tag": "日常", "text": "爸，今天加班刚到家，给你看看我养的那盆绿萝，长得可好了。"},
            {"tag": "关心", "text": "妈，晚上出去散步注意安全，带好手机。想你了，周末回来看你。"},
        ]
