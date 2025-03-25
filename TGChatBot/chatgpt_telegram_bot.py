import random
import logging
import requests
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import wikipediaapi
from transformers import pipeline

API_TOKEN = ''
WEATHER_API_KEY = ""
NEWS_API_KEY = ''
OPENAI_API_KEY = ''
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инициализация Wikipedia API с правильным user_agent
wiki_wiki = wikipediaapi.Wikipedia(language='ru', user_agent='MyTelegramBot/1.0 (https://t.me/AI_assistant_byK1selev_bot)')
# openai.api_key = OPENAI_API_KEY
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')

# Примерный список товаров для рекламы
advertisements = [
    {"name": "Смартфон", "description": "Современный смартфон с отличной камерой и аккумулятором.", "url": "https://www.ozon.ru/product/xiaomi-smartfon-redmi-14c-8-256-gb-fioletovyy-1726508146/?at=r2t4OKQ7xs6OBMBqFvnzQZzCv8z2NYsA9YZ4yfRmXYBP&keywords=%D1%81%D0%BC%D0%B0%D1%80%D1%82%D1%84%D0%BE%D0%BD"},
    {"name": "Ноутбук", "description": "Мощный ноутбук для работы и игр.", "url": "https://www.ozon.ru/product/lunnen-ground-noutbuk-15-6-amd-ryzen-5-pro-5675u-ram-16-gb-ssd-amd-radeon-graphics-windows-home-1772266174/?at=ywtA3vOKYTk31w0XsX1V0g6HXp6xr0CYkzQ2xHLMBqDg&keywords=%D0%BD%D0%BE%D1%83%D1%82%D0%B1%D1%83%D0%BA"},
    {"name": "Наушники", "description": "Беспроводные наушники с качественным звуком.", "url": "https://www.ozon.ru/product/hoco-naushniki-besprovodnye-s-mikrofonom-hoco-w35-max-bluetooth-3-5-mm-usb-type-c-chernyy-1871532462/?at=DqtDZ2YwXsLVRG7oUwRNYoVFjw93KDFRk3km0iR1v9lV&keywords=%D0%BD%D0%B0%D1%83%D1%88%D0%BD%D0%B8%D0%BA%D0%B8"}
]

# Функция для плавного перехода к рекламе
def get_advertisement():
    return random.choice(advertisements)

def get_gpt_response(prompt):
    # Генерация ответа на основе введенного запроса с использованием GPT-Neo
    response = generator(prompt, 
                         max_length=150, 
                         num_return_sequences=1, 
                         temperature=0.7,
                         truncation=True,  # Добавляем явное указание на обрезку текста
                         pad_token_id=50256)  # Устанавливаем pad_token_id

    # Возвращаем сгенерированный текст
    return response[0]['generated_text'].strip()  # Извлекаем и очищаем ответ


# Функция для поиска информации в Википедии
def search_wikipedia(query):
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary  # Возвращаем краткое содержание страницы
    else:
        gpt_response = get_gpt_response(query)
        return gpt_response
        # return "Статья не найдена. Попробуйте уточнить запрос."

# Функция для получения текущего курса доллара
def get_dollar_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    if 'RUB' in data['rates']:
        return data['rates']['RUB']
    else:
        return None
    
def get_euro_rate():
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    response = requests.get(url)
    data = response.json()
    if 'RUB' in data['rates']:
        return data['rates']['RUB']
    else:
        return None

# Функция для получения погоды
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    data = response.json()
    
    if data.get("cod") != 200:
        return f"Ошибка получения данных о погоде: {data.get('message', 'Неизвестная ошибка')}"
    
    weather = data['weather'][0]['description']
    temp = data['main']['temp']
    city_name = data['name']
    
    return f"Погода в {city_name}: {weather}, температура: {temp}°C."

# Функция для получения новостей
def get_news():
    url = f"https://newsapi.org/v2/everything?q=technology&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    
    if data.get("status") == "ok" and data.get("articles"):
        news = ""
        for article in data['articles'][:5]:  # Берем 5 последних новостей
            title = article['title']
            url = article['url']
            news += f"{title}\n{url}\n\n"
        return news
    else:
        return "Не удалось получить новости. Попробуйте позже."

# Обработка команды /start
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: Message):
    await message.reply("Привет! Задавайте вопросы, и я постараюсь помочь. Могу рассказать о погоде, новостях, и многом другом.")

# Обработка вопроса о курсе доллара
@dp.message_handler(lambda message: 'доллар' in message.text.lower())
async def get_dollar(message: Message):
    rate = get_dollar_rate()
    if rate:
        await message.reply(f"1 доллар = {rate} рублей.")
    else:
        await message.reply("Не удалось получить курс доллара. Попробуйте позже.")

# Обработка вопроса о курсе доллара
@dp.message_handler(lambda message: 'евро' in message.text.lower())
async def get_dollar(message: Message):
    rate = get_euro_rate()
    if rate:
        await message.reply(f"1 евро = {rate} рублей.")
    else:
        await message.reply("Не удалось получить курс евро. Попробуйте позже.")

# Обработка вопроса о погоде
@dp.message_handler(lambda message: 'погода' in message.text.lower())
async def get_weather_info(message: Message):
    city = message.text.split(" ", 1)[-1] if len(message.text.split()) > 1 else "Москва"
    weather_info = get_weather(city)
    await message.reply(weather_info)

# Обработка вопроса о новостях
@dp.message_handler(lambda message: 'новости' in message.text.lower())
async def get_news_info(message: Message):
    news_info = get_news()
    await message.reply(news_info)

# Обработка приветствия
@dp.message_handler(lambda message: 'привет' in message.text.lower())
async def get_giraffe_info(message: Message):
    await message.reply("Привет, я искусственный интеллект! Как могу помочь?")

@dp.message_handler(lambda message: 'пока' in message.text.lower())
async def get_giraffe_info(message: Message):
    await message.reply("Пока, рад был помочь!")
    if random.random() > 0.1:  # Примерный шанс перехода к рекламе
            ad = get_advertisement()
            await message.reply(f"Кстати, я хотел бы порекомендовать вам {ad['name']}!\n\nОписание: {ad['description']}\nСсылка: {ad['url']}")

# @dp.message_handler(lambda message: 'привет' in message.text.lower())
@dp.message_handler(lambda message: message.text.lower() in ['как дела?', 'что нового?', 'как ты?'])
async def get_giraffe_info(message: Message):
    await message.reply("Я искусственный интеллект, у меня всё хорошо, спасибо, что спросил! Как могу помочь?")
    if random.random() > 0.1:  # Примерный шанс перехода к рекламе
            ad = get_advertisement()
            await message.reply(f"Кстати, я хотел бы порекомендовать вам {ad['name']}!\n\nОписание: {ad['description']}\nСсылка: {ad['url']}")


# Обработка других вопросов о Википедии
@dp.message_handler(lambda message: message.text.strip() != "")
async def search_wikipedia_for_other_queries(message: Message):
    user_message = message.text.strip()
    wiki_response = search_wikipedia(user_message)
    await message.reply(wiki_response)


# Обработка других вопросов
@dp.message_handler(lambda message: message.text.strip() != "")
async def search_wikipedia_for_other_queries(message: Message):
    user_message = message.text.strip()
    
    # Если вопрос не о простых вещах (например, погода, доллар и т.д.), используем GPT-3 для ответа
    if user_message.lower() in ['как дела?', 'что нового?', 'как ты?', 'почему ты тут?', 'что ты думаешь?']:
        await message.reply("Я искусственный интеллект, у меня всё хорошо, спасибо, что спросил! Как могу помочь?")
    else:
        # Используем GPT-3 для ответа на запрос
        gpt_response = get_gpt_response(user_message)
        await message.reply(gpt_response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
