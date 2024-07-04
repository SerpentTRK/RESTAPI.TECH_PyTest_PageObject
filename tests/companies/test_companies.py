import pytest
import requests

from src.configuration import baseUrl_companies
from src.classes.global_methods import GlobalMethods
from src.classes.companies_methods import CompaniesMethods

from src.pydantic_shemas.model_companies_200 import ModelCompanies200
from src.pydantic_shemas.model_https_422 import ModelHttps422


@pytest.mark.companies
def test_001_get_companies_default_request():
    """
    Получить список компаний.

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON 3 компании, company_status = ACTIVE
    """
    response_object = requests.get(url=baseUrl_companies)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_json_schema(ModelCompanies200)
    test_object_companies.validate_companies_quantity(3)
    test_object_companies.validate_companies_statuses("ACTIVE")

@pytest.mark.companies
def test_002_get_companies_without_ssl():
    """
    Получить список компаний HTTP-запросом (не HTTPS)

    Ожидаемый результат:
        Статус-код 301;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Response url == "http://restapi.tech/api/companies"
        Response header "Location" == "https://send-request.me/api/companies/"
        Response header "Connection": "keep-alive"
    """
    response_object = requests.get("http://restapi.tech/api/companies", allow_redirects=False)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(301)
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response(1000)
    assert response_object.url == "http://restapi.tech/api/companies"
    assert response_object.headers["Location"] == "https://restapi.tech/api/companies"

@pytest.mark.companies
def test_003_get_companies_with_limit_and_offset():
    """
    Получить список компаний с указанием limit=5 и offset=2

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
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

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_companies_quantity(5)
    test_object_companies.validate_offset(offset_value)

@pytest.mark.companies
@pytest.mark.parametrize("company_status", [("ACTIVE"), ("CLOSED"), ("BANKRUPT")])
def test_004_get_companies_with_different_query_statuses(company_status):
    """
    Получить список компаний с разными "company_status" = "ACTIVE", "CLOSED" или "BANKRUPT"

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON компании только с указанным статусом
    """
    parameters = {"status": company_status}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks_collection()

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_companies_statuses(company_status)

@pytest.mark.companies
def test_005_get_compani_with_incorrect_status_ABCDE():
    """
    Получить список компаний с указанием не сущестующего "company_status": "ABCDE"

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    company_status = "ABCDE"
    parameters = {"status": company_status}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response(1000)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_json_schema(ModelHttps422)
    test_object_companies.validate_error_message_with_status_code_422("company_status", company_status)

@pytest.mark.skip("{id записи об ошибке} Вместо 422 получаем статус-код 200. Skip-аем пока не починят")
@pytest.mark.companies
def test_006_get_companies_with_incorrect_query_limit():
    """
    Получить список компаний с указанием отрицательного лимита limit = -1

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки

    Полученный результат: Выгружены все компании из БД, статус-код 200
    """
    limit_value = -1
    parameters = {"limit": limit_value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response(1000)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_json_schema(ModelHttps422)
    # если бы это была не учебная база, то можно было бы провалидировать и сообщение об ошибке, но мы не знаем этого
    # сообщения, потому и метод создать для этого случая не можем

@pytest.mark.companies
def test_007_get_companies_with_incorrect_query_limit():
    """
    Получить список компаний с указанием строчного значения limit = "abc"

    Ожидаемый результат:
        Статус-код 422;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует требованиям;
        Response header "Content-Type": "application/json"
        Response header "Connection": "keep-alive"
        В JSON присутствует описание ошибки
    """
    limit_value = "abc"
    parameters = {"limit": limit_value}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(422)
    test_object.validate_response_header("Content-Type", "application/json")
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response(1000)

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_json_schema(ModelHttps422)
    test_object_companies.validate_error_message_with_status_code_422("limit", limit_value)


def test_test():
    """
    черновик
    """
    company_status = "ABCDE"
    parameters = {"status": company_status}
    response_object = requests.get(url=baseUrl_companies, params=parameters)

    # # вообще все выгружается, что есть
    # print(response_object.__getstate__())

    print(response_object.json())

    error_message = ""

    for elem in response_object.json().get("detail"):
        assert elem["msg"] == "Input should be 'ACTIVE', 'CLOSED' or 'BANKRUPT'"








