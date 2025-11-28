class ConsolePresenter:
    @staticmethod
    def print_table(rows, description, title="Результаты"):
        print(f"\n--- {title} ---")

        # 1. Извлекаем ТОЛЬКО имена столбцов (список строк)
        columns = [desc[0] for desc in description]

        if not columns or not rows:
            print("Нет данных для отображения.")
            return

        # 2. Рассчитываем максимальную ширину для каждого столбца
        col_widths = [len(col) for col in columns]
        for row in rows:
            for i, item in enumerate(row):
                if len(str(item)) > col_widths[i]:
                    col_widths[i] = len(str(item))

        # 3. Форматируем и выводим шапку
        header_line = "".join(f"{col:<{col_widths[i] + 2}}" for i, col in
                              enumerate(columns))
        print(header_line)
        print("-" * len(header_line))

        # 4. Форматируем и выводим данные
        for row in rows:
            row_line = "".join(f"{str(item):<{col_widths[i] + 2}}" for i,
                               item in enumerate(row))
            print(row_line)
        print("-" * len(header_line))
