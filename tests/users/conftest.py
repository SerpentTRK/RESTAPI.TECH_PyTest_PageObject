import requests
import pytest
import json

from src.configuration import baseUrl_users, first_name_value, last_name_value, company_id


@pytest.fixture
def get_users():
    """
    Выполняем GET запрос по URI и необходимыми параметрами, если они требуются, для получения всех пользователей
    """
    def _wrapped(parameters={}):
        response_object = requests.get(baseUrl_users, params=parameters)
        return response_object
    return _wrapped

@pytest.fixture
def get_user_by_id():
    """
    Выполняем GET запрос по URI для получения данных пользователя по его "user_id"
    """
    def _wrapped(user_id):
        response_object = requests.get(baseUrl_users + "/" + str(user_id))
        return response_object
    return _wrapped

@pytest.fixture
def delete_user():

    def _wrapped(user_id):
        payload = {}
        headers = {}
        requests.delete(baseUrl_users + "/" + str(user_id), headers=headers, data=payload)
    return _wrapped

@pytest.fixture
def create_user():
    """
    Выполняем POST запрос для создания нового пользователя
    """
    def _wrapped(user_data):
        payload = json.dumps(user_data)
        headers = {'Content-Type': 'application/json'}
        response_object = requests.post(baseUrl_users, headers=headers, data=payload)

        return response_object
    return _wrapped



# @pytest.fixture
# def create_and_delete_user():
#     """
#     Фикстура создает пользователя, передает данные в тест, и по завершении теста удаляет пользователя.
#     Тут же проверка удаления пользователя
#     """
#     # first_name_value, last_name_value, company_id= "Вальдемар", "Евлампиевич", 3
#
#     payload = json.dumps({"first_name": first_name_value, "last_name": last_name_value, "company_id": company_id})
#     headers = {'Content-Type': 'application/json'}
#     response_object = requests.post(baseUrl_users, headers=headers, data=payload)
#
#     user_id = response_object.json().get("user_id")
#     # print(user_id)  # удобно в постмане проверить, удалился ли потом пользователя
#
#     yield response_object
#
#     payload = {}
#     headers = {}
#     requests.delete(baseUrl_users + "/" + str(user_id), headers=headers, data=payload)


