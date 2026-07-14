import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Загружаем ключ из .env
load_dotenv()

# Инициализируем клиента
client = genai.Client()

# Наша функция-инструмент (база данных цен)
def get_product_price(product_name: str) -> str:
    """
    Позволяет узнать цену товара в нашем магазине по его точному названию.
    
    Args:
        product_name: Название товара (например, "яблоки", "молоко", "хлеб").
    """
    product = product_name.lower()
    prices_db = {
        "яблоки": "120 рублей за кг",
        "молоко": "85 рублей за бутылку",
        "хлеб": "45 рублей за буханку"
    }
    if product in prices_db:
        return f"Цена товара '{product_name}': {prices_db[product]}"
    else:
        return f"Товар '{product_name}' не найден в ассортименте."


# =====================================================================
# НАЧАЛО ДИАЛОГА
# =====================================================================

user_query = "Привет! Подскажи, пожалуйста, сколько у вас стоят яблоки?"
print(f"👤 Пользователь: {user_query}\n")

# Шаг 1: Отправляем первый запрос модели.
# Мы используем метод chats.create(), так как он автоматически умеет
# вести историю переписки (хранить контекст сообщений).
chat = client.chats.create(
    model="gemini-3.1-flash-lite",
    # Передаем конфигурацию с нашими доступными инструментами
    config=types.GenerateContentConfig(
        tools=[get_product_price]
    )
)

# Отправляем вопрос пользователя в чат
response = chat.send_message(user_query)

# Шаг 2: Проверяем, хочет ли модель вызвать функцию
if response.function_calls:
    print("🤖 Модель решила использовать инструмент...")
    
    for function_call in response.function_calls:
        # 1. Извлекаем имя функции и аргументы, которые подобрала модель
        tool_name = function_call.name
        tool_args = function_call.args
        print(f"   -> ИИ вызывает: {tool_name} с параметрами {tool_args}")
        
        # 2. Выполняем реальный Python-код
        # В реальных проектах тут может быть запрос к API, к SQL базе данных или поиск в векторе
        if tool_name == "get_product_price":
            tool_result = get_product_price(product_name=tool_args["product_name"])
            print(f"⚙️ Результат работы функции: {tool_result}\n")
            
            # 3. САМЫЙ ВАЖНЫЙ МОМЕНТ:
            # Отправляем результат работы функции обратно в чат.
            # Для этого мы используем специальный тип ответа Part.from_function_response
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=tool_name,
                    response={"result": tool_result} # Передаем ответ в виде словаря
                )
            )
            
            # 4. Выводим пользователю итоговый, красивый ответ от ИИ
            print(f"🤖 Итоговый ответ Gemini:\n{final_response.text}")
else:
    # Если модель сразу знала ответ без вызова функций
    print(f"🤖 Ответ Gemini:\n{response.text}")