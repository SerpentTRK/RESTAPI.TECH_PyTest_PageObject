import pytest
import requests
import json

from src.test_workspace.authorization.create_token_with_correct_data_combination_034 import \
    CreateTokenWithCorrectDataCombination
from src.test_workspace.authorization.create_token_with_incorrect_login_combination_035 import \
    CreateTokenWithIncorrectLoginCombination
from src.test_workspace.authorization.create_token_with_incorrect_password_combination_036 import \
    CreateTokenWithIncorrectPasswordCombination


@pytest.mark.authorization
@pytest.mark.parametrize("login, password, timeout, result_status_code",
                        [("1234567", "qwerty12345", 360, 200),
                        ("1234567", "qwerty12345", 360, 200),
                        ("123", "qwerty12345", 360, 200)], ids=str)
def test_create_token_with_correct_data_combination_034(login, password, timeout, result_status_code, create_token):
    """
    Получить токен подставляя допустимые значения, в ожидании status code == 200

    Проведение общих проверок для всех тестов:
        Валидация модели или сообщения об ошибке
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
        Время ответа сервера - не превышает 500ms;* это время пришлось сильно увеличить,
        т.к. тестовая база иногда еле отзывается, и все тесты падают на этой проверке
    """
    response_object = create_token(login, password, timeout)

    api = CreateTokenWithCorrectDataCombination(response_object)
    api.run_tests(result_status_code)

@pytest.mark.authorization
@pytest.mark.parametrize("login, password, timeout, result_status_code",
                        [("1", "qwerty12345", 360, 422),
                        ("12", "qwerty12345", 360, 422),
                        ("0", "qwerty12345", 360, 422),
                        ("", "qwerty12345", 360, 422),
                        (None, "qwerty12345", 360, 422)], ids=str)
def test_create_token_with_incorrect_login_combination_035(login, password, timeout, result_status_code, create_token):
    """
    Получить токен подставляя не допустимые значения, в ожидании status code == 422

    Проведение общих проверок для всех тестов:
        Валидация модели или сообщения об ошибке
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
        Время ответа сервера - не превышает 500ms;* это время пришлось сильно увеличить,
        т.к. тестовая база иногда еле отзывается, и все тесты падают на этой проверке
    """
    response_object = create_token(login, password, timeout)

    api = CreateTokenWithIncorrectLoginCombination(response_object)
    api.run_tests(result_status_code, login)

@pytest.mark.authorization
@pytest.mark.parametrize("login, password, timeout, result_status_code",
                        [("123", "qwerty", 360, 403),
                        ("123", "0", 360, 403),
                        ("123", "", 360, 403),
                        ("123", None, 360, 422)], ids=str)
def test_create_token_with_incorrect_password_combination_036(login, password, timeout, result_status_code, create_token):
    """
    Получить токен подставляя не допустимые значения, в ожидании status code == 422

    Проведение общих проверок для всех тестов:
        Валидация модели или сообщения об ошибке
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
        Время ответа сервера - не превышает 500ms;* это время пришлось сильно увеличить,
        т.к. тестовая база иногда еле отзывается, и все тесты падают на этой проверке
    """
    response_object = create_token(login, password, timeout)

    api = CreateTokenWithIncorrectPasswordCombination(response_object)
    api.run_tests(result_status_code)





@pytest.mark.skip("Это черновик")
def test_test():
    """
    черновик
    print(response_object.__getstate__())  # вообще все выгружается, что есть
    """
