
from src.classes.companies_methods import CompaniesMethods
from src.classes.global_methods import GlobalMethods
from src.pydantic_shemas.model_companies_200 import ModelCompanies200

query_parameter = "status"

class GetCompaniesWithDifferentQueryStatuses(GlobalMethods, CompaniesMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self, company_status):
        self.validate_status_code(200)
        self.validate_time_from_request_to_response()
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_json_schema(ModelCompanies200)

        self.validate_companies_statuses(company_status)