
import pytest
import requests
import json

from src.classes.companies_methods import CompaniesMethods
from src.configuration import user_data

from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods
from src.pydantic_shemas.model_https_400 import Model400

from src.pydantic_shemas.model_users_200 import ModelUsers200
from src.pydantic_shemas.model_user_200 import ModelUser200
from src.pydantic_shemas.model_422 import Model422
from src.pydantic_shemas.model_404 import Model404
from src.pydantic_shemas.model_user_201 import ModelUser201


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
    test_object.validate_json_schema(ModelUsers200)

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
def test_020_create_user(create_and_delete_user):
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
    response_object = create_and_delete_user(user_data)

    test_object = GlobalMethods(response_object)
    test_object.validate_json_schema(ModelUser201)
    test_object.validate_status_code(201)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(response_object)
    test_object_users.user_validation(user_data)

@pytest.mark.users
def test_021_create_user_with_incorrect_company_id(create_user):
    """
    Зарегистрировать нового пользователя с не верным company_id

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON - присутствует ключ detail, значением является описание ошибки
        В тексте ошибки указан отправленный нами "company_id"
    """
    company_id = "33"
    user_data = {"first_name": "Вальдемар", "last_name": "Евлампиевич", "company_id": company_id}
    response_object = create_user(user_data)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(404)
    test_object.validate_json_schema(Model404)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_response_message_about_error_404(company_id)

@pytest.mark.users
@pytest.mark.parametrize("user_data",
             [({"first_name": "1", "last_name": None, "company_id": 3}),
              ({"first_name": "1", "company_id": 3})], ids=str)
def test_022_create_user_with_null_and_empty_last_name(user_data, create_user):
    """
    Зарегистрировать пользователя:
        - обязательное полем "last_name" = None;
        - вообще без указания обязательного поля "last_name" и его значения
        Все остальные данные корректные

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    response_object = create_user(user_data)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    if "last_name" in user_data:
        test_object.validate_error_message_with_status_code_422("Input should be a valid string")
    else:
        test_object.validate_error_message_with_status_code_422("Field required")

@pytest.mark.users
def test_023_create_user_in_with_closed_status(create_user):
    """
    Создать пользователя в компании company_status = CLOSED

    Ожидаемый результат:
        Статус-код 400;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    company_id = 5
    user_data = {"first_name": "Вальдемар", "last_name": "Евлампиевич", "company_id": company_id}
    response_object = create_user(user_data)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(400)
    test_object.validate_json_schema(Model400)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(response_object)
    test_object_users.assert_response_message_about_error_400()

@pytest.mark.users
def test_024_get_user_by_id(create_and_delete_user, get_user_by_id):
    """
    Получить данные пользователя по его user_id

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Запись JSON ответа соответствует тому, что мы отправляли при регистрации
    """
    response_object_create_user = create_and_delete_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    #Переходим к самому тесту
    response_object = get_user_by_id(user_id)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelUser200)

    test_object_users = UsersMethods(response_object)
    test_object_users.user_validation(user_data)

@pytest.mark.users
def test_025_get_created_user_by_incorrect_id(get_user_by_id):
    """
    Получить данные пользователя по не корректному user_id

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON - присутствует ключ detail, значением является описание ошибки
        В тексте ошибки указан отправленный нами "user_id"
    """
    user_id = 1000000
    response_object = get_user_by_id(user_id)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(404)
    test_object.validate_json_schema(Model404)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(response_object)
    test_object_users.validate_response_message_about_error_404(user_id)

@pytest.mark.users
def test_026_update_user(create_and_delete_user, update_user):
    """
    Внести изменения в данные существующего пользователя

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Новая запись JSON ответа соответствует тому, что мы отправляли при редактировании пользователя
    """
    response_object_create_user = create_and_delete_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    # Переходим к самому тесту
    update_data = {"first_name": "Гена", "last_name": "Пипеткин", "company_id": 3}
    response_object = update_user(update_data, user_id)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelUser200)

    test_object_users = UsersMethods(response_object)
    test_object_users.user_validation(update_data)

@pytest.mark.users
def test_027_update_user_with_incorrect_user_id(update_user):
    """
    Отредактировать не существующего пользователя (не существующий user_id)

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON - присутствует ключ detail, значением является описание ошибки
        В тексте ошибки указан отправленный нами "user_id"
    """
    user_id = 99999  # не существующий user_id
    update_data = {"first_name": "Гена", "last_name": "Пипеткин", "company_id": 3}
    response_object = update_user(update_data, user_id)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(404)
    test_object.validate_json_schema(Model404)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(response_object)
    test_object_users.validate_response_message_about_error_404(user_id)

@pytest.mark.users
def test_028_update_user_with_incorrect_company_id(create_and_delete_user, update_user):
    """
    Отредактировать пользователя не существующей компании (не существующий company_id)

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    response_object_create_user = create_and_delete_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    company_id = "33"
    update_data = {"first_name": "Маня", "last_name": "Пена", "company_id": company_id}
    response_object = update_user(update_data, user_id)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(404)
    test_object.validate_json_schema(Model404)
    test_object.validate_response_header("Content-type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()


    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_response_message_about_error_404(company_id)

@pytest.mark.users
def test_029_delete_user(create_user, delete_user):
    """
    Удалить пользователя

    Ожидаемый результат:
        Статус-код 202;
        Время ответа сервера - не превышает 500ms;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON ответа выводится: None
    """
    response_object_create_user = create_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    response_object_delete_user = delete_user(user_id)

    delete_object = GlobalMethods(response_object_delete_user)
    delete_object.validate_status_code(202)
    delete_object.validate_response_header("Content-type", "application/json")
    delete_object.validate_response_header("Connection", "keep-alive")
    delete_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(response_object_delete_user)
    test_object_users.validate_response_with_code_202()

@pytest.mark.users
def test_030_twice_deleted_user(create_user, delete_user):
    """
    Удалить удаленного пользователя

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В тексте ошибки указан отправленный нами "user_id"
    """
    response_object_create_user = create_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    delete_user(user_id)
    twice_delete_user = delete_user(user_id)

    delete_object = GlobalMethods(twice_delete_user)
    delete_object.validate_status_code(404)
    delete_object.validate_json_schema(Model404)
    delete_object.validate_response_header("Content-type", "application/json")
    delete_object.validate_response_header("Connection", "keep-alive")
    delete_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(twice_delete_user)
    test_object_users.validate_response_message_about_error_404(user_id)

@pytest.mark.users
def test_031_delete_user_with_incorrect_user_id(delete_user):
    """
    Удалить не существующего пользователя (не существующий user_id)

    Ожидаемый результат:
        Время ответа сервера - не превышает 500ms;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В тексте ошибки указан отправленный нами "user_id"
    """
    user_id = 99999
    response_object_delete_user = delete_user(user_id)

    delete_object = GlobalMethods(response_object_delete_user)
    delete_object.validate_status_code(404)
    delete_object.validate_response_header("Content-type", "application/json")
    delete_object.validate_response_header("Connection", "keep-alive")
    delete_object.validate_time_from_request_to_response()

    test_object_users = UsersMethods(response_object_delete_user)
    test_object_users.validate_response_message_about_error_404(user_id)




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