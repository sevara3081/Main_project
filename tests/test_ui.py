import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure

UI_URL = "https://www.chitai-gorod.ru"

@pytest.fixture
def driver():
    """Фикстура для управления браузером."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-cache")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.title("Тест поиска книг по автору. POSITIVE")
@allure.description("Этот тест проверяет, что поиск книг по автору работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_author(driver):
    driver.get(UI_URL)
    search_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/header/div/div[1]/div[2]/div/form/input'))
    )
    search_input.clear()
    search_input.send_keys("Джоан Роулинг")
    search_input.send_keys(Keys.ENTER)

    results = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.catalog-search-products"))
    )
    assert results, "Результаты поиска не отображаются."


@allure.title("Тест поиска книг по названию. POSITIVE")
@allure.description("Этот тест проверяет, что поиск книг по названию работает корректно.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_title(driver):
    driver.get(UI_URL)
    search_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/header/div/div[1]/div[2]/div/form/input'))
    )
    search_input.clear()
    search_input.send_keys("Гарри Поттер")
    search_input.send_keys(Keys.ENTER)

    results = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.catalog-search-products"))
    )
    assert results, "Результаты поиска не отображаются."


@allure.title("Тест поиска по несуществующему автору. NEGATIVE")
@allure.description("Этот тест проверяет, что поиск по несуществующему автору возвращает сообщение о пустых результатах.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_nonexistent_author(driver):
    driver.get(UI_URL)
    search_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/header/div/div[1]/div[2]/div/form/input'))
    )
    search_input.clear()
    search_input.send_keys("qwertyuiop123456789")
    search_input.send_keys(Keys.ENTER)

    no_results_message = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div[1]/section/div/div/h4'))
    )
    assert no_results_message.text == "Похоже, у нас такого нет", "Сообщение о пустых результатах не отображается или некорректно."


@allure.title("Тест поиска по некорректному запросу с символами !@. NEGATIVE")
@allure.description(
    "Этот тест проверяет, что поиск по некорректному запросу !@ возвращает сообщение о пустых результатах.")
@allure.feature("READ")
@allure.severity("CRITICAL")
def test_search_by_invalid_symbols(driver):
    driver.get(UI_URL)
    search_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/header/div/div[1]/div[2]/div/form/input'))
    )
    search_input.clear()
    search_input.send_keys("!@")
    search_input.send_keys(Keys.ENTER)

    no_results_message = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div[1]/section/div/div/h4'))
    )
    assert no_results_message.text == "Похоже, у нас такого нет", "Сообщение о пустых результатах некорректное."


@allure.title("Тест отображения главной страницы. POSITIVE")
@allure.description("Этот тест проверяет, что главная страница сайта отображается корректно.")
@allure.feature("UI")
@allure.severity("NORMAL")
def test_homepage_display(driver):
    driver.get(UI_URL)

    homepage_banner = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div[1]/div[1]/section/div/div/div/div[1]/a[2]/picture/img'))
    )
    assert homepage_banner, "Главная страница не отображается корректно."
