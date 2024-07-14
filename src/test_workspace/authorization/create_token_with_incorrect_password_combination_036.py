from src.classes.authorization_methods import AuthMethods
from src.classes.global_methods import GlobalMethods


class CreateTokenWithIncorrectPasswordCombination(GlobalMethods, AuthMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self, result_status_code):

        if result_status_code == 403:
            self.validate_status_code(result_status_code)
            self.validate_response_header("Content-type", "application/json")
            self.validate_response_header("Connection", "keep-alive")
            self.validate_time_from_request_to_response()

            self.validate_response_message_about_error_403()

        if result_status_code == 422:
            self.validate_status_code(result_status_code)
            self.validate_response_header("Content-type", "application/json")
            self.validate_response_header("Connection", "keep-alive")
            self.validate_time_from_request_to_response()

            self.validate_error_message_with_status_code_422()