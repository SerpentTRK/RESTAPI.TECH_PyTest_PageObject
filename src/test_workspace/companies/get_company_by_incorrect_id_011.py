from src.classes.companies_methods import CompaniesMethods
from src.classes.global_methods import GlobalMethods
from src.pydantic_shemas.model_404 import Model404

company_id = "/8"

class GetCompanyByIncorrectId(GlobalMethods, CompaniesMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(404)
        self.validate_response_header("Content-Type", "application/json")
        self.validate_response_header("Connection", "keep-alive")
        self.validate_json_schema(Model404)
        self.validate_time_from_request_to_response()

        self.validate_response_message_about_error_404(company_id)