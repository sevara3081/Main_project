from selenium import webdriver
from selenium.webdriver.common.by import By
import allure

class SearchByTitle:
    @allure.description("Тестирование поля поиска по названию на сайте Читай-город.")
    def __init__(self, book_title: str):
        self.book_title = book_title

    @allure.step("Поиск книги по названию")
    def search_by_title(self, driver: webdriver.Chrome) -> None:
        """Поиск книг по названию."""
        try:
            search_input = driver.find_element(By.NAME, "phrase")
            search_input.send_keys(self.book_title)
            search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
            search_button.click()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
            raise
