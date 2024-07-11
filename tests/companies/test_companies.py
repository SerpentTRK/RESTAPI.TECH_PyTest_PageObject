
import pytest
import requests

from src.configuration import baseUrl_companies
from src.classes.global_methods import GlobalMethods
from src.classes.companies_methods import CompaniesMethods


from src.pydantic_shemas.model_companies_200 import ModelCompanies200
from src.pydantic_shemas.model_company_200 import ModelCompany200
from src.pydantic_shemas.model_422 import Model422
from src.pydantic_shemas.model_404 import Model404


@pytest.mark.companies
def test_001_get_companies_default_request():
    """
    Получить список компаний.

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON 3 компании, company_status = ACTIVE
    """
    response_object = requests.get(url=baseUrl_companies)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompanies200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_limit(3)
    test_object_companies.validate_companies_statuses("ACTIVE")

@pytest.mark.companies
def test_002_get_companies_without_ssl():
    """
    Получить список компаний HTTP-запросом (не HTTPS)

    Ожидаемый результат:
        Статус-код 301;
        Время ответа сервера - не превышает 500ms;
        Response url == "http://restapi.tech/api/companies"
        Response header "Location" == "https://send-request.me/api/companies/"
        Response header "Connection": "keep-alive"
    """
    response_object = requests.get("http://restapi.tech/api/companies", allow_redirects=False)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(301)
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()
    assert response_object.url == "http://restapi.tech/api/companies"
    assert response_object.headers["Location"] == "https://restapi.tech/api/companies"

@pytest.mark.companies
def test_003_get_companies_with_limit_and_offset():
    """
    Получить список компаний с указанием limit=5 и offset=2

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON data 5 компаний (limit = 5), company_id первой = 3 (offset = 2)
    """
    limit_value, offset_value = 5, 2
    parameters = {"limit": limit_value, "offset": offset_value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompanies200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_limit(limit_value)
    test_object_companies.offset_validation(offset_value)

@pytest.mark.companies
@pytest.mark.parametrize("company_status", [("ACTIVE"), ("CLOSED"), ("BANKRUPT")])
def test_004_get_companies_with_different_query_statuses(company_status):
    """
    Получить список компаний с разными "company_status" = "ACTIVE", "CLOSED" или "BANKRUPT"

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON компании только с указанным статусом
    """
    query_parameter = "status"
    parameters = {query_parameter: company_status}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompanies200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_companies_statuses(company_status)

@pytest.mark.companies
def test_005_get_compani_with_incorrect_status_ABCDE():
    """
    Получить список компаний с указанием не сущестующего "company_status": "ABCDE"

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    query_parameter, value = "status", "ABCDE"
    parameters = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object.validate_error_message_with_status_code_422(query_parameter, value)

@pytest.mark.skip("{id записи об ошибке} Вместо 422 получаем статус-код 200. Skip-аем пока не починят")
@pytest.mark.companies
def test_006_get_companies_with_incorrect_int_query_limit():
    """
    Получить список компаний с указанием отрицательного лимита limit = -1

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки

    Полученный результат: Выгружены все компании из БД, статус-код 200
    """
    query_parameter, value = "limit", -1
    parameters = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    # если бы это была не учебная база, то можно было бы провалидировать и сообщение об ошибке, но мы не знаем этого
    # сообщения, потому и метод создать для этого случая не можем

@pytest.mark.companies
def test_007_get_companies_with_incorrect_str_query_limit():
    """
    Получить список компаний с указанием строчного значения limit = "abc"

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    query_parameter, value = "limit", "abc"
    parameters = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object.validate_error_message_with_status_code_422(query_parameter, value)

@pytest.mark.companies
def test_008_companies_with_incorrect_int_query_offset():
    """
    Получить список компаний с указанием отрицательного значения offset = -1

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON id первой в списке компании начинается = 1, и количество компаний = 3
        (выводятся значения по-умолчанию, как в test_001_get_companies_default_request)
    """
    query_parameter, value = "offset", -1
    parameters = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompanies200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_limit(3)
    test_object_companies.validate_companies_statuses("ACTIVE")

@pytest.mark.companies
def test_009_companies_with_incorrect_str_query_offset():
    """
    Получить список компаний с указанием строчного значения offset = "abc"

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    query_parameter, value = "offset", "abc"
    parameters = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_json_schema(Model422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object.validate_error_message_with_status_code_422(query_parameter, value)

@pytest.mark.companies
def test_010_get_company_by_id():
    """
    Получить информацию о компании по существующему Id=1 в эндпоинте URI

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON - company_id совпадает с id URI и первый в списке поддерживаемых языков EN;
    """
    company_id = "/1"
    response_object = requests.get(url=baseUrl_companies + company_id)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompany200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_uri_in_request_and_response(baseUrl_companies + company_id)
    test_object_companies.validate_first_language()

@pytest.mark.companies
def test_011_get_company_by_incorrect_id():
    """
    Получить информацию о компании по не существующему Id=8 в эндпоинте URI

    Ожидаемый результат:
        Статус-код 404;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON - присутствует ключ detail, значением является описание ошибки, company_id в
        сообщении совпадает с company_id из реквеста
    """
    company_id = "/8"
    response_object = requests.get(url=baseUrl_companies + company_id)

    test_object = GlobalMethods(response_object)
    test_object.validate_json_schema(Model404)
    test_object.validate_status_code(404)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response()

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_response_message_about_error_404(company_id)

def test_012_get_company_by_id_and_supported_language():
    """
    Получить информацию о компании по существующему id=1 в эндпоинте URI, с выбором поддерживаемого языка RU

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        company_id в JSON совпадает с id URI;
        Текст в description на Русском языке
    """
    company_id = "/1"
    query_parameter, value = "Accept-Language", "RU"
    headers = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies + company_id, headers=headers)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompany200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_uri_in_request_and_response(baseUrl_companies + company_id)
    test_object_companies.validate_language(value)

def test_013_get_company_by_id_and_unsupported_language():
    """
    Получить информацию о компании по существующему id=1 в эндпоинте URI, с выбором не поддерживаемого языка KZ

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        Company_id в JSON совпадает с id URI;
        Выгружены все поддерживаемы языки (как в тесте test_010_get_company_by_id),
        первый в списке поддерживаемых языков EN;
    """
    company_id = "/1"
    query_parameter, value = "Accept-Language", "KZ"
    headers = {query_parameter: value}
    response_object = requests.get(url=baseUrl_companies + company_id, headers=headers)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompany200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_uri_in_request_and_response(baseUrl_companies + company_id)
    test_object_companies.validate_first_language()

@pytest.mark.companies
# @pytest.mark.xfail(raises=AssertionError)
def test_014_issues_get_companies_with_limit_offset_and_status_company():
    """
    Это специальный тест, где мы получим заведомо не верный ответ от сервера.
    Получение списка компаний с указанием limit=1 ,offset=1 и status_company = ACTIVE

    Ожидаемый результат:
        татус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"

    Полученный результат: падает валидация offset и company-status:
        Ошибка! offset: 1. Ожидаемое значение 'company_id': 2, фактически значение 'company_id': 6
        Ошибка! Ожидали 'company_status': ACTIVE, а получили CLOSED
    """
    parameters = {"limit": 1, "offset": 1, "status": "ACTIVE"}
    response_object = requests.get("https://restapi.tech/api/issues/companies", params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompanies200)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_limit(1)
    test_object_companies.offset_validation(1)
    test_object_companies.validate_companies_statuses("ACTIVE")

@pytest.mark.companies
# @pytest.mark.xfail(raises=AssertionError)
def test_015_issues_get_companies_by_id():
    """
    Это специальный тест, где мы получим заведомо не верный ответ от сервера.
    Получение компании по company_id

    Ожидаемый результат:
        Запрос успешно отправлен;
        Статус-код 200;
        Время ответа сервера - не превышает 500ms;
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
        В JSON - company_id совпадает с id URI и первый в списке поддерживаемых языков EN;

    Полученный результат: Превышено время ожидания ответа от сервера
    """
    company_id = "2"
    response_object = requests.get("https://restapi.tech/api/issues/companies/" + company_id)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()
    test_object.validate_json_schema(ModelCompany200)





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









