import requests

from src.configuration import baseUrl_companies
from src.classes.global_methods import GlobalMethods
from src.classes.companies_methods import CompaniesMethods

from src.pydantic_shemas.model_companies_200 import ModelCompanies200


def test_001_get_companies_list():
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
    test_object.basic_checks()

    test_object_companies = CompaniesMethods(response_object)
    test_object_companies.validate_json_schema(ModelCompanies200)
    test_object_companies.validate_companies_quantity(3)
    test_object_companies.validate_companies_statuses("ACTIVE")

def test_002_get_companies_list_by_http():
    """
    Получить список компаний HTTP-запросом (не HTTPS)

    Ожидаемый результат:
        Статус-код 301;
        Время ответа сервера - не превышает 1000ms;
        Response url: "http://restapi.tech/api/companies"
        Response header "Connection": "keep-alive"
    """
    response_object = requests.get("http://restapi.tech/api/companies", allow_redirects=False)

    test_object = GlobalMethods(response_object)
    test_object.validate_status_code(301)
    test_object.validate_response_header("Connection", "keep-alive")
    test_object.validate_time_from_request_to_response(1000)
    assert response_object.url == "http://restapi.tech/api/companies"





def test_test():
    """
    Вспоминаем и проверяем...
    В JSON 3 компании, id первой в списке = 1, company_status = ACTIVE
    """
    params = {"limit": 1, "offset": 2}
    response_object = requests.get(url=baseUrl_companies)
    # response_object = requests.get(url=baseUrl_companies, params=params)

    # # вообще все выгружается, что есть
    # print(response_object.__getstate__())
    print(response_object.json())
    data = response_object.json().get("data")

    for dicts in data:
        assert dicts["company_status"] == "ACTIVE"

    print(data)

    # print(response_object.json().get("data"))

# data = [{'company_id': 1, 'company_name': 'Tesla', 'company_address': 'Nicholastown, IL 80126', 'company_status': 'ACTIVE'}, {'company_id': 2, 'company_name': 'Google', 'company_address': '1093 Cooke Harbor Apt. 908', 'company_status': 'ACTIVE'}, {'company_id': 3, 'company_name': 'Toyota', 'company_address': 'Davidberg, MN 88952', 'company_status': 'ACTIVE'}]


