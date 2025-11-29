from datetime import datetime


class ValidationError(Exception):
    pass


class Validator:
    @staticmethod
    def validate_not_empty_string(value, field_name, max_length):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"Поле '{field_name}' не может быть пустым.")
        if len(value) > max_length:
            raise ValidationError(
                f"Поле '{field_name}' превышает максимальную длину в"
                f" {max_length} символов.")
        return value

    @staticmethod
    def validate_student_names(name, second_name):
        Validator.validate_not_empty_string(name, 'Имя студента', 100)
        Validator.validate_not_empty_string(second_name, 'Фамилия студента',
                                            100)

    @staticmethod
    def validate_book_title(title):
        Validator.validate_not_empty_string(title, 'Название книги', 100)

    @staticmethod
    def validate_group_dates(start_date, end_date):
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            raise ValidationError("Дата должны быть в формате ГГГГ-ММ-ДД.")

    @staticmethod
    def validate_mark_value(value):
        valid_marks = ['1', '2', '3', '4', '5']
        if str(value) not in valid_marks:
            raise ValidationError("Ожидаются цифры от 1 до 5.")
