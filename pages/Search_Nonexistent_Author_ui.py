from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchByNonexistentAuthor:
    def __init__(self, driver):
        self.driver = driver
        self.search_input_xpath = '//*[@id="__layout"]/div/header/div/div[1]/div[2]/div/form/input'
        self.no_results_css_selector = "div.catalog-search-products"

    def search(self, author_name):
        search_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.XPATH, self.search_input_xpath))
        )
        search_input.clear()
        search_input.send_keys(author_name)
        search_input.send_keys(Keys.ENTER)

    def get_no_results_message(self):
        no_results_message = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.no_results_css_selector))
        )
        return no_results_message.text

