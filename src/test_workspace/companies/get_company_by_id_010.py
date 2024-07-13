
from src.classes.companies_methods import CompaniesMethods
from src.classes.global_methods import GlobalMethods

from src.configuration import baseUrl_companies

from src.pydantic_shemas.model_company_200 import ModelCompany200

company_id = "/1"

class GetCompanyById(GlobalMethods, CompaniesMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(200)
        self.validate_time_from_request_to_response()
        self.validate_response_header("Content-type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_json_schema(ModelCompany200)

        self.validate_uri_in_request_and_response(baseUrl_companies + company_id)
        self.validate_first_language()