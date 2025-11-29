import os
import logging.config
from dotenv import load_dotenv
from db_utils import DBConnector, DBError
from student_system_manager import StudentManagementSystem, ValidationError
from presenter import ConsolePresenter

# Настраиваем логирование из файла logging.conf
try:
    logging.config.fileConfig('logging.conf')
except FileNotFoundError:
    logging.basicConfig(level=logging.INFO)
except Exception as e:
    print(f"Ошибка настройки логирования: {e}")
    logging.basicConfig(level=logging.INFO)


class ApplicationRunner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.student_system = None
        self.connection = None
        self._last_student_id = None
        self.presenter = ConsolePresenter()
        load_dotenv()

        self.DB_CONFIG = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_DATABASE'),
            'port': os.getenv('DB_PORT')
        }

        if not all(self.DB_CONFIG.values()):
            error_msg = "Ошибка загрузки конфигурации БД: проверьте .env файл."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        else:
            self.logger.info("Конфигурация БД успешно загружена")

    def run(self):
        try:
            self.logger.info("Запуск приложения")
            connector = DBConnector(self.DB_CONFIG)
            with connector.connect() as connection:
                self.connection = connection
                self.student_system = StudentManagementSystem(connector)
                self.logger.info(
                    "Соединение с БД установлено. Запуск демо-логики...")
                self._execute_demo_logic()
                self.connection.commit()
                self.logger.info(
                    "Все операции успешно выполнены и зафиксированы!")
                self._print_reports()

        except ValidationError as exp:
            self.logger.error(f"Ошибка валидации данных: {exp}")
            if self.connection:
                self.connection.rollback()
                self.logger.warning(
                    "Транзакция откачена из-за ошибки валидации.")
        except DBError as exp:
            self.logger.error(f"Ошибка базы данных: {exp}")
            if self.connection:
                self.connection.rollback()
                self.logger.warning("Транзакция откачена из-за ошибки БД.")
        except Exception as exp:
            self.logger.exception(f"Неизвестная ошибка: {exp}")
        finally:
            self.logger.info("Завершение работы приложения")

    def _execute_demo_logic(self):
        student_data = ('Александр', 'Соколовский')
        books_data = ['Статистика', 'Психология успеха', 'Программирование на '
                                                         'Python']
        group_data = ('Группа 777', '2025-10-01', '2025-12-30')
        subjects_data = ['Математика', 'Психология', 'Программирование']

        lessons_data_titles = [
            'Алгебра', 'Геометрия',  # Математика
            'КПТ', 'Гештальт-терапия',  # Психология
            'ООП', 'Базы данных'  # Программирование
        ]
        subject_assignments = [0, 0, 1, 1, 2, 2]

        marks_data_values = ['5', '4', '5', '4', '5', '4']

        self.logger.debug("Начало выполнения демо-логики")

        # 1. Создаем студента
        student_id = self.student_system.create_student(*student_data)
        self.logger.info(f"Создан студент с ID: {student_id}")

        # 2. Создаем книги
        self.student_system.create_books(books_data, student_id)
        self.logger.info(f"Созданы книги: {', '.join(books_data)}")

        # 3. Создаем группу и обновляем студента
        group_id = self.student_system.create_group(*group_data)
        self.student_system.update_student_group(student_id, group_id)
        self.logger.info(f"Создана группа с ID: {group_id}")

        # 4. Создаем предметы
        subject_ids = [self.student_system.create_subject(title) for title in
                       subjects_data]
        for i, subject_id in enumerate(subject_ids):
            self.logger.info(
                f"Создан предмет '{subjects_data[i]}' с ID: {subject_id}")

        # 5. Создаем занятия
        lesson_ids = []
        for i, lesson_title in enumerate(lessons_data_titles):
            subject_index = subject_assignments[i]
            lesson_id = self.student_system.create_lesson(
                lesson_title,
                subject_ids[subject_index]
            )
            lesson_ids.append(lesson_id)
            self.logger.info(
                f"Создано занятие '{lesson_title}' для предмета "
                f"'{subjects_data[subject_index]}' с ID: {lesson_id}")

        # 6. Добавляем оценки
        marks_to_insert = [
            (marks_data_values[i], lesson_ids[i], student_id)
            for i in range(len(lesson_ids))
        ]
        self.student_system.add_marks_bulk(marks_to_insert)
        self.logger.info(f"Добавлено {len(marks_to_insert)} оценок")
        self.logger.debug("Демо-логика завершена")

        self._last_student_id = student_id

    def _print_reports(self):
        student_id = self._last_student_id
        if student_id is None:
            return

        print("\n" + "=" * 80)

        marks_data, marks_desc = self.student_system.get_student_marks_report(
            student_id)
        self.presenter.print_table(marks_data, marks_desc, "ОЦЕНКИ СТУДЕНТА")

        full_data, full_desc = self.student_system.get_full_student_report(
            student_id)
        self.presenter.print_table(full_data, full_desc,
                                   "ПОЛНАЯ ИНФОРМАЦИЯ О СТУДЕНТЕ")

        self.logger.info("Отчеты сгенерированы")


if __name__ == "__main__":
    app = ApplicationRunner()
    app.run()
