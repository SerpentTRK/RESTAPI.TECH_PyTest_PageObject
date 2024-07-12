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

        # assert count_user_id == users_quantity, \
        #     f"Ошибка! В JSON-DATA ожидали {users_quantity} компании, а фактическое значение = {count_user_id}"
        check.equal(count_user_id, limit_value,
                    msg=f"Ошибка! В JSON-DATA ожидали {limit_value} компании, "
                        f"а фактическое значение = {count_user_id}")

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

        # assert expected_user_id == received_user_id, f"Ошибка! Со значением offset={offset_value} первым в списке " \
        #                                              f"должен находиться 'user_id': {expected_user_id}, а по факту " \
        #                                              f"на первой строчке стоит 'user_id': {received_user_id}"
        check.equal(expected_user_id, received_user_id,
                    msg=f"Ошибка! Со значением offset={offset_value} первым в списке должен находиться 'user_id': "
                        f"{expected_user_id}, а по факту на первой строчке стоит 'user_id': {received_user_id}")


    def user_validation(self, user_data):
        """
        Проверка на соответствие того, что пользователь в БД именно такой, каким его создали
        """
        test_data = user_data
        response_data = self.response.json()

        for key in response_data.keys():
            if key in test_data:
                check.equal(test_data[key], response_data[key], msg=f"Ошибка! Переданное значение "
                f"'{str(test_data[key])}' не совпадает с зарегистрированным '{str(response_data[key])}'")
                # assert test_data[key] == response_data[key], \
                # f"Ошибка! Переданное значение '{test_data[key]}' не совпадает с зарегистрированным '{response_data[key]}'"

    def validate_response_message_about_error_404(self, user_id):
        """
        Валидация 404 ошибки. В тексте ошибки должен быть указан тот же "user_id", что и request-e
        """
        error_message = self.response.json().get("detail")["reason"]
        # assert error_message == f"User with requested id: {user_id} is absent", \
        #     f"Ошибка! В запросе был company_id: '{user_id}', а по факту получили {self.response.url}"
        check.equal(error_message, f"User with requested id: {user_id} is absent",
            msg=f"Ошибка! В запросе был company_id: '{user_id}', а по факту получили {self.response.url}")

    def assert_response_message_about_error_400(self):
        """
        Валидация сообщения об ошибке.
        """
        error_message = self.response.json().get("detail")['reason']
        expected_message = "You can only register with companies with ACTIVE status"

        # assert error_message == expected_message, \
        # f"Ошибака! Полученное сообщение об ошибке:'{error_message}' не соответствует ожидаемому:'{expected_message}'"
        check.equal(error_message, expected_message,
                    msg=f"Ошибака! Полученное сообщение об ошибке:'{error_message}' "
                        f"не соответствует ожидаемому:'{expected_message}'")
