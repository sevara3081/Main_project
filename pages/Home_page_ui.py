from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Homepage:
    def __init__(self, driver):
        """
        Конструктор для инициализации драйвера.
        """
        self.driver = driver
        self.banner_xpath = '//*[@id="__layout"]/div/div[3]/div[1]/div[1]/section/div/div/div/div[1]/a[2]/picture/img'

    def open(self, url):
        """
        Открывает главную страницу сайта.
        """
        self.driver.get(url)

    def is_banner_displayed(self):
        """
        Проверяет, отображается ли баннер на главной странице.
        """
        try:
            banner = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, self.banner_xpath))
            )
            return banner is not None
        except:
            return False
