import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import requests
from bs4 import BeautifulSoup
import random

# Инициализация синтезатора речи
engine = pyttsx3.init()
engine.setProperty('rate', 170)  # Скорость речи
engine.setProperty('voice', 'com.apple.speech.synthesis.voice.milena')  # Голос (для macOS)

API_KEY = "d0e67d323fbcafd1c119c7907b9b2942"
CITY = "Москва"
NEWS_API_KEY = "8f3588fa85684aa089ccdb6c74b189df"

# Определяем команды и реакции
commands = {
    "привет": "Привет! Как дела?",
    "как тебя зовут": "Я голосовой ассистент.",
    "сколько времени": "",
    "который час": "",
    "сколько время": "",
    "какая погода": "",
    "расскажи анекдот": "Окей! Почему программисты не любят природу? Потому что в ней слишком много багов!",
    "спасибо": "Всегда пожалуйста!",
    "открой почту" : "Открываю почту",
    "какие новости": "",
    "что нового": "",
    "найди в гугле": "",
    "загугли": "",
    "случайное число": "",
    "стоп": "Выключаюсь."
}

def speak(text):
    """Функция озвучивания текста"""
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """Функция распознавания речи"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio, language="ru-RU").lower()
            
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания")
            return None
        

def time_to_text(): 
    dict_hours = {1: 'чac', 2: 'чaca', 3: 'чaca', 4: 'чaca', 5: 'чaсов', 6: 'чaсов',
                  7: 'часов', 8: 'часов', 9: 'часов', 10: 'часов', 11: 'часов', 12: 'часов', 
                  13: 'часов', 14: 'часов', 15: 'часов', 16: 'часов', 17: 'часов', 18: 'часов', 
                  19: 'часов', 20: 'часов', 21: 'час', 22: 'часа', 23: 'часа', 0: 'часов'} 
    dict_minutes = {
        'минута': [1, 21, 31, 41, 51],
        'минуты': [2, 3, 4, 22, 23, 24, 32, 33, 34, 42, 43, 44, 52, 53, 54], 
        'минут': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                  25, 26, 27, 28, 29, 30, 
                  35, 36, 37, 38, 39, 40, 
                  45, 46, 47, 48, 49, 50, 
                  55, 56, 57, 58, 59]}
    now = datetime.datetime.now() 
    h = now.hour
    m = now.minute
    
    str_time = str(h) + dict_hours[h] + ''
    for minutes in dict_minutes:
        if m in dict_minutes[minutes]: 
            str_time += str(m) + ' ' + minutes 
            break

    return str_time

def get_weather():
    """Получение текущей погоды"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"Сейчас в {CITY} {description}, температура {temp} градусов."
        else:
            return "Не удалось получить данные о погоде."
    except:
        return "Ошибка при получении погоды."
    

def get_news():
    """Получение новостей"""
    url = f"https://newsapi.org/v2/everything?q=technology&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data["status"] == "ok":
            articles = data["articles"][:3]  # Берем 3 главные новости
            news_list = [article["title"] for article in articles]
            return "Вот главные новости: " + ". ".join(news_list)
        else:
            return "Не удалось получить новости."
    except:
        return "Ошибка при получении новостей."

def main():
    speak("Привет! Я голосовой ассистент. Скажите команду.")
    while True:
        command = recognize_speech()

        if command == "который час" or  command == "сколько времени" or  command == "сколько время":
            speak(time_to_text())
            print(time_to_text())
            continue
        if command == "открой почту":
            URL = "https://mail.google.com/"
            webbrowser.open(URL)
        if command == "какая погода":
            speak(get_weather())
            print(get_weather())
            continue
        if command == "что нового" or command == "какие новости":
            speak(get_news())
            print(get_news())
            continue
        if command == "найди в гугле" or command == "загугли":
            speak("открываю гугл")
            search_query = command
            webbrowser.open(f"https://www.google.com/")
        if command == "случайное число":
            number = random.randint(0, 10)
            print(f"случайное числo: {number}")
            speak(f"случайное числo: {number}")
            continue
        if command:
            response = commands.get(command, "Я не знаю такой команды.")
            speak(response)
            if command == "стоп":
                break

if __name__ == "__main__":
    main()
