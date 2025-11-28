import csv
from db_utils import DBConnector, DBError


class DataCheckerDetailed:
    def __init__(self, db_connector: DBConnector):
        self.db = db_connector

    def check_csv_data(self, csv_file_path):
        missing_data = []

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row_num, row in enumerate(reader, 1):
                    print(f"Проверка строки {row_num}: {row}")

                    if not self._check_row_in_db(row):
                        missing_data.append({
                            'row_number': row_num,
                            'data': row,
                            'missing_fields': self._get_missing_fields(row)
                        })

        except FileNotFoundError:
            raise DBError(f"Файл не найден по пути: {csv_file_path}")
        except Exception as e:
            raise DBError(f"Ошибка чтения CSV файла: {e}")

        return missing_data

    def _check_row_in_db(self, row):
        checks = [
            self._check_student_in_group(row),
            self._check_book_for_student(row),
            self._check_mark_for_lesson(row)
        ]

        return all(checks)

    def _check_student_in_group(self, row):
        query = """
            SELECT 1 FROM students s
            JOIN `groups` g ON s.group_id = g.id
            WHERE s.name = %s AND s.second_name = %s AND g.title = %s
        """
        try:
            result = self.db.execute_query(query, (
                row['name'], row['second_name'], row['group_title']
            ))
            return bool(result[0]) if result else False
        except DBError:
            return False

    def _check_book_for_student(self, row):
        query = """
            SELECT 1 FROM books b
            JOIN students s ON b.taken_by_student_id = s.id
            WHERE b.title = %s AND s.name = %s AND s.second_name = %s
        """
        try:
            result = self.db.execute_query(query, (
                row['book_title'], row['name'], row['second_name']
            ))
            return bool(result[0]) if result else False
        except DBError:
            return False

    def _check_mark_for_lesson(self, row):
        query = """
            SELECT 1 FROM marks m
            JOIN students s ON m.student_id = s.id
            JOIN lessons l ON m.lesson_id = l.id
            JOIN subjects sub ON l.subject_id = sub.id
            WHERE m.value = %s AND s.name = %s AND s.second_name = %s
            AND l.title = %s AND sub.title = %s
        """
        try:
            result = self.db.execute_query(query, (
                row['mark_value'], row['name'], row['second_name'],
                row['lesson_title'], row['subject_title']
            ))
            return bool(result[0]) if result else False
        except DBError:
            return False

    def _get_missing_fields(self, row):
        missing_fields = []

        if not self._check_student_in_group(row):
            missing_fields.append('student_in_group')

        if not self._check_book_for_student(row):
            missing_fields.append('book_for_student')

        if not self._check_mark_for_lesson(row):
            missing_fields.append('mark_for_lesson')

        return missing_fields
