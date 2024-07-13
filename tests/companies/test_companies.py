
import pytest
import requests

from src.configuration import baseUrl_issues_companies

from src.test_workspace.companies.companies_with_incorrect_int_query_offset_008 import CompaniesWithIncorrectIntQueryOffset
from src.test_workspace.companies.companies_with_incorrect_str_query_offset_009 import \
    GetCompaniesWithIncorrectStrQueryOffset
from src.test_workspace.companies.get_compani_with_incorrect_status_ABCDE_005 import GetCompaniEithIncorrectStatusABCDE
from src.test_workspace.companies.get_companies_default_request_001 import GetCompaniesDefaultRequest
from src.test_workspace.companies.get_companies_with_limit_and_offset_003 import GetCompaniesWithLimitAndOffset
from src.test_workspace.companies.get_companies_without_ssl_002 import GetCompaniesWithoutSsl
from src.test_workspace.companies.get_companies_with_different_query_statuses_004 import \
    GetCompaniesWithDifferentQueryStatuses
from src.test_workspace.companies.get_companies_with_incorrect_int_query_limit_006 import \
    GetCompaniesWithIncorrectIntQueryLimit
from src.test_workspace.companies.get_companies_with_incorrect_str_query_limit_007 import \
    GetCompaniesWithIncorrectStrQueryLimit
from src.test_workspace.companies.get_company_by_id_010 import GetCompanyById
from src.test_workspace.companies.get_company_by_id_and_supported_language_012 import GetCompanyByIdAndSupportedLanguage
from src.test_workspace.companies.get_company_by_id_and_unsupported_language_013 import GetCompanyByIdAndUnsupportedLanguage
from src.test_workspace.companies.get_company_by_incorrect_id_011 import GetCompanyByIncorrectId
from src.test_workspace.companies.issues_get_companies_by_id_015 import IssuesGetCompaniesById
from src.test_workspace.companies.issues_get_companies_with_limit_offset_and_status_company_014 import \
    IssuesGetCompaniesWithLimitOffsetAndStatusCompany


@pytest.mark.companies
def test_get_companies_default_request_001(get_company):
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
    api = GetCompaniesDefaultRequest(get_company())
    api.run_tests()

@pytest.mark.companies
def test_get_companies_without_ssl_002():
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

    api = GetCompaniesWithoutSsl(response_object)
    api.run_tests()

@pytest.mark.companies
def test_get_companies_with_limit_and_offset_003(get_company):
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
    parameters = {"limit": 5, "offset": 2}

    api = GetCompaniesWithLimitAndOffset(get_company(parameters=parameters))
    api.run_tests()

@pytest.mark.companies
@pytest.mark.parametrize("company_status", [("ACTIVE"), ("CLOSED"), ("BANKRUPT")], ids=str)
def test_get_companies_with_different_query_statuses_004(company_status, get_company):
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
    parameters = {"status": company_status}

    api = GetCompaniesWithDifferentQueryStatuses(get_company(parameters=parameters))
    api.run_tests(company_status)

@pytest.mark.companies
def test_get_compani_with_incorrect_status_ABCDE_005(get_company):
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
    parameters = {"status": "ABCDE"}

    api = GetCompaniEithIncorrectStatusABCDE(get_company(parameters=parameters))
    api.run_tests()

@pytest.mark.skip("{id записи об ошибке} Вместо 422 получаем статус-код 200. Skip-аем пока не починят")
@pytest.mark.companies
def test_get_companies_with_incorrect_int_query_limit_006(get_company):
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
    parameters = {"limit": -1}

    api = GetCompaniesWithIncorrectIntQueryLimit(get_company(parameters=parameters))
    api.run_tests()

@pytest.mark.companies
def test_get_companies_with_incorrect_str_query_limit_007(get_company):
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
    parameters = {"limit": "abc"}

    api = GetCompaniesWithIncorrectStrQueryLimit(get_company(parameters=parameters))
    api.run_tests()

@pytest.mark.companies
def test_companies_with_incorrect_int_query_offset_008(get_company):
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
    parameters = {"offset": -1}

    api = CompaniesWithIncorrectIntQueryOffset(get_company(parameters=parameters))
    api.run_tests()

@pytest.mark.companies
def test_get_companies_with_incorrect_str_query_offset_009(get_company):
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
    parameters = {"offset": "abc"}

    api = GetCompaniesWithIncorrectStrQueryOffset(get_company(parameters=parameters))
    api.run_tests()

@pytest.mark.companies
def test_get_company_by_id_010(get_company):
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
    api = GetCompanyById(get_company(company_id="/1"))
    api.run_tests()

@pytest.mark.companies
def test_get_company_by_incorrect_id_011(get_company):
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
    api = GetCompanyByIncorrectId(get_company(company_id="/8"))
    api.run_tests()

def test_get_company_by_id_and_supported_language_012(get_company):
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
    headers = {"Accept-Language": "RU"}

    api = GetCompanyByIdAndSupportedLanguage(get_company(headers=headers, company_id="/1"))
    api.run_tests()

def test_get_company_by_id_and_unsupported_language_013(get_company):
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
    headers = {"Accept-Language": "KZ"}

    api = GetCompanyByIdAndUnsupportedLanguage(get_company(headers=headers, company_id="/1"))
    api.run_tests()

@pytest.mark.companies
# @pytest.mark.xfail(raises=AssertionError)
def test_issues_get_companies_with_limit_offset_and_status_company_014():
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
    response_object = requests.get(baseUrl_issues_companies, params=parameters)

    api = IssuesGetCompaniesWithLimitOffsetAndStatusCompany(response_object)
    api.run_tests()

@pytest.mark.companies
# @pytest.mark.xfail(raises=AssertionError)
def test_issues_get_companies_by_id_015():
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
    company_id = "/2"
    response_object = requests.get(baseUrl_issues_companies + company_id)

    api = IssuesGetCompaniesById(response_object)
    api.run_tests()







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

