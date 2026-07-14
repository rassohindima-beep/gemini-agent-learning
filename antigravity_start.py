import os
from dotenv import load_dotenv
# Импортируем официальный SDK от Google
from google import genai

# Загружаем переменные окружения (включая GEMINI_API_KEY)
load_dotenv()

# Инициализируем клиента
client = genai.Client()

print("🚀 Запускаем автономного агента Antigravity в удаленной песочнице...\n")

try:
    # ИСПРАВЛЕНО: Обращаемся через client.interactions.create
    interaction = client.interactions.create(
        agent="antigravity-preview-05-2026",
        # Задача для агента: найти новости, суммаризировать и записать в файл
        input="Найди топ-5 главных новостей про искусственный интеллект за эту неделю, сделай краткое резюме каждой и сохрани результат в файл ai_news.txt",
        environment="remote",  # Агент разворачивается в безопасном облачном контейнере Google
    )

    # Выводим финальный лог и результат работы агента
    print("🤖 Ответ агента:")
    print(interaction.output_text)

except Exception as e:
    print(f"Произошла ошибка при запуске агента: {e}")