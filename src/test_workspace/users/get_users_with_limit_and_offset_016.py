from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods
from src.pydantic_shemas.model_users_200 import ModelUsers200

limit_value, offset_value = 10, 5

class GetUsersWithLimitAndOffset(GlobalMethods, UsersMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(200)
        self.validate_time_from_request_to_response()
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_json_schema(ModelUsers200)

        self.limit_validation(limit_value)
        self.offset_validation(offset_value)