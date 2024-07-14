
import pytest
import requests
import json

from src.configuration import user_data, baseUrl_issues_users

from src.test_workspace.users._issues_get_created_user_by_id_032 import IssuesGetCreatedUserById
from src.test_workspace.users.create_user_020 import CreateUser
from src.test_workspace.users.create_user_in_with_closed_status_023 import CreateUserWithClosedStatus
from src.test_workspace.users.create_user_with_incorrect_company_id_021 import CreateUserWithIncorrectCompanyId
from src.test_workspace.users.create_user_with_null_and_empty_last_name_022 import CreateUserWithNullAndEmptyLastName
from src.test_workspace.users.delete_user_029 import DeleteUser
from src.test_workspace.users.delete_user_with_incorrect_user_id_031 import DeleteUserWithIncorrectUserId
from src.test_workspace.users.get_created_user_by_incorrect_id_025 import GetCreatedUserByIncorrectId
from src.test_workspace.users.get_user_by_id_024 import GetUserById
from src.test_workspace.users.get_users_list_by_http_019 import GetUsersListByHttp
from src.test_workspace.users.get_users_with_incorrect_limit_017 import GetUsersWithIncorrectLimit
from src.test_workspace.users.get_users_with_limit_and_offset_016 import GetUsersWithLimitAndOffset
from src.test_workspace.users.issues_create_user_033 import IssuesCreateUser
from src.test_workspace.users.twice_deleted_user_030 import TwiceDeletedUser
from src.test_workspace.users.update_user_026 import UpdateUser
from src.test_workspace.users.update_user_with_incorrect_company_id_028 import UpdateUserWithIncorrectCompanyId
from src.test_workspace.users.update_user_with_incorrect_user_id_027 import UpdateUserWithIncorrectUserId


@pytest.mark.users
def test_get_users_with_limit_and_offset_016(get_users):
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
    parameters = {"limit": 10, "offset": 5, "status": "ACTIVE"}

    api = GetUsersWithLimitAndOffset(get_users(parameters))
    api.run_tests()

@pytest.mark.skip("{id записи об ошибке} Вместо 422 получаем статус-код 200. Skip-аем пока не починят")
@pytest.mark.users
def test_get_users_with_incorrect_limit_017(get_users):
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
    parameters = {"limit": -1}

    api = GetUsersWithIncorrectLimit(get_users(parameters))
    api.run_tests()

@pytest.mark.users
def test_get_users_with_incorrect_str_limit_and_offset_018(get_users):
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
    parameters = {"limit": "abc", "offset": "abc"}

    api = GetUsersWithIncorrectLimit(get_users(parameters))
    api.run_tests()

@pytest.mark.users
def test_get_users_list_by_http_019():
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

    api = GetUsersListByHttp(response_object)
    api.run_tests()

@pytest.mark.users
def test_create_user_020(create_and_delete_user):
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
    api = CreateUser(create_and_delete_user(user_data))
    api.run_tests()

@pytest.mark.users
def test_create_user_with_incorrect_company_id_021(create_user):
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
    user_data = {"first_name": "Вальдемар", "last_name": "Евлампиевич", "company_id": 33}

    api = CreateUserWithIncorrectCompanyId(create_user(user_data))
    api.run_tests()

@pytest.mark.users
@pytest.mark.parametrize("user_data",
             [({"first_name": "1", "last_name": None, "company_id": 3}),
              ({"first_name": "1", "company_id": 3})], ids=str)
def test_create_user_with_null_and_empty_last_name_022(user_data, create_user):
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
    api = CreateUserWithNullAndEmptyLastName(create_user(user_data))
    api.run_tests(user_data)

@pytest.mark.users
def test_create_user_in_with_closed_status_023(create_user):
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
    user_data = {"first_name": "Вальдемар", "last_name": "Евлампиевич", "company_id": 5}

    api = CreateUserWithClosedStatus(create_user(user_data))
    api.run_tests()

@pytest.mark.users
def test_get_user_by_id_024(create_and_delete_user, get_user_by_id):
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
    api = GetUserById(get_user_by_id(user_id))
    api.run_tests()

@pytest.mark.users
def test_get_created_user_by_incorrect_id_025(get_user_by_id):
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

    api = GetCreatedUserByIncorrectId(get_user_by_id(user_id))
    api.run_tests()

@pytest.mark.users
def test_update_user_026(create_and_delete_user, update_user):
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
    update_data = {"first_name": "Гена", "last_name": "Пипеткин", "company_id": 3}
    response_object_create_user = create_and_delete_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    # Переходим к самому тесту
    api = UpdateUser(update_user(update_data, user_id))
    api.run_tests()

@pytest.mark.users
def test_update_user_with_incorrect_user_id_027(update_user):
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

    api = UpdateUserWithIncorrectUserId(update_user(update_data, user_id))
    api.run_tests()

@pytest.mark.users
def test_update_user_with_incorrect_company_id_028(create_and_delete_user, update_user):
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
    update_data = {"first_name": "Маня", "last_name": "Пена", "company_id": 33}
    response_object_create_user = create_and_delete_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    api = UpdateUserWithIncorrectCompanyId(update_user(update_data, user_id))
    api.run_tests()

@pytest.mark.users
def test_delete_user_029(create_user, delete_user):
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

    api = DeleteUser(delete_user(user_id))
    api.run_tests()

@pytest.mark.users
def test_twice_deleted_user_030(create_user, delete_user):
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
    api = TwiceDeletedUser(delete_user(user_id))
    api.run_tests(user_id)

@pytest.mark.users
def test_delete_user_with_incorrect_user_id_031(delete_user):
    """
    Удалить не существующего пользователя (не существующий user_id)

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В тексте ошибки указан отправленный нами "user_id"
    """
    user_id = 99999

    api = DeleteUserWithIncorrectUserId(delete_user(user_id))
    api.run_tests()

@pytest.mark.users
def test_issues_get_created_user_by_id_032(create_and_delete_user):
    """
    Это специальный тест, где мы получим заведомо не верный ответ от сервера.
    Получить данные пользователя по его user_id

    Ожидаемый результат:
        Статус-код 201;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Новая запись JSON ответа соответствует тому, что мы отправляли при регистрации + содержит Id созданного юзера.

    Полученный результат: статус код 202 (запрос был принят на обработку, но она не завершена),
        ключи first_name и last_name не соответствуют тому, что мы ожидали.
    """
    response_object_create_user = create_and_delete_user(user_data)
    user_id = response_object_create_user.json().get("user_id")

    #Переходим к самому тесту
    response_object = requests.get(baseUrl_issues_users + f"/{user_id}")
    api = IssuesGetCreatedUserById(response_object)
    api.run_tests()

@pytest.mark.users
def test_issues_create_user_033(delete_user):
    """
    Это специальный тест, где мы получим заведомо не верный ответ от сервера.
    Зарегистрировать нового пользователя (делаем громоздко внутри теста, не используем фикстуру, т.к. тут уникальный
    URL, и не хочется из-за него заводить новые фикстуры. Это, все-таки, специальная демонстрация возможных ошибок

    Ожидаемый результат:
        Запрос успешно отправлен;
        Статус-код 201;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
        Соединение безопасное, порт 443
        Новая запись JSON ответа соответствует тому, что мы отправляли при регистрации + содержит Id созданного юзера

    Полученный результат: все данные пользователя не совпадают
    """
    user_data = {"first_name": "Дыр", "last_name": "Пыр", "company_id": 3}
    payload = json.dumps(user_data)
    headers = {'Content-Type': 'application/json'}
    response_object = requests.post(baseUrl_issues_users, headers=headers, data=payload)
    user_id = response_object.json().get("user_id")

    api = IssuesCreateUser(response_object)
    api.run_tests()

    delete_user(user_id)




@pytest.mark.skip("Это черновик")
def test_test():
    """
    черновик
    print(response_object.__getstate__())  # вообще все выгружается, что есть
    """
