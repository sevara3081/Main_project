from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchInvalidSymbolsPage:
    def __init__(self, driver):
        self.driver = driver
        self.search_input_xpath = '//*[@id="__layout"]/div/header/div/div[1]/div[2]/div/form/input'
        self.no_results_message_xpath = '//*[@id="__layout"]/div/div[3]/div[1]/section/div/div/h4'

    def enter_symbols_and_search(self, symbols):
        """
        Вводит символы в поле поиска и выполняет поиск.
        """
        search_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, self.search_input_xpath))
        )
        search_input.clear()
        search_input.send_keys(symbols)
        search_input.send_keys(Keys.ENTER)

    def get_no_results_message(self):
        """
        Ожидает появления сообщения о пустых результатах и возвращает текст сообщения.
        """
        no_results_message = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, self.no_results_message_xpath))
        )
        return no_results_message.text


