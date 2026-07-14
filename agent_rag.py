import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client()

# =====================================================================
# НАШ RAG-ИНСТРУМЕНТ
# Функция открывает текстовый файл и ищет там ключевые слова.
# =====================================================================
def search_in_knowledge_base(query: str) -> str:
    """
    Поиск информации в официальных правилах, инструкциях и регламентах магазина.
    Используйте этот инструмент, если пользователь спрашивает про возврат, доставку или скидки.
    
    Args:
        query: Ключевое слово для поиска (например, "возврат", "доставка", "скидка").
    """
    keyword = query.lower()
    relevant_lines = []
    
    # Открываем наш файл с базой знаний
    with open("shop_rules.txt", "r", encoding="utf-8") as file:
        for line in file:
            # Если строка содержит ключевое слово, сохраняем её
            if keyword in line.lower():
                relevant_lines.append(line.strip())
                
    if relevant_lines:
        # Возвращаем найденные строки, объединенные в один текст
        return "\n".join(relevant_lines)
    else:
        return "В базе знаний ничего не найдено по этому запросу."


# =====================================================================
# ЗАПУСК ЦЕПОЧКИ (Автоматический цикл через chat.send_message)
# =====================================================================

user_query = "Привет! Я вчера купил у вас куртку, но она не подошла по размеру. Могу я её вернуть?"
print(f"👤 Пользователь: {user_query}\n")

# Создаем чат и передаем туда наш RAG-инструмент
chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=types.GenerateContentConfig(
        tools=[search_in_knowledge_base]
    )
)

# Отправляем сообщение
response = chat.send_message(user_query)

# Проверяем, вызвала ли модель наш RAG-поиск
if response.function_calls:
    for call in response.function_calls:
        print(f"🔍 ИИ заглядывает в базу знаний по ключевому слову: '{call.args['query']}'")
        
        # Выполняем поиск по файлу
        db_result = search_in_knowledge_base(query=call.args['query'])
        
        # Отправляем кусок текста из файла обратно модели
        final_response = chat.send_message(
            types.Part.from_function_response(
                name=call.name,
                response={"result": db_result}
            )
        )
        print(f"\n🤖 Ответ Gemini (на основе файла):\n{final_response.text}")
else:
    print(f"🤖 Ответ Gemini:\n{response.text}")