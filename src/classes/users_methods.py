import requests
from pytest_check import check
import re

from src.configuration import baseUrl_users


class UsersMethods:
    def __init__(self, response):
        self.response = response

    def limit_validation(self, limit_value):
        """
        Валидация работы limit. Должно быть выведено заданное количество пользователей
        """
        data_object = self.response.json().get("data")
        count_user_id = sum(1 for item in data_object if "user_id" in item)

        check.equal(count_user_id, limit_value,
                msg=f"Ошибка! В JSON-DATA ожидали {limit_value} компании, а фактическое значение = {count_user_id}")

    def offset_validation(self, offset_value):
        """
        Валидация работы offset.
        Проблема в том, что id пользователей начинаются не с 1, а произвольного числа,
        потому, чтобы понять, правильно в тесте работает offset или нет, нам надо сперва
        сделать запрос без offset, и взять resp.json().get("data")[offset].get("user_id") = id ножного нам
        по порядку пользователя в базе, и сразвнить с id первого пользователя из теста.
        """
        # надо получить "user_id", который станет первым с заданным offset
        limit_value = offset_value + 1
        parameters = {"limit": limit_value, "status": "ACTIVE"}
        response = requests.get(baseUrl_users, params=parameters)

        expected_user_id = response.json().get("data")[offset_value].get("user_id")
        received_user_id = self.response.json().get("data")[0].get("user_id")

        check.equal(expected_user_id, received_user_id,
                    msg=f"Ошибка! Со значением offset={offset_value} первым в списке должен находиться 'user_id': "
                        f"{expected_user_id}, а по факту на первой строчке стоит 'user_id': {received_user_id}")


    def user_validation(self, test_data):
        """
        Проверка на соответствие того, что пользователь в БД именно такой, каким его создали
        """
        response_data = self.response.json()

        for key in response_data.keys():
            if key in test_data:
                check.equal(test_data[key], response_data[key], msg=f"Ошибка! Переданное значение "
                f"'{str(test_data[key])}' не совпадает с зарегистрированным '{str(response_data[key])}'")


    def validate_response_message_about_error_404(self, user_id):
        """
        Валидация 404 ошибки. В тексте ошибки должен быть указан тот же "user_id", что и request-e
        """
        error_message = self.response.json().get("detail")["reason"]

        check.equal(error_message, f"User with requested id: {user_id} is absent",
            msg=f"Ошибка! В запросе был company_id: '{user_id}', а по факту получили {self.response.url}")

    def assert_response_message_about_error_400(self):
        """
        Валидация сообщения об ошибке.
        """
        error_message = self.response.json().get("detail")['reason']
        expected_message = "You can only register with companies with ACTIVE status"

        check.equal(error_message, expected_message,
                    msg=f"Ошибака! Полученное сообщение об ошибке:'{error_message}' "
                        f"не соответствует ожидаемому:'{expected_message}'")

    def validate_response_with_code_202(self):
        message_status_code_202 = None

        check.equal(message_status_code_202, self.response.json(),
            msg=f"Ошибка! Ожидаемое получить: '{message_status_code_202}', а получили: '{self.response.json()}'")

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
