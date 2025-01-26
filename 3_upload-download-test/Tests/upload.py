from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from excel import Excel_upd
import os
from dotenv import load_dotenv

load_dotenv()


def slow_action(delay=2):
    time.sleep(delay)


CHROME_PATH=os.getenv("CHROME_PATH")
FILE_PATH=os.getenv("FILE_PATH")
FRUIT_NAME="Apple"


service = Service(CHROME_PATH)
# Настройки браузера
options = Options()
options.add_argument("--start-maximized")  # Запуск в полноэкранном режиме
# Инициализация драйвера
driver = webdriver.Chrome(service=service, options=options)
driver.implicitly_wait(10)
driver.get("https://rahulshettyacademy.com/upload-download-test/index.html")

driver.find_element(By.ID, "downloadButton").click()
slow_action(3)

#change excel class
test=Excel_upd(FILE_PATH)
test.read_exact_name(FRUIT_NAME, "price")
my_new_value=test.add_new_value(14)

#uplod file logic
file_input=driver.find_element(By.ID, "fileinput")
slow_action(3)
file_input.send_keys(FILE_PATH)

toast_locator=(By.XPATH,"//div[@class='Toastify__toast-body']/div[2]")
slow_action(3)
WebDriverWait(driver, 5).until(EC.visibility_of_element_located(toast_locator))
print(driver.find_element(*toast_locator).text)
priceColumn=driver.find_element(By.XPATH, "//div[text()='Price']").get_attribute("data-column-id")
slow_action(3)
actual_price=driver.find_element(By.XPATH, "//div[text()='"+FRUIT_NAME+"']/parent::div/parent::div/div[@id='cell-"+priceColumn+"-undefined']").text
slow_action(3)

assert int(actual_price)==my_new_value

# Закрытие браузера
driver.quit()
