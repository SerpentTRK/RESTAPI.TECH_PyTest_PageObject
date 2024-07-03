import requests

from src.configuration import baseUrl_companies
from src.classes.global_methods import GlobalMethods
from src.classes.companies_methods import CompaniesMethods

from src.pydantic_shemas.model_companies_200 import ModelCompanies200


def test_get_companies_list_001():
    """
    Получение списка компаний.

    Ожидаемый результат:
        Статус-код 200;
        Время ответа сервера - не превышает 800ms; (на боевых не должно быть больше 500)
        Схема JSON-ответа соответствует Требованиям;
        Response header "Content-Type":  "application/json"
        Response header "Connection": "keep-alive"
        В JSON 3 компании, id первой в списке = 1, company_status = ACTIVE
    """
    response_object = requests.get(url=baseUrl_companies)

    test_object = GlobalMethods(response_object)
    test_object.basic_checks()
    test_object.validate_schema(ModelCompanies200)

    test_object_companies = CompaniesMethods(response_object)






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
    print(response_object.headers)

    # print(response_object.json().get("data"))




