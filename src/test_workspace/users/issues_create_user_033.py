from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods
from src.configuration import user_data
from src.pydantic_shemas.model_user_201 import ModelUser201


class IssuesCreateUser(GlobalMethods, UsersMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(201)
        self.validate_json_schema(ModelUser201)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        self.user_validation(user_data)
