class Book:
    material = "бумага"
    has_text = True

    def __init__(self, title, author, pages, isbn, reserved=False):
        self.title = title
        self.author = author
        self.pages = pages
        self.isbn = isbn
        self.reserved = reserved

    def get_info(self):
        status = ", зарезервирована" if self.reserved else ""
        return (f"Название: {self.title}, Автор: {self.author}, страниц:"
                f" {self.pages}, материал: {self.material}{status}")


# Создаём обычные книги
books = [
    Book("Идиот", "Достоевский", 500, "978-5-699-12014-7"),
    Book("Мастер и Маргарита", "Булгаков", 480, "978-5-17-067581-1"),
    Book("1984", "Оруэлл", 320, "978-5-17-148138-6", reserved=True),
    Book("Преступление и наказание", "Достоевский", 672, "978-5-04-116640-3"),
    Book("Война и мир", "Толстой", 1225, "978-5-389-06256-6")
]

books[len(books) - 1].reserved = True


class SchoolBook(Book):
    def __init__(self, title, author, pages, isbn, subject, grade, has_tasks,
                 reserved=False):
        super().__init__(title, author, pages, isbn, reserved)
        self.subject = subject
        self.grade = grade
        self.has_tasks = has_tasks

    def get_info(self):
        status = ", зарезервирована" if self.reserved else ""
        return (f"Название: {self.title}, Автор: {self.author}, страниц:"
                f" {self.pages}, предмет: {self.subject},  класс:"
                f" {self.grade}{status}")


# Создаём учебники
school_books = [
    SchoolBook("Алгебра", "Иванов", 200, "978-5-09-071234-5", "Математика", 9,
               True),
    SchoolBook("История России", "Петров", 180, "978-5-09-071235-2", "История",
               10, True),
    SchoolBook("География", "Сидоров", 220, "978-5-09-071236-9",
               "География", 8,
               True, reserved=True),
    SchoolBook("Физика", "Кузнецов", 250, "978-5-09-071237-6", "Физика", 11,
               True),
    SchoolBook("Биология", "Смирнова", 190, "978-5-09-071238-3", "Биология", 7,
               True),
]

school_books[0].reserved = True

print("=== ОБЫЧНЫЕ КНИГИ ===")
for book in books:
    print(book.get_info())

print("\n=== УЧЕБНИКИ ===")
for book in school_books:
    print(book.get_info())
