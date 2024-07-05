import re

"""
Во всех методах в конце поудалял "return self". В том году без этого не работало, а сейчас работает
"""

class CompaniesMethods:
    def __init__(self, response):
        self.response = response

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
        if query_parameter == "status":
            error_message = "Input should be 'ACTIVE', 'CLOSED' or 'BANKRUPT'"
        if query_parameter in ["limit", "offset"]:
            error_message = "Input should be a valid integer, unable to parse string as an integer"

        for elem in self.response.json().get("detail"):
            assert elem["msg"] == error_message, \
                f"Ошибка! Ожидаемый текст ошибки: '{error_message}' не совпадает с полученным: '{elem['msg']}'"
            assert elem["input"] == value, \
                f"Ошибка! Отправленное значение: {value} не совпадает с полученным: {elem['input']}"

    def validate_response_message_about_error_404(self, company_id):
        """
        Валидация 404 ошибки. В нем должен быть указан тот company_id, что и в URI
        """
        company_id = company_id.replace("/", "")
        for key, value in self.response.json().get("detail").items():
            assert value == f"Company with requested id: {company_id} is absent", \
                f"Ошибка! В запросе был company_id: '{company_id}', " \
                f"а по факту получили {''.join(c for c in value if c.isdigit())}"

    def validate_uri_in_request_and_response(self, request_uri):
        """
        Сравниваем URI из запроса и ответа
        """
        assert self.response.url == request_uri, \
            f"Ошибка! URI запроса: {request_uri} не совпадает с URI ответа: {self.response.url}"

    def validate_first_language(self):
        """
        Проверка того, что первый язык в "description_lang" == EN
        """
        first_language_by_default = "EN"
        data_object = self.response.json().get("description_lang")[0]
        first_language = [value for key, value in data_object.items() if key == "translation_lang"]

        assert "".join(first_language) == first_language_by_default, \
            f"Ошибка! Первым языком в 'description_lang' должен стоять '{first_language_by_default}', " \
            f"а мы получаем '{''.join(first_language)}'"

    def validate_language(self, language):
        """
        Валидация языка в тексте.
        """
        alphabets = {"RU": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
                     "EN": "abcdefghijklmnopqrstuvwxyz",
                     "PL": "aąbcćdeęfghijklłmnńoóprsśtuwyzźż",
                     "UA": "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"}
        symbols = alphabets[language]

        # удаляем все символы, отличные от букв, влключая пробелы. Потом убираем дублирующиеся буквы
        text = re.sub(r'[^\w\s]', '', self.response.json().get("description")).lower()
        text = set(text.replace(" ", ""))

        assert all(word in symbols for word in text), f"Ошибка! Символы в тексте не соответствуюет языку: '{language}'"