
from src.classes.companies_methods import CompaniesMethods
from src.classes.global_methods import GlobalMethods
from src.pydantic_shemas.model_422 import Model422

query_parameter, value = "limit", -1

class GetCompaniesWithIncorrectIntQueryLimit(GlobalMethods, CompaniesMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(422)
        self.validate_json_schema(Model422)
        self.validate_response_header("Content-Type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        # если бы это была не учебная база, то можно было бы провалидировать и сообщение об ошибке, но мы не знаем этого
        # сообщения, потому и метод создать для этого случая не можем
        self.validate_error_message_with_status_code_422(query_parameter, value)