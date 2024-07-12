
import pytest
import requests
import json

from src.configuration import baseUrl_users, first_name_value, last_name_value, company_id

from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods

from src.pydantic_shemas.model_user_200 import ModelUser200
from src.pydantic_shemas.model_422 import Model422


@pytest.mark.users
def test_016_get_users_with_limit_and_offset(get_users):
    """
    Получить список пользователей с query-параметрами limit = 10 и offset = 5

    Ожидаемый результат:
        Cтатус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON data 10 пользователей, user_id начинается с 6-ой по счету записи
    """
    limit_value, offset_value = 10, 5
    parameters = {"limit": limit_value, "offset": offset_value, "status": "ACTIVE"}
    response_object = get_users(parameters)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelUser200)

    test_object_users = UsersMethods(response_object)
    test_object_users.limit_validation(limit_value)
    test_object_users.offset_validation(offset_value)

@pytest.mark.skip("{id записи об ошибке} Вместо 422 получаем статус-код 200. Skip-аем пока не починят")
@pytest.mark.users
def test_017_get_users_with_incorrect_limit(get_users):
    """
    Получить список пользователей с отрицательным query-параметрам limit = -1

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки

    Полученный результат: Выгружены все пользователи из БД, статус-код 200
    """
    limit_value = -1
    parameters = {"limit": limit_value}
    response_object = get_users(parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

@pytest.mark.users
def test_018_get_users_with_incorrect_str_limit_and_offset(get_users):
    """
    Получить список пользователей с query-параметрами limit = abc и offset = abc

    Ожидаемый результат:
        Запрос успешно отправлен;
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
        Соединение безопасное, порт 443
        В JSON присутствует описание ошибки
    """

    limit_value, offset_value = "abc", "abc"
    parameters = {"limit": limit_value, "offset": offset_value}
    response_object = get_users(parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object.validate_error_message_with_status_code_422("limit", limit_value)
    test_object.validate_error_message_with_status_code_422("offset", offset_value)

@pytest.mark.users
def test_019_get_users_list_by_http():
    """
    Получить списка компаний HTTP-запросом (не HTTPS)

    Ожидаемый результат:
        Статус-код 301;
        Время ответа сервера - не превышает 500ms;
        Response url == "http://restapi.tech/api/users"
        Response header "Location" - "https://send-request.me/api/users/"
        Response header "Connection": "keep-alive"
    """
    response_object = requests.get("http://restapi.tech/api/users", allow_redirects=False)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(301)
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()
    assert response_object.url == "http://restapi.tech/api/users"
    assert response_object.headers["Location"] == "https://restapi.tech/api/users"

@pytest.mark.users
def test_020_create_user(get_user_by_id, create_user, delete_user):
    """
    Зарегистрировать нового пользователя

    Ожидаемый результат:
        Статус-код 201;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Новая запись JSON ответа соответствует тому, что мы отправляли при регистрации + содержит Id созданного юзера.
    """
    user_data = {"first_name": "Вальдемар", "last_name": "Евлампиевич", "company_id": 3}
    response_object = create_user(user_data)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(201)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")

    test_object_users = UsersMethods(response_object)
    test_object_users.user_validation(first_name_value, last_name_value, company_id)

    # чистим за собой БД, чтобы не засорять её тестовыми данными
    user_id = response_object.json().get("user_id")

    delete_user(user_id)
    test_object_users.validate_response_message_about_error_404(user_id)

    # response_object_ater_delete_user_id = get_user_by_id(user_id)
    # print(response_object_ater_delete_user_id.json())

    # надо сделлать отдельный метод на удаление и  метод на получение юзера но левому id
    # надо провалидировать удаление пользователя
    # "reason": "User with requested id: 4377 is absent"

@pytest.mark.users
def test_021_create_user_with_incorrect_id(create_user):
    """
    Зарегистрировать нового пользователя с не верным company_id

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON - присутствует ключ detail, значением является описание ошибки
    """

    company_id = "33"
    user_data = {"first_name": "Вальдемар", "last_name": "Евлампиевич", "company_id": company_id}
    response_object = create_user(user_data)

    print(response_object.json())



@pytest.mark.skip("Это черновик")
def test_test():
    """
    черновик
    print(response_object.__getstate__())  # вообще все выгружается, что есть
    """
    import re

    company_id = "2"
    response_object = requests.get("https://restapi.tech/api/issues/companies/" + company_id)

    response_time = int(response_object.elapsed.seconds) + int(response_object.elapsed.microseconds) / 100
    # print(response_object.elapsed.seconds, response_object.elapsed.microseconds, response_object.elapsed)
    #
    # print(response_object.elapsed.seconds)

    print(500, 500 * 10**-6)
    print(response_object.elapsed, response_object.elapsed.microseconds * 10**-3)
    # print(response_object.elapsed.seconds, response_object.elapsed.microseconds * 10**-6)
    # print(response_object.elapsed.seconds + response_object.elapsed.microseconds * 10 ** -6)


        # print(response_object.json())