from src.classes.global_methods import GlobalMethods
from src.pydantic_shemas.model_422 import Model422


class CreateUserWithNullAndEmptyLastName(GlobalMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self, user_data):
        self.validate_status_code(422)
        self.validate_json_schema(Model422)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        if "last_name" in user_data:
            self.validate_error_message_with_status_code_422(msg="Input should be a valid string")
        else:
            self.validate_error_message_with_status_code_422(msg="Field required")