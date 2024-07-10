import requests
import pytest
import json

from src.configuration import baseUrl_users, first_name_value, last_name_value, company_id


@pytest.fixture
def create_and_dalete_user():
    """
    Фикстура создает пользователя, передает данные в тест, и по завершении теста удаляет пользователя.
    """
    # first_name_value, last_name_value, company_id= "Вальдемар", "Евлампиевич", 3

    payload = json.dumps({"first_name": first_name_value, "last_name": last_name_value, "company_id": company_id})
    headers = {'Content-Type': 'application/json'}
    response_object = requests.post(baseUrl_users, headers=headers, data=payload)

    user_id = response_object.json().get("user_id")
    # print(user_id)  # удобно в постмане проверить, удалился ли потом пользователя

    yield response_object
    payload = {}
    headers = {}
    delete_response_object = requests.delete(baseUrl_users + "/" + str(user_id), headers=headers, data=payload)

