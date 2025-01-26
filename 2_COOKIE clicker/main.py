from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

options = Options()
options.add_argument("--disable-search-engine-choice-screen")

driver = webdriver.Chrome(options=options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Функция для клика по печеньке
def coockie_click():
    cookie = driver.find_element(By.ID, value="cookie")
    return cookie.click()

# Функция для получения цен в магазине
def get_store_price():
    prices = []
    store_items = driver.find_elements(By.CSS_SELECTOR, "#store div")
    for i in store_items:
        try:
            price_element = i.find_element(By.TAG_NAME, "b")
            prices.append(price_element.text)
        except:
            continue

    items_dict = {}

    for i in prices:
        if i:  # Проверка, чтобы не обрабатывать пустую строку
            name, price = i.split(' - ')  # Разделяем строку на название и стоимость
            price = price.replace(',', '')  # Убираем запятые из числа
            items_dict[name.strip()] = int(price)  # Добавляем в словарь с преобразованием стоимости в число
    return items_dict

# Функция для клика на элемент, если хватает денег
def buy_item(item_name):
    try:
        item_id = {
            "Cursor": "buyCursor",
            "Grandma": "buyGrandma",
            "Factory": "buyFactory",
            "Mine": "buyMine",
            "Shipment": "buyShipment",
            "Alchemy lab": "buyAlchemy_lab",
            "Portal": "buyPortal",
            "Time machine": "buyTime_machine"
        }
        buy_button = driver.find_element(By.ID, item_id[item_name])
        buy_button.click()
        print(f"Purchased: {item_name}")
    except Exception as e:
        print(f"Could not purchase {item_name}: {e}")

# Таймеры и интервалы
timeout = time.time() + 60 * 5  # 5 минут с настоящего момента
interval = 5  # Интервал в 5 секунд
next_check = time.time() + interval

while True:
    coockie_click()  # Клик по печеньке

    if time.time() >= next_check:
        money = driver.find_element(By.ID, value="money")

        # Убираем запятые из строки
        money_text = money.text.replace(',', '').replace('$', '')
        money_value = int(money_text)
        items_dict = get_store_price()
        affordable_items = []

        for item, price in items_dict.items():
            if money_value >= price:
                affordable_items.append(item)

        # Если есть элементы, на которые хватает денег
        if affordable_items:
            # Находим самый дорогой элемент, который можем себе позволить
            most_expensive_item = affordable_items[-1]
            buy_item(most_expensive_item)  # Покупаем его
        else:
            print("Not enough money for any item.")

        next_check = time.time() + interval

    if time.time() > timeout:
        break

input("Press Enter to close the browser...")
driver.quit()
