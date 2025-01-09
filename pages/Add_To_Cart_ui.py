import allure
from selenium.webdriver.common.by import By

class AddToCart:
    """
    Класс для добавления книги в корзину.
    """
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Добавить книгу в корзину")
    def add_book(self, book_title):
        """
        Добавить книгу в корзину.
        :param book_title: Название книги.
        """
        search_input = self.driver.find_element(By.CSS_SELECTOR, "input.search-input")
        search_input.clear()
        search_input.send_keys(book_title)

        search_button = self.driver.find_element(By.CSS_SELECTOR, "button.search-button")
        search_button.click()

        add_to_cart_button = self.driver.find_element(By.CSS_SELECTOR, "button.add-to-cart")
        add_to_cart_button.click()