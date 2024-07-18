import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import schedule
from telegram import Bot


# Ваш токен Telegram бота
TOKEN = '7421323783:AAGgOkEEU5HwULpNs4aPxmTM8BC92DcyP9E'

# ID вашего чата в Telegram (можно узнать у бота @userinfobot)
CHAT_ID = '5043912221'

# URL сайта для проверки
URL = 'https://www.rdv-prefecture.interieur.gouv.fr/rdvpref/reservation/demarche/1904/creneau/'

# Инициализация бота
bot = TelegramBot(TOKEN)

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск браузера в фоновом режиме
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def check_website():
    driver.get(URL)
    
    # Здесь может быть код для взаимодействия с сайтом через Selenium, если требуется

    # Пример использования BeautifulSoup для парсинга страницы
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    slots = soup.find_all(class_='column items-center')  # Замените 'your-slot-class' на реальный класс слота

    if slots:
        message = 'Найдены новые временные слоты для записи!'
        bot.send_message(chat_id=CHAT_ID, text=message)
    else:
        print('Новых слотов нет.')

# Функция для периодической проверки
def job():
    print("Проверка сайта...")
    check_website()

# Настройка расписания проверки каждые 3 минуты
schedule.every(3).minutes.do(job)

# Запуск цикла проверки
while True:
    schedule.run_pending()
    time.sleep(1)
