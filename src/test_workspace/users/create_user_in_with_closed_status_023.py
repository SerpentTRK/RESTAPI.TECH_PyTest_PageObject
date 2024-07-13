from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods
from src.pydantic_shemas.model_https_400 import Model400


class CreateUserWithClosedStatus(GlobalMethods, UsersMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(400)
        self.validate_json_schema(Model400)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        self.assert_response_message_about_error_400()