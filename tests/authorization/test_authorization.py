import pytest
import requests
import json

from src.configuration import authorization_data
from src.test_workspace.authorization.create_token_with_correct_data_combination_034 import \
    CreateTokenWithCorrectDataCombination
from src.test_workspace.authorization.create_token_with_incorrect_login_combination_035 import \
    CreateTokenWithIncorrectLoginCombination
from src.test_workspace.authorization.create_token_with_incorrect_password_combination_036 import \
    CreateTokenWithIncorrectPasswordCombination
from src.test_workspace.authorization.get_data_about_user_by_token_037 import GetDataAboutUserByToken


@pytest.mark.authorization
@pytest.mark.parametrize("login, password, timeout, result_status_code",
                        [("1234567", "qwerty12345", 360, 200),
                        ("1234567", "qwerty12345", 360, 200),
                        ("123", "qwerty12345", 360, 200)], ids=str)
def test_create_token_with_correct_data_combination_034(login, password, timeout, result_status_code, create_token):
    """
    Получить токен подставляя допустимые значения

    Проведение общих проверок для всех тестов:
        Валидация модели или сообщения об ошибке
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Время ответа сервера - не превышает 500ms;
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
    Получить токен подставляя не допустимые значения login

    Проведение общих проверок для всех тестов:
        Валидация модели или сообщения об ошибке
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Время ответа сервера - не превышает 500ms;
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
    Получить токен подставляя не допустимые значения password

    Проведение общих проверок для всех тестов:
        Валидация модели или сообщения об ошибке
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Время ответа сервера - не превышает 500ms;
    """
    response_object = create_token(login, password, timeout)

    api = CreateTokenWithIncorrectPasswordCombination(response_object)
    api.run_tests(result_status_code)

def test_get_data_about_user_by_token_037(authorization):
    """
    Получить данные пользователя по токену.

    Проведение общих проверок для всех тестов:
        Статус-код 200;
        Валидация модели;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Время ответа сервера - не превышает 500ms;
        Проверка, что имя пользователя, указанное при регистрации токена,
            совпадает с данными, полученными при авторизации по токену;
    """

    response_object = authorization(*authorization_data)

    api = GetDataAboutUserByToken(response_object)
    api.run_tests()





    # test_object = ResponseTest(authorization)
    # test_object_auth = ResponseAuthTest(resp)
    #
    # test_object.assert_status_code(200). \
    #     validate_schema(ModelAuth200). \
    #     assert_response_header("content-type", "application/json"). \
    #     assert_response_header("connection", "keep-alive"). \
    #     assert_https_request("443")
    # test_object_auth.assert_user_data("Test_login")
    # test_object.validate_time_from_request_to_response(timedelta(microseconds=1500000))




@pytest.mark.skip("Это черновик")
def test_test():
    """
    черновик
    print(response_object.__getstate__())  # вообще все выгружается, что есть
    """
