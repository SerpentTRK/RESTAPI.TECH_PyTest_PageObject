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

    def validatde_user_authorization_data_by_token(self, user_authorization_data):
        """
        Валидация авторизационных данных пользовтеля, полученных по токену
        """
        expected_name = user_authorization_data[0]
        response_name = self.response.json().get('user_name')
        expected_email = expected_name + "@example.com"
        response_email = self.response.json().get("email_address")

        check.equal(expected_name, response_name, msg=f"Ошибка! Ожидаемое значение 'user_name': {expected_name} "
                            f"не соответствует полученному: {response_name}")
        check.equal(expected_email, response_email, msg=f"Ошибка! Ожидаемое значение 'email_address': {expected_email} "
                            f"не соответствует полученному: {response_email}")

    def validate_error_message_with_status_code_422(self, login=None):
        """
        Валидация сообщения об 422 ошибке.
        """
        received_error_message = self.response.json().get("detail")[0]["msg"]
        received_input = self.response.json().get("detail")[0]["input"]

        if login != None:
            expected_error_message = "String should have at least 3 characters"
            check.equal(received_error_message, expected_error_message,
                        msg=f"Ошибка! {received_error_message} != {expected_error_message}")
            check.equal(received_input, login,
                        msg=f"Ошибка! {received_input} != {login}")
        else:
            expected_error_message = "Input should be a valid string"
            check.equal(received_error_message, expected_error_message,
                        msg=f"Ошибка! {expected_error_message} != {received_error_message}")

    def validate_response_message_about_error_403(self, login_or_pass=False, token=False, timeout=False):
        """
        Валидация сообщения об 403 ошибки.
        """
        if token:
            expected_error_message = "Token is incorrect. Please login and try again"
        if timeout:
            expected_error_message = "Token is expired. Please login and try again"
        if login_or_pass:
            expected_error_message = "Invalid login or password"

        received_error_message = self.response.json().get("detail")["reason"]

        check.equal(expected_error_message, received_error_message, msg=f"Ошибка! Ожидаемое сообщение об ошибке: "
                            f"'{expected_error_message}' не соответствует полученному: '{received_error_message}'")