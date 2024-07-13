import requests
import pytest
import json

from src.configuration import baseUrl_companies



@pytest.fixture
def get_company():
    def _wrapped(parameters={}, headers={}, company_id=None):

        if not company_id:
            url = baseUrl_companies
        else:
            url = baseUrl_companies + company_id

        response_object = requests.get(url, params=parameters, headers=headers)
        return response_object
    return _wrapped