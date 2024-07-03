import datetime

class GlobalMethods:
    def __init__(self, response):
        self.response = response

    def basic_checks(self):
        """
        Коллекция базовых проверок под стандартные данные:
            Status code == 200
            Ожидание ответа от сервера < 700 сек
            !!! Заголовок "content-type" == "application/json" !!!
        """
        self.validate_status_code(200)
        self.validate_time_from_request_to_response(800)
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
        return self

    def validate_time_from_request_to_response(self, max_time_to_response):
        """
        Валидация времени ответа от сервера
        """
        response_time = int(self.response.elapsed.microseconds) / 100  # 50333 => 503.33

        assert max_time_to_response > response_time, self
        return self

    def validate_response_header(self, header, value):
        """
        Валидация заголовков ответа.
        """
        if header in self.response.headers:
            assert value == self.response.headers.get(header), self
            return self

    def validate_schema(self, schema):
        """
        Валидация схемы
        """
        if isinstance(self.response.json(), list):
            for item in self.response.json():
                schema.model_validate(item)
        else:
            schema.model_validate(self.response.json())
        return self

    # def assert_https_request(self, port):
    #     assert port in self.response.headers.get("alt-svc"), f"Не безопасное соединение {self.response.headers.get('alt-svc')}"
    #     return  self


    def __str__(self):
        return f"\nRequested Url: {self.response.url} \n" \
                f"Status code: {self.response.status_code} \n" \
                f"Response time: {int(self.response.elapsed.microseconds / 100)} microseconds \n" \
                f"Response headers: {self.response.headers} \n" \
                f"Response body: {self.response.json().get('data')}"
