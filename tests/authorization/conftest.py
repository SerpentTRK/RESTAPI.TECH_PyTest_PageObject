import requests
import pytest
import json

from src.configuration import baseUrl_create_token, baseUrl_get_user_by_token


@pytest.fixture
def create_token():
    """
    Получение токена по пользовательским авторизационным данным.
    """
    def _create_token(login, password, timeout):
        payload = json.dumps({"login": login, "password": password, "timeout": timeout})
        headers = {'Content-Type': 'application/json'}
        response_object = requests.post(baseUrl_create_token, headers=headers, data=payload)
        return response_object

    return _create_token

@pytest.fixture
def authorization(create_token):
    """
    Получение пользовательских авторизационных данных по токену.
    Сперва используется фикстура create_token для получения токена, а после уже получаем авторизационные данные
    """
    def _wrapped(login, password, timeout):

        response = create_token(login, password, timeout)
        token = response.json().get("token")

        payload, headers = {}, {"x-token": token}
        response_object = requests.get(baseUrl_get_user_by_token, headers=headers, data=payload)
        return response_object

    return _wrapped


## Старая реализация
# def _create_token(login, password, timeout):
#
#     payload = json.dumps({"login": login, "password": password, "timeout": timeout})
#     headers = {'Content-Type': 'application/json'}
#     response_object = requests.post(baseUrl_create_token, headers=headers, data=payload)
#
#     return response_object
#
# @pytest.fixture
# def create_token():
#     return _create_token
#
# @pytest.fixture
# def authorization():
#     payload = json.dumps({"login": "Test_login", "password": "qwerty12345"})
#     headers = {'Content-Type': 'application/json'}
#     resp = requests.post(baseUrl_create_token, headers=headers, data=payload)
#     print(resp.json())
#     token = resp.json().get("token")
#     return resp












