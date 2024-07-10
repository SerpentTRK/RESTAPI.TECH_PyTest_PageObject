
from pytest_check import check
import re



class UsersMethods:
    def __init__(self, response):
        self.response = response

    def validate_users_quantity(self, users_quantity):
        """
        Валидация работы limit. Должно быть выведено заданное количество пользователей
        """
        data_object = self.response.json().get("data")
        count_user_id = sum(1 for item in data_object if "user_id" in item)

        # assert count_user_id == users_quantity, \
        #     f"Ошибка! В JSON-DATA ожидали {users_quantity} компании, а фактическое значение = {count_user_id}"
        check.equal(count_user_id, users_quantity,
                    msg=f"Ошибка! В JSON-DATA ожидали {users_quantity} компании, "
                        f"а фактическое значение = {count_user_id}")

    def offset_validation(self, offset_value):
        """
        Валидация работы offset. Должно быть выведено заданное количество пользователей
        """