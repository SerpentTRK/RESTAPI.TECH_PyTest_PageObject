
from src.classes.companies_methods import CompaniesMethods
from src.classes.global_methods import GlobalMethods

from src.pydantic_shemas.model_companies_200 import ModelCompanies200

limit_value, offset_value = 5, 2

class GetCompaniesWithLimitAndOffset(GlobalMethods, CompaniesMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(200)
        self.validate_time_from_request_to_response()
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_json_schema(ModelCompanies200)

        self.validate_limit(limit_value)
        self.offset_validation(offset_value)
