import requests
import pytest
import json

@pytest.fixture
def get_request_responce(endpoint):
    return requests.get(url="https://restapi.tech" + endpoint)