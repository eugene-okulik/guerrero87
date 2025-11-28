import mysql.connector


class DBError(Exception):
    pass


class DBConnector:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        if not self.config:
            raise ValueError("Параметры подключения к БД не предоставлены.")

        connection_params = self.config.copy()
        connection_params.update({
            'charset': 'utf8mb4',
            'autocommit': False,
            'connect_timeout': 10,
        })

        try:
            self.connection = mysql.connector.connect(**connection_params)
            return self
        except mysql.connector.Error as e:
            raise DBError(f"Не удалось подключиться к БД: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def execute_query(self, query, data=None, many=False):
        if not self.connection or not self.connection.is_connected():
            raise DBError("Соединение с БД не установлено или разорвано")

        try:
            with self.connection.cursor() as cursor:
                if many and data:
                    cursor.executemany(query, data)
                elif data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)

                if cursor.description:
                    return cursor.fetchall(), cursor.description
                else:
                    self.connection.commit()
                    return cursor.lastrowid

        except mysql.connector.Error as e:
            self.connection.rollback()
            raise DBError(f"Ошибка выполнения запроса: {e}")

    def execute_queries_many(self, query, data_list):
        self.execute_query(query, data=data_list, many=True)
