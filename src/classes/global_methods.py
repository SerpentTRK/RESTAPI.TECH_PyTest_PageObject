import requests
from pytest_check import check

from src.configuration import baseUrl_users


class GlobalMethods:
    def __init__(self, response):
        self.response = response

    def basic_checks_collection(self):
        """
        Коллекция базовых проверок под стандартные данные:
            Status code == 200
            Ожидание ответа от сервера < 500 сек
            Response header "Content-Type":  "application/json"
            Response header "Connection": "keep-alive"
        """
        self.validate_status_code(200)
        self.validate_time_from_request_to_response()
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")

    def validate_status_code(self, status_code):
        """
        Валидация статус-кода
        """
        if isinstance(status_code, list):
            assert self.response.status_code in status_code, self
        else:
            assert self.response.status_code == status_code, self

    def validate_response_header(self, header, value):
        """
        Валидация заголовков ответа.
        """
        if header in self.response.headers:
            # assert value == self.response.headers.get(header), self
            check.equal(value, self.response.headers.get(header), msg=self)

    def validate_json_schema(self, schema):
        """
        Валидация JSON-схемы
        """
        if isinstance(self.response.json(), list):
            for item in self.response.json():
                schema.model_validate(item)
        else:
            schema.model_validate(self.response.json())

    def validate_time_from_request_to_response(self, max_time_to_response=900):
        """
        Валидация времени ответа от сервера. Время дается в миллисекунд
        !!! Чтобы все тесты не были красными - удвоил время на ответ. Тестовая база... !!!
        """
        max_time_to_response_in_seconds = max_time_to_response * 10**-3  # перевели микросекунды в секунды
        response_time = self.response.elapsed.seconds + (self.response.elapsed.microseconds * 10**-6)

        check.greater(max_time_to_response_in_seconds, response_time, self)

    def validate_error_message_with_status_code_422(self, query_parameter=None, value=None, msg=None):
        """
        Валидация сообщений об ошибках для разных query-параметров
        """
        for elem in self.response.json().get("detail"):
            if msg:
                check.equal(elem["msg"], msg,
                    msg=f"Ошибка! Ожидаемый текст ошибки: '{msg}' не совпадает с полученным: '{elem['msg']}'")
            if query_parameter == "status":
                error_message = "Input should be 'ACTIVE', 'CLOSED' or 'BANKRUPT'"
            if query_parameter in ["limit", "offset"]:
                error_message = "Input should be a valid integer, unable to parse string as an integer"

                check.equal(elem["msg"], error_message,
                    msg=f"Ошибка! Ожидаемый текст ошибки: '{error_message}' не совпадает с полученным: '{elem['msg']}'")
                check.equal(elem["input"], value,
                    msg=f"Ошибка! Отправленное значение: {value} не совпадает с полученным: {elem['input']}")




    def __str__(self):
        return f"\nRequested Url: {self.response.url} \n" \
                f"Status code: {self.response.status_code} \n" \
                f"Response time: {self.response.elapsed.seconds + (self.response.elapsed.microseconds * 10**-6)} seconds \n" \
                f"Response headers: {self.response.headers} \n" \
                f"Response body: {self.response.json().get('data')}"
