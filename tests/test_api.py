import requests
import allure
from constants import BASE_API_URL, BEARER_TOKEN, API_URL_SEARCH


@allure.feature("Читай-город API")
@allure.story("Поиск предложений по фразе (Позитивный тест)")
def test_search_phrase_suggestions_positive():
    """
    Проверяет, что API возвращает предложения по фразе с корректным токеном.
    """
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "suggests[page]": 1,
        "suggests[per-page]": 5,
        "phrase": "Гарри Поттер и философский камень",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }

    with allure.step("Отправить запрос на получение предложений по фразе"):
        response = requests.get(API_URL_SEARCH, headers=headers, params=params, timeout=30)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить, что статус ответа 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Проверить, что в ответе есть ключ 'data'"):
        response_json = response.json()
        assert "data" in response_json, "Response does not contain 'data' key"


@allure.feature("Читай-город API")
@allure.story("Поиск с пустой фразой (Негативный тест)")
def test_search_empty_phrase_negative():
    """
    Проверяет, что API возвращает ошибку при поиске с пустой фразой.
    """
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "suggests[page]": 1,
        "suggests[per-page]": 5,
        "phrase": "",
        "include": "products"
    }

    with allure.step("Отправить запрос на поиск с пустой фразой"):
        response = requests.get(API_URL_SEARCH, headers=headers, params=params, timeout=30)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить, что статус ответа 422"):
        assert response.status_code == 422, f"Expected 422, got {response.status_code}"

    with allure.step("Проверить структуру и содержание ответа"):
        response_json = response.json()
        assert "errors" in response_json, "Response does not contain 'errors' key"
        assert isinstance(response_json["errors"], list), "'errors' key is not a list"
        assert len(response_json["errors"]) > 0, "'errors' list is empty"

        # Проверяем первое сообщение об ошибке
        error = response_json["errors"][0]
        assert "title" in error, "Error does not contain 'title' key"
        assert error["title"] == "Значение не должно быть пустым.", \
            f"Unexpected error message: {error['title']}"


@allure.feature("Читай-город API")
@allure.story("Поиск с некорректным токеном (Негативный тест)")
def test_search_invalid_token_negative():
    """
    Проверяет, что API возвращает ошибку при использовании некорректного токена.
    """
    headers = {"Authorization": "Bearer INVALID_TOKEN"}
    params = {
        "suggests[page]": 1,
        "suggests[per-page]": 5,
        "phrase": "Гарри Поттер",
        "include": "products"
    }

    with allure.step("Отправить запрос на поиск с некорректным токеном"):
        response = requests.get(API_URL_SEARCH, headers=headers, params=params, timeout=30)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить, что статус ответа 401"):
        assert response.status_code == 401, f"Expected 401, got {response.status_code}"

    with allure.step("Проверить сообщение об ошибке в ответе"):
        response_json = response.json()
        assert "message" in response_json, "Response does not contain 'message' key"
        assert response_json["message"] == "JWTTokenMiddleware: token unknown", \
            f"Unexpected error message: {response_json['message']}"


@allure.feature("Читай-город API")
@allure.story("Поиск с большим количеством результатов (Позитивный тест)")
def test_search_large_result_positive():
    """
    Проверяет, что API корректно возвращает большое количество результатов.
    """
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "suggests[page]": 1,
        "suggests[per-page]": 50,
        "phrase": "Гарри Поттер",
        "include": "products"
    }

    with allure.step("Отправить запрос на поиск с большим количеством результатов"):
        response = requests.get(API_URL_SEARCH, headers=headers, params=params, timeout=30)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить, что статус ответа 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Проверить, что количество результатов соответствует запросу"):
        response_json = response.json()
        assert "data" in response_json, "Response does not contain 'data' key"
        assert len(response_json["data"]) <= 50, "More than 50 results returned"


@allure.feature("Читай-город API")
@allure.story("Поиск с несуществующей фразой (Позитивный тест)")
def test_search_nonexistent_phrase_positive():
    """
    Проверяет, что API корректно возвращает пустой результат или определённый ответ для несуществующей фразы.
    """
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "suggests[page]": 1,
        "suggests[per-page]": 5,
        "phrase": "абракадабра",
        "include": "products"
    }

    with allure.step("Отправить запрос на поиск с несуществующей фразой"):
        response = requests.get(API_URL_SEARCH, headers=headers, params=params, timeout=30)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверить, что статус ответа 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    with allure.step("Проверить, что ответ содержит ключ 'data'"):
        response_json = response.json()
        assert "data" in response_json, "Response does not contain 'data' key"

    with allure.step("Проверить содержимое 'data'"):
        if isinstance(response_json["data"], list):
            # Если "data" — список, проверяем, что он пуст
            assert len(response_json["data"]) == 0, f"Expected 'data' to be empty, got {len(response_json['data'])} items"
        elif isinstance(response_json["data"], dict):
            # Если "data" — словарь, проверяем наличие ключей
            assert "attributes" in response_json["data"], "'attributes' key is missing in 'data'"
            allure.attach(str(response_json["data"]), name="Data Content", attachment_type=allure.attachment_type.JSON)
        else:
            allure.attach(str(response_json["data"]), name="Unexpected 'data' structure", attachment_type=allure.attachment_type.JSON)
            assert False, f"Unexpected type for 'data': {type(response_json['data'])}"