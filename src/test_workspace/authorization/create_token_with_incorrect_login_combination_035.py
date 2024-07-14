from src.classes.authorization_methods import AuthMethods
from src.classes.global_methods import GlobalMethods


class CreateTokenWithIncorrectLoginCombination(GlobalMethods, AuthMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self, result_status_code, login):
        self.validate_status_code(result_status_code)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")

        self.validate_error_message_with_status_code_422(login)

        # else:
        #     test_object.assert_response_header("content-type", "application/json"). \
        #         assert_response_header("connection", "keep-alive"). \
        #         assert_https_request("443")
        #     test_object_auth.assert_response_message_about_error_403("Invalid password")
        #     test_object.validate_time_from_request_to_response(timedelta(microseconds=1500000))