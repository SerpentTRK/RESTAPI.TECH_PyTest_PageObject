from src.classes.authorization_methods import AuthMethods
from src.classes.global_methods import GlobalMethods


class GetDataAboutUserWithTokenAfterTimeout(GlobalMethods, AuthMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(403)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")

        self.validate_response_message_about_error_403(timeout=True)