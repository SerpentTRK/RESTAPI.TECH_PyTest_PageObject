from pytest_check import check

class AuthMethods:
    def __init__(self, response):
        self.response = response

    def validation_token(self, token_len):
        """
        Валидация токена
        """
        token = self.response.json()["token"]
        check.equal(len(token), token_len,
            msg=f"Ошибка! Ожидаема длинна токена: '{token_len}'. Полученная: '{len(token)}'")

    def validate_response_message_about_error_422(self, login=None):
        """
        Валидация сообщения об 422 ошибке.
        """
        received_error_message = self.response.json().get("detail")[0]["msg"]
        received_input = self.response.json().get("detail")[0]["input"]

        if login != None:
            expected_error_message = "String should have at least 3 characters"
            assert received_error_message == expected_error_message
            assert received_input == login
        else:
            expected_error_message = "Input should be a valid string"
            assert received_error_message == expected_error_message, f"{expected_error_message}, {received_error_message}"


    def validate_response_message_about_error_403(self):
        """
        Валидация сообщения об 403 ошибки.
        """
        expected_error_message = "Invalid login or password"
        received_error_message = self.response.json().get("detail")["reason"]

        check.equal(expected_error_message, received_error_message, msg=f"Ошибка! Ожидаемое сообщение об ошибке: "
                            f"'{expected_error_message}' не соответствует полученному: '{received_error_message}'")