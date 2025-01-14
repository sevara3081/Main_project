import requests
import allure


class EmptyPhraseSearchAPI:
    """
    Класс для работы с API при поиске с пустой фразой.
    """

    def __init__(self, base_url, token):
        """
        Инициализация API клиента.
        :param base_url: Базовый URL API.
        :param token: Токен для авторизации.
        """
        self.base_url = base_url
        self.token = token

    @allure.step("Отправить запрос с пустой фразой")
    def search_empty_phrase(self, page=1, per_page=5):
        """
        Отправить запрос с пустой фразой.
        :param page: Номер страницы (по умолчанию 1).
        :param per_page: Количество элементов на странице (по умолчанию 5).
        :return: Кортеж из кода статуса ответа и тела ответа в формате JSON.
        """
        url = f"{self.base_url}/search/search-phrase-suggests"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {
            "suggests[page]": page,
            "suggests[per-page]": per_page,
            "phrase": "",
            "include": "products",
        }

        with allure.step("Выполнить GET запрос с пустой фразой"):
            response = requests.get(url, headers=headers, params=params)
            allure.attach(str(params), name="Request Parameters", attachment_type=allure.attachment_type.JSON)
            allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

        return response.status_code, response.json()
