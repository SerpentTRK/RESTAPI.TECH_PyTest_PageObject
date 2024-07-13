from src.classes.global_methods import GlobalMethods
from src.classes.users_methods import UsersMethods
from src.pydantic_shemas.model_404 import Model404


class TwiceDeletedUser(GlobalMethods, UsersMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self, user_id):
        self.validate_status_code(404)
        self.validate_json_schema(Model404)
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        self.validate_response_message_about_error_404(user_id)