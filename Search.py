import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Загрузка сертификата и ключа из pfx
caps = DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True
caps['browserName'] = 'chrome'
caps['platform'] = 'ANY'
caps['version'] = ''

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(chrome_options=options, desired_capabilities=caps)
driver.get("https://demo.u-system.tech/dicts/ou")

try:
    # Ввод сертификата и ключа pfx
    driver.find_element(By.NAME, "certfile").send_keys("путь_к_файлу.pfx")
    driver.find_element(By.NAME, "password").send_keys("пароль_к_файлу")

    driver.find_element(By.NAME, "submit").click()

    time.sleep(3)

    # Поиск по параметрам (например, по названию)
    search_input = driver.find_element(By.NAME, "search_field")
    search_input.send_keys("Название_организации")  # Замените на фактическое название
    search_input.send_keys(Keys.RETURN)

    time.sleep(3)


except Exception as e:
    print(f"Произошла ошибка: {str(e)}")

finally:
    driver.quit()
