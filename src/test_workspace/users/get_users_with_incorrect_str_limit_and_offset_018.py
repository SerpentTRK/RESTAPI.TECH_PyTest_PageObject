from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods
from src.pydantic_shemas.model_422 import Model422

query_parameter_limit, query_parameter_offset = "limit", "offset"
limit_value, offset_value = "abc", "abc"

class GetUsersWithIncorrectLimit(GlobalMethods, UsersMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(422)
        self.validate_json_schema(Model422)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        self.validate_error_message_with_status_code_422(query_parameter_limit, limit_value)
        self.validate_error_message_with_status_code_422(query_parameter_offset, offset_value)