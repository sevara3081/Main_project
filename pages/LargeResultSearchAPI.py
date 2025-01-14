import requests
import allure


class LargeResultSearchAPI:
    """
    Класс для работы с API при запросе большого количества результатов.
    """

    def __init__(self, base_url, token):
        """
        Инициализация API клиента.
        :param base_url: Базовый URL API.
        :param token: Токен для авторизации.
        """
        self.base_url = base_url
        self.token = token

    @allure.step("Отправить запрос с большим количеством результатов")
    def search_large_results(self, phrase, page=1, per_page=50):
        """
        Отправить запрос с большим количеством результатов.
        :param phrase: Фраза для поиска.
        :param page: Номер страницы (по умолчанию 1).
        :param per_page: Количество элементов на странице (по умолчанию 50).
        :return: Кортеж из кода статуса ответа и тела ответа в формате JSON.
        """
        url = f"{self.base_url}/search/search-phrase-suggests"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "suggests[page]": page,
            "suggests[per-page]": per_page,
            "phrase": phrase,
            "include": "products",
        }

        with allure.step("Выполнить GET запрос с большим количеством результатов"):
            response = requests.get(url, headers=headers, params=params)
            allure.attach(str(params), name="Request Parameters", attachment_type=allure.attachment_type.JSON)
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

        return response.status_code, response.json()
