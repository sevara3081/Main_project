from selenium import webdriver
from selenium.webdriver.common.by import By
import allure

class DeleteFromCart:
    @allure.description("Тестирование удаления товара из корзины на сайте Читай-город.")
    def __init__(self, book_title: str):
        self.book_title = book_title

    @allure.step("Удаление книги из корзины")
    def delete_from_cart(self, driver: webdriver.Chrome) -> None:
        """Удаляет книгу из корзины."""
        driver.find_element(By.NAME, "phrase").send_keys(self.book_title)
        search_button_find = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Искать']")
        search_button_find.click()
        search_button_buy = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Купить']")
        search_button_buy.click()
        cart_icon = driver.find_element(By.CSS_SELECTOR, ".header-cart__icon")
        cart_icon.click()
        delete_button = driver.find_element(By.CSS_SELECTOR, "span.clear-cart")
        delete_button.click()