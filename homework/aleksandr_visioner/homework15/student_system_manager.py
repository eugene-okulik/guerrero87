from db_utils import DBConnector
from db_validator import Validator, ValidationError


class StudentManagementSystem:
    def __init__(self, db_connector: DBConnector):
        self.db = db_connector
        self.connection = db_connector.connection
        self.validator = Validator()

    def create_student(self, name, second_name):
        self.validator.validate_student_names(name, second_name)

        query = ("INSERT INTO students (name, second_name, group_id) "
                 "VALUES (%s, %s, NULL)")
        return self.db.execute_query(query, data=(name, second_name))

    def create_book(self, title, student_id):
        self.validator.validate_book_title(title)

        query = ("INSERT INTO books (title, taken_by_student_id) "
                 "VALUES (%s, %s)")
        return self.db.execute_query(query, data=(title, student_id))

    def create_group(self, title, start_date, end_date):
        self.validator.validate_not_empty_string(title,
                                                 'Название группы', 100)
        self.validator.validate_group_dates(start_date, end_date)

        query = ("INSERT INTO `groups` (title, start_date, end_date) VALUES ("
                 "%s, %s, %s)")
        return self.db.execute_query(query, data=(title, start_date, end_date))

    def update_student_group(self, student_id, group_id):
        if not isinstance(student_id, int) or not isinstance(group_id, int):
            error_msg = "ID студента и группы должны быть целыми числами."
            raise ValidationError(error_msg)

        query = "UPDATE students SET group_id = %s WHERE id = %s"
        self.db.execute_query(query, data=(group_id, student_id))

    def create_subject(self, title):
        self.validator.validate_not_empty_string(title, 'Название предмета',
                                                 100)

        query = "INSERT INTO subjects (title) VALUES (%s)"
        return self.db.execute_query(query, data=(title,))

    def create_lesson(self, title, subject_id):
        self.validator.validate_not_empty_string(title, 'Название занятия',
                                                 100)

        query = "INSERT INTO lessons (title, subject_id) VALUES (%s, %s)"
        return self.db.execute_query(query, data=(title, subject_id))

    def add_marks_bulk(self, marks_data_list):
        for mark_tuple in marks_data_list:
            value = mark_tuple[0]
            self.validator.validate_mark_value(value)

        query = ("INSERT INTO marks (value, lesson_id, student_id)"
                 " VALUES (%s, %s, %s)")
        self.db.execute_queries_many(query, marks_data_list)

    def get_student_marks_report(self, student_id):
        query = """
            SELECT m.value as оценка, l.title as занятие, s.title as предмет
            FROM marks m JOIN lessons l ON m.lesson_id = l.id
            JOIN subjects s ON l.subject_id = s.id
            WHERE m.student_id = %s
        """

        return self.db.execute_query(query, data=(student_id,))

    def get_full_student_report(self, student_id):
        query = """
                   SELECT st.name as имя, st.second_name as фамилия,
                   g.title as группа, b.title as книга, m.value as оценка,
                   l.title as занятие, s.title as предмет
                   FROM students st
                   LEFT JOIN `groups` g ON st.group_id = g.id
                   LEFT JOIN books b ON b.taken_by_student_id = st.id
                   LEFT JOIN marks m ON m.student_id = st.id
                   LEFT JOIN lessons l ON m.lesson_id = l.id
                   LEFT JOIN subjects s ON l.subject_id = s.id
                   WHERE st.id = %s
               """

        return self.db.execute_query(query, data=(student_id,))
