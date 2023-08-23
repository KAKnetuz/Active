import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class TestOUManagement(unittest.TestCase):
    driver = None
    options = None

    @classmethod
    def setUpClass(cls):
        # Загрузка сертификата и ключа из pfx
        cls.caps = DesiredCapabilities.CHROME.copy()
        cls.caps['acceptInsecureCerts'] = True
        cls.caps['acceptSslCerts'] = True
        cls.caps['browserName'] = 'chrome'
        cls.caps['platform'] = 'ANY'
        cls.caps['version'] = ''

        cls.options = webdriver.ChromeOptions()
        cls.options.add_argument('--ignore-ssl-errors=yes')
        cls.options.add_argument('--ignore-certificate-errors')
        cls.options.add_argument('--start-maximized')

        cls.driver = webdriver.Chrome(chrome_options=cls.options, desired_capabilities=cls.caps)
        cls.driver.get("https://demo.u-system.tech/dicts/ou")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_create_invalid_ou(self):
        try:
            # Ввод сертификата и ключа pfx
            certfile = self.driver.find_element(By.NAME, "certfile")
            certfile.send_keys("путь_к_файлу.pfx")

            password = self.driver.find_element(By.NAME, "password")
            password.send_keys("пароль_к_файлу")

            submit = self.driver.find_element(By.NAME, "submit")
            submit.click()

            # Перейти на страницу создания организационной единицы (ОЕ)
            self.driver.get("https://demo.u-system.tech/dicts/ou/create")

            # Ввод невалидных данных для создания ОЕ
            name_input = self.driver.find_element(By.NAME, "name")
            name_input.send_keys("")

            # Клик на кнопке "Создать"
            create_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Создать')]")
            create_button.click()

            # Проверка наличия ошибки или уведомления о невалидных данных
            error_message = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Введите корректные данные')]")
            self.assertTrue(error_message.is_displayed())

        except Exception as e:
            self.fail(f"Произошла ошибка: {str(e)}")

    def test_interface_stability(self):
        try:
            certfile = self.driver.find_element(By.NAME, "certfile")
            certfile.send_keys("путь_к_файлу.pfx")

            password = self.driver.find_element(By.NAME, "password")
            password.send_keys("пароль_к_файлу")

            submit = self.driver.find_element(By.NAME, "submit")
            submit.click()

            for i in range(10):
                time.sleep(2)

        except Exception as e:
            self.fail(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    unittest.main()
