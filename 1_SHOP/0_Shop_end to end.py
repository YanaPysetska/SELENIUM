from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from dotenv import load_dotenv

load_dotenv()

PATH=os.getenv("DRIVER_PATH")
service = Service(PATH)

options = Options()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://rahulshettyacademy.com/angularpractice/")
driver.implicitly_wait(5)
print(driver.title)
driver.find_element(By.CSS_SELECTOR, "a[href*='shop']").click()
cards=driver.find_elements(By.XPATH, "//div[@class='card h-100']")
my_titles_list=[]
for i in cards:
    titles=i.find_element(By.CLASS_NAME, "card-title").text
    if titles=="Blackberry":
        i.find_element(By.XPATH, "div/button").click()

driver.find_element(By.CSS_SELECTOR, "a[class*='btn-primary']").click()
driver.find_element(By.CSS_SELECTOR,"button[class*='btn-success']").click()
driver.find_element(By.ID, "country").send_keys("Pol")
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Poland")))
driver.find_element(By.LINK_TEXT, "Poland").click()
driver.find_element(By.XPATH, "//label[@for='checkbox2']").click()
driver.find_element(By.XPATH, "//input[@type='submit']").click()
success_text=driver.find_element(By.CLASS_NAME,"alert-success").text

try:
    assert "Success! Thank you!" in success_text
    print("Passed")
except AssertionError as e:
    print(f"Failed: {e}")


# Ожидание ввода от пользователя перед закрытием браузера
input("Press Enter to close the browser...")

# Закрытие браузера
driver.quit()
