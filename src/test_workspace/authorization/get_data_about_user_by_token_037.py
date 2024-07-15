from src.classes.authorization_methods import AuthMethods
from src.classes.global_methods import GlobalMethods
from src.configuration import authorization_data


class GetDataAboutUserByToken(GlobalMethods, AuthMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(200)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        self.validatde_user_authorization_data_by_token(authorization_data)