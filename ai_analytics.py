import json
from openai import AsyncOpenAI
from bot.core.config import settings

# Инициализация AITunnel клиента
client = AsyncOpenAI(
    api_key=settings.AITUNNEL_API_KEY,
    base_url=settings.AITUNNEL_BASE_URL
)

async def generate_weekly_report(student_name: str, universe: str, stats: dict) -> dict:
    """
    Генерирует два отчета: вайбовый для студента и методический для репетитора.
    """
    system_prompt = f"""
    Ты — эксперт-методист по английскому языку и гейм-мастер. 
    Ученик: {student_name}, Вселенная: {universe}. 
    Статистика за неделю: {json.dumps(stats)}
    
    Сгенерируй JSON-ответ с двумя ключами:
    1. "student_report": Мотивационный текст в стиле выбранной вселенной (вайбовый, обращение на "ты").
    2. "tutor_report": Сухой методический анализ для репетитора (проблемные темы, рекомендации по ДЗ).
    """

    try:
        response = await client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Сгенерируй еженедельный отчет."}
            ],
            response_format={"type": "json_object"}, 
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Ошибка генерации отчета: {e}")
        return {"student_report": "Ошибка ИИ", "tutor_report": "Ошибка ИИ"}