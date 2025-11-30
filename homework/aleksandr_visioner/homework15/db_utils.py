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
        # Прочитал в интернете, что такой метод безопаснее,
        # на сколько это правда?
        connection_params = self.config.copy()
        connection_params.update({
            'charset': 'utf8mb4',  # Поддержка всех Unicode символов
            'autocommit': False,  # Явное управление транзакциями
            'connect_timeout': 10,  # Таймаут подключения
        })

        try:
            connection = mysql.connector.connect(**connection_params)
            self.connection = connection
            return self.connection
        except mysql.connector.Error as e:
            raise DBError("Не удалось подключиться к БД") from e

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
                    return cursor.lastrowid  # Для INSERT/UPDATE/DELETE

        except mysql.connector.Error as e:
            raise DBError("Ошибка выполнения запроса") from e

    def execute_queries_many(self, query, data_list):
        self.execute_query(query, data=data_list, many=True)
