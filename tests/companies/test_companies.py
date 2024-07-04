import pytest
import requests

from src.configuration import baseUrl_companies
from src.classes.global_methods import GlobalMethods
from src.classes.companies_methods import CompaniesMethods

from src.pydantic_shemas.model_companies_200 import ModelCompanies200

@pytest.mark.companies
def test_001_get_companies_default_request():
    """
    Получить список компаний.

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 1000ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type":  "application/json"
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
        Response header "Content-Type" - "application/json"
        Response header "Connection" - "keep-alive"
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



def test_test():
    """
    Вспоминаем и проверяем...
    В JSON 3 компании, id первой в списке = 1, company_status = ACTIVE
    """
    params = {"limit": 5, "offset": 2}
    # response_object = requests.get(url=baseUrl_companies)
    response_object = requests.get(url=baseUrl_companies, params=params)

    # # вообще все выгружается, что есть
    # print(response_object.__getstate__())

    # print(response_object.json().get("data"))

    data_object = response_object.json().get("data")
    list_company_id_values = [value for item in data_object for key, value in item.items() if key == "company_id"]

    print(list_company_id_values)






