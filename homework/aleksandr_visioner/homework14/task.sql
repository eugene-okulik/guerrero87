-- 1. Создаем студента
INSERT INTO students (name, second_name, group_id) 
VALUES ('Александр', 'Соколов', NULL);
SET @student_id = LAST_INSERT_ID();

-- 2. Создаем книги и указываем, что студент взял их
INSERT INTO books (title, taken_by_student_id) VALUES
('Математический анализ', @student_id),
('Психология для начинающих', @student_id),
('Программирование на Python', @student_id);
SET @book1_id = LAST_INSERT_ID() - 2;
SET @book2_id = LAST_INSERT_ID() - 1;
SET @book3_id = LAST_INSERT_ID();

-- Добавляем связи в таблицу student_books
INSERT INTO student_books (student_id, book_id) VALUES
(@student_id, @book1_id),
(@student_id, @book2_id),
(@student_id, @book3_id);

-- 3. Создаем группу и определяем студента в нее
INSERT INTO `groups` (title, start_date, end_date)
VALUES ('Группа 101', '2024-09-01', '2025-06-30');
SET @group_id = LAST_INSERT_ID();

-- Обновляем студента, устанавливаем группу
UPDATE students SET group_id = @group_id WHERE id = @student_id;

-- 4. Создаем учебные предметы
INSERT INTO subjects (title) VALUES
('Математика'),
('Психология'),
('Программирование');
SET @subject1_id = LAST_INSERT_ID() - 2;
SET @subject2_id = LAST_INSERT_ID() - 1;
SET @subject3_id = LAST_INSERT_ID();

-- 5. Создаем занятия для каждого предмета (по два на предмет)
INSERT INTO lessons (title, subject_id) VALUES
('Алгебра', @subject1_id),
('Геометрия', @subject1_id),
('Гештальт', @subject2_id),
('КПТ', @subject2_id),
('Основы Python', @subject3_id),
('ООП', @subject3_id);
SET @lesson1_id = LAST_INSERT_ID() - 5;
SET @lesson2_id = LAST_INSERT_ID() - 4;
SET @lesson3_id = LAST_INSERT_ID() - 3;
SET @lesson4_id = LAST_INSERT_ID() - 2;
SET @lesson5_id = LAST_INSERT_ID() - 1;
SET @lesson6_id = LAST_INSERT_ID();

-- 6. Ставим оценки студенту для всех созданных занятий
INSERT INTO marks (value, lesson_id, student_id) VALUES
('5', @lesson1_id, @student_id),
('4', @lesson2_id, @student_id),
('5', @lesson3_id, @student_id),
('3', @lesson4_id, @student_id),
('5', @lesson5_id, @student_id),
('4', @lesson6_id, @student_id);

-- Получение информации из базы данных:

-- 1. Все оценки студента
SELECT m.value as оценка, l.title as занятие, s.title as предмет
FROM marks m
JOIN lessons l ON m.lesson_id = l.id
JOIN subjects s ON l.subject_id = s.id
WHERE m.student_id = @student_id;

-- 2. Все книги, которые находятся у студента
SELECT b.title as книга
FROM books b
WHERE b.taken_by_student_id = @student_id;

-- 3. Вся информация о студенте (группа, книги, оценки с названиями занятий и предметов)
SELECT 
    st.name as имя,
    st.second_name as фамилия,
    g.title as группа,
    b.title as книга,
    m.value as оценка,
    l.title as занятие,
    s.title as предмет
FROM students st
LEFT JOIN `groups` g ON st.group_id = g.id
LEFT JOIN books b ON b.taken_by_student_id = st.id
LEFT JOIN marks m ON m.student_id = st.id
LEFT JOIN lessons l ON m.lesson_id = l.id
LEFT JOIN subjects s ON l.subject_id = s.id
WHERE st.id = @student_id;