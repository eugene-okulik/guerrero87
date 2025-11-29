import os
from dotenv import load_dotenv
from db_utils import DBConnector, DBError
from data_checker import DataCheckerDetailed
from presenter import ConsolePresenter


class ApplicationRunner:
    def __init__(self):
        self.data_checker = None
        self.connection = None
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
            raise ValueError(
                "Ошибка загрузки конфигурации БД: проверьте .env файл.")

    def run(self):
        try:
            connector = DBConnector(self.DB_CONFIG)
            with connector.connect() as connection:
                self.connection = connection
                self.data_checker = DataCheckerDetailed(connector)

                missing_data = self._check_csv_data()
                self.presenter.print_missing_data_report(missing_data)

        except DBError as exp:
            print(f"Ошибка базы данных: {exp}")
            if self.connection:
                self.connection.rollback()
        except Exception as exp:
            print(f"Неизвестная ошибка: {exp}")
            if self.connection:
                self.connection.rollback()

    def _check_csv_data(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(
            script_dir)))
        csv_file_path = os.path.join(root_dir, "homework", "eugene_okulik",
                                     "Lesson_16", "hw_data", "data.csv")

        return self.data_checker.check_csv_data(csv_file_path)


if __name__ == "__main__":
    app = ApplicationRunner()
    app.run()
