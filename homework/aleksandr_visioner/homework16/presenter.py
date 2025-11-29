class ConsolePresenter:
    @staticmethod
    def print_missing_data_report(missing_data):
        if missing_data:
            print("\n" + "=" * 80)
            print("ДЕТАЛЬНЫЙ ОТЧЕТ ОБ ОТСУТСТВУЮЩИХ ДАННЫХ:")
            print("=" * 80)

            for item in missing_data:
                row = item['data']
                print(f"\nСтрока {item['row_number']}:")
                print(f"  Студент: {row['name']} {row['second_name']}")
                print(f"  Группа: {row['group_title']}")
                print(f"  Книга: {row['book_title']}")
                print(f"  Предмет: {row['subject_title']}")
                print(f"  Урок: {row['lesson_title']}")
                print(f"  Оценка: {row['mark_value']}")

                missing_fields = item['missing_fields']
                print("  Отсутствующие связи:")
                if 'student_in_group' in missing_fields:
                    print("    - Студент не найден в указанной группе")
                if 'book_for_student' in missing_fields:
                    print("    - Книга не найдена у данного студента")
                if 'mark_for_lesson' in missing_fields:
                    print("    - Оценка не найдена за указанный урок")

            print(f"\nВсего записей с проблемами: {len(missing_data)}")
        else:
            print("\n✓ Все данные из CSV файла найдены в базе данных!")
