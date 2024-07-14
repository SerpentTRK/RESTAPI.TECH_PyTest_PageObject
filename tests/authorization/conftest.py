import requests
import pytest
import json

from src.configuration import baseUrl_create_token


def _create_token(login, password, timeout):

    payload = json.dumps({"login": login, "password": password, "timeout": timeout})
    headers = {'Content-Type': 'application/json'}
    response_object = requests.post(baseUrl_create_token, headers=headers, data=payload)

    return response_object
@pytest.fixture
def create_token():
    return _create_token


@pytest.fixture
def authorization():
    payload = json.dumps({"login": "Test_login", "password": "qwerty12345"})
    headers = {'Content-Type': 'application/json'}
    response_object = requests.post("https://send-request.me/api/auth/authorize", headers=headers, data=payload)
    token = response_object.json().get("token")
    return response_object
    # print(token)