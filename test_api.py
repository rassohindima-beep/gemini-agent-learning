import os
from dotenv import load_dotenv
from google import genai

# Загружаем переменные из .env
load_dotenv()

# Инициализируем клиента
client = genai.Client()

try:
    # Используем актуальную легкую модель
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents='Привет! Если ты видишь это сообщение, значит наше подключение работает. Ответь одной короткой фразой.',
    )
    print("Ответ от Gemini:")
    print(response.text)
except Exception as e:
    print(f"Ошибка при подключении: {e}")