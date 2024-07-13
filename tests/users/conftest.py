import requests
import pytest
import json

from src.configuration import baseUrl_users


@pytest.fixture
def get_users():
    """
    Выполняем GET запрос по URI и необходимыми параметрами, если они требуются, для получения выборки пользователей
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

@pytest.fixture
def update_user():
    """
    Выполняем PUT запрос для редактирования пользователя
    """
    def _wrapped(update_data, user_id):
        payload = json.dumps(update_data)
        headers = {'Content-Type': 'application/json'}
        response_object = requests.put(baseUrl_users +"/" + str(user_id), headers=headers, data=payload)

        return response_object
    return _wrapped

@pytest.fixture
def create_and_delete_user(create_user, delete_user):
    user_id = None

    def _create_user(user_data):
        nonlocal user_id
        response_object = create_user(user_data)
        user_id = response_object.json().get("user_id")
        return response_object

    yield _create_user

    # Часть удаления пользователя
    delete_user(user_id)

# @pytest.fixture
# def create_and_delete_user():
#     """
#     Фикстура создает пользователя, передает данные в тест, и по завершении теста удаляет пользователя.
#     """
#     user_id = None
#
#     def _wrapped(user_data):
#         nonlocal user_id
#         payload = json.dumps(user_data)
#         headers = {'Content-Type': 'application/json'}
#         response_object = requests.post(baseUrl_users, headers=headers, data=payload)
#
#         user_id = response_object.json().get("user_id")
#
#         return response_object
#     yield _wrapped
#
#     payload = {}
#     headers = {}
#     requests.delete(baseUrl_users + f"/{user_id}", headers=headers, data=payload)


