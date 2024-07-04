import re


class CompaniesMethods:
    def __init__(self, response):
        self.response = response

    def validate_json_schema(self, schema):
        """
        Валидация JSON-схемы
        """
        if isinstance(self.response.json(), list):
            for item in self.response.json():
                schema.model_validate(item)
        else:
            schema.model_validate(self.response.json())
        return self

    def validate_companies_statuses(self, company_status):
        """
        Валидация статуса компаний
        """
        data_object = self.response.json().get("data")

        for item in data_object:
            assert item["company_status"] == company_status, \
                f"Ошибка! Ожидали 'company_status': {company_status}, а получили {item['company_status']}"

    def validate_companies_quantity(self, company_quantity):
        """
        Валидация количества компаний
        """
        data_object = self.response.json().get("data")
        count_company_id = sum(1 for item in data_object if 'company_id' in item)

        assert count_company_id == company_quantity, \
            f"Ошибка! В JSON-DATA ожидали {company_quantity} компании, а фактическое значение = {count_company_id}"
        return self

    def validate_offset(self, offset_value):
        """
        Валидация работы offset
        Проверить работу offset мы можем, выбрав значения company_id. Зная, что первый company_id == 1, offset даст
        сдвиг первого сохраненного значения в company_id.
        Если offset == 2, то первое company_id == 3 (1 и 2 отбрасывает offset)
        """
        data_object = self.response.json().get("data")
        first_company_id = 1

        list_company_id_values = [value for item in data_object for key, value in item.items() if key == "company_id"]
        assert first_company_id + offset_value == list_company_id_values[0], \
            f"Ошибка! offset: {offset_value}. Ожидаемое значение 'company_id': {first_company_id + offset_value}, " \
            f"фактически значение 'company_id': {list_company_id_values[0]}"

    def validate_error_message_with_status_code_422(self, query_parameter, value):
        """
        Валидация сообщений об ошибках для разных query-параметров
        """
        if query_parameter == "company_status":
            for elem in self.response.json().get("detail"):
                assert elem["msg"] == "Input should be 'ACTIVE', 'CLOSED' or 'BANKRUPT'"
                assert elem["input"] == value
        if query_parameter == "limit":
            for elem in self.response.json().get("detail"):
                assert elem["msg"] == "Input should be a valid integer, unable to parse string as an integer"
                assert elem["input"] == value


    def __str__(self):
        return \
            f"\nRequested Url: {self.response.url} \n" \
            f"Status code: {self.response.status_code} \n" \
            f"Response body: {self.response.json().get('data')} \n" \
            f"Response headers: {self.response.headers}"

### Старые методы



    def validate_status_company(self, body_key, body_value):
        """
        Валидация нужных элементов json("body")
        """
        for dicts in self.response.json().get("data"):
            for key, value in dicts.items():
                if key == body_key:
                    assert value == body_value, "Не верный company_status"
                    return self

    def assert_limit_json_body_data(self, num):
        """
        Валидация json("body") c query-параметром limit
        """
        for key, value in self.response.json().get("meta").items():
            if key == "limit":
                len_data = value
        assert len(self.response.json().get("data")) == len_data == num, "Ошибка в работе limit"
        return self

    def assert_offset_json_body_data(self, offset_num, company_id):
        """
        Валидация json("body") c query-параметром offset
        """
        for key, value in self.response.json().get("meta").items():
            if key == "offset":
                offset_meta_data = value
        for dicts in self.response.json().get("data"):
            for key, value in dicts.items():
                if key == "company_id":
                    first_id = value

        assert offset_meta_data == offset_num and company_id == first_id, "Ошибка в работе offset"
        return self

    def assert_first_language_in_response(self, lang):
        """
        Если в JSON есть translation_lang, то первый язык должен быть EN
        """
        for dict in self.response.json().get("description_lang")[:1]:
            for key, value in dict.items():
                if key == "translation_lang":
                    assert value == lang, "Первый язык должен быть EN"
                    return self

    def assert_comparison_uri_in_request_and_response(self, url):
        """
        Проверка на совпадение URI из запроса и URI из ответа
        """
        assert self.response.url == url, "Адреса не совпадают"
        return self

    def assert_response_message_about_error_404(self, company_id):
        """
        Валидация 404 ошибки. В нем должен быть указан тот company_id, что и в URI
        """
        for key, value in self.response.json().get("detail").items():
            assert value == f"Company with requested id: {company_id} is absent", self
            return self

    def assert_response_message_about_error_422(self, resp_key, resp_value):
        """
        Валидация сообщения об 404 ошибке.
        """
        for dicts in self.response.json().get("detail"):
            for key, value in dicts.items():
                if key == resp_key:
                    assert value == resp_value
                    return self

    def assert_language(self, lang):
        """
        Валидация текста языка в тексте. Функция принимает алфавит и сверяет соответствие
        """
        text = self.response.json().get("description").split()  # [каждое, слово, отдельно]
        text = ''.join(text)  # вернулитекстизспискаудалилипробелы
        only_text = re.sub(r'[^\w\s]', '', text)  # удаляем все символы, отличные от букв

        for words in only_text:
            assert words.lower() in lang
            return self
