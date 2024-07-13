
from src.classes.companies_methods import CompaniesMethods
from src.classes.global_methods import GlobalMethods

class GetCompaniesWithoutSsl(GlobalMethods, CompaniesMethods):
    def __init__(self, response):
        self.response = response
        super().__init__(response)

    def run_tests(self):
        self.validate_status_code(301)
        self.validate_response_header("Connection", "keep-alive")
        self.validate_time_from_request_to_response()

        assert self.response.url == "http://restapi.tech/api/companies"
        assert self.response.headers["Location"] == "https://restapi.tech/api/companies"


