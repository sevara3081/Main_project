from selenium import webdriver
from selenium.webdriver.common.by import By
import allure

class SearchByAuthor:
    @allure.description("Тестирование поля поиска по автору на сайте Читай-город.")
    def __init__(self, author_name: str):
        self.author_name = author_name

    @allure.step("Поиск книг по автору")
    def search_by_author(self, driver: webdriver.Chrome) -> None:
        """Поиск книг по имени автора."""
        try:
            search_input = driver.find_element(By.NAME, "phrase")
            search_input.send_keys(self.author_name)
            search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
            search_button.click()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
            raise