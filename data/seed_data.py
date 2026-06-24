"""
seed_data.py - Наполнение базы данными (минимум 5 курсов)
Запустите этот файл для заполнения данными
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage import SchoolStorage


def seed_database():
    """Наполняет базу данными"""
    storage = SchoolStorage()
    
    print("🌱 Наполнение базы данными...")
    
    # ===== Преподаватели =====
    teachers = [
        storage.add_teacher("Анна Иванова", "Математика"),
        storage.add_teacher("Петр Сидоров", "Программирование"),
        storage.add_teacher("Мария Петрова", "Физика"),
        storage.add_teacher("Иван Смирнов", "История"),
        storage.add_teacher("Елена Козлова", "Литература"),
    ]
    
    # ===== Студенты =====
    students = [
        storage.add_student("Алексей Петров", "alex@mail.com"),
        storage.add_student("Мария Соколова", "maria@mail.com"),
        storage.add_student("Дмитрий Кузнецов", "dima@mail.com"),
        storage.add_student("Ольга Васильева", "olga@mail.com"),
        storage.add_student("Сергей Новиков", "sergey@mail.com"),
        storage.add_student("Екатерина Морозова", "katya@mail.com"),
    ]
    
    # ===== Курсы =====
    courses = []
    
    # Курс 1: Математика
    course1 = storage.add_course("Высшая математика", "Математика", teachers[0].id)
    m1 = storage.add_module_to_course(course1.id, "Введение в математический анализ", "Основы")
    l1 = storage.add_lesson_to_module(course1.id, m1[2].id, "Пределы и непрерывность")
    storage.add_homework_to_lesson(course1.id, l1[2].id, "Задачи на пределы", "Решить 10 задач", 100)
    l2 = storage.add_lesson_to_module(course1.id, m1[2].id, "Производные")
    storage.add_homework_to_lesson(course1.id, l2[2].id, "Вычисление производных", "Найти производные функций", 100)
    courses.append(course1)
    
    # Курс 2: Программирование
    course2 = storage.add_course("Python для начинающих", "Программирование", teachers[1].id)
    m2 = storage.add_module_to_course(course2.id, "Основы Python", "Базовый синтаксис")
    l3 = storage.add_lesson_to_module(course2.id, m2[2].id, "Переменные и типы данных")
    storage.add_homework_to_lesson(course2.id, l3[2].id, "Практика по типам", "Написать простые программы", 100)
    l4 = storage.add_lesson_to_module(course2.id, m2[2].id, "Условные операторы")
    storage.add_homework_to_lesson(course2.id, l4[2].id, "Условная логика", "Решить задачи на if/else", 100)
    courses.append(course2)
    
    # Курс 3: Физика
    course3 = storage.add_course("Общая физика", "Физика", teachers[2].id)
    m3 = storage.add_module_to_course(course3.id, "Механика", "Движение тел")
    l5 = storage.add_lesson_to_module(course3.id, m3[2].id, "Кинематика")
    storage.add_homework_to_lesson(course3.id, l5[2].id, "Задачи на движение", "Решить задачи", 100)
    courses.append(course3)
    
    # Курс 4: История
    course4 = storage.add_course("История России", "История", teachers[3].id)
    m4 = storage.add_module_to_course(course4.id, "Средневековье", "IX-XVII века")
    l6 = storage.add_lesson_to_module(course4.id, m4[2].id, "Киевская Русь")
    courses.append(course4)
    
    # Курс 5: Литература
    course5 = storage.add_course("Русская литература XIX века", "Литература", teachers[4].id)
    m5 = storage.add_module_to_course(course5.id, "Золотой век", "Писатели XIX века")
    l7 = storage.add_lesson_to_module(course5.id, m5[2].id, "Пушкин А.С.")
    storage.add_homework_to_lesson(course5.id, l7[2].id, "Анализ стихотворений", "Написать анализ", 100)
    courses.append(course5)
    
    # ===== Зачисляем студентов =====
    enrollments = [
        (students[0].id, course1.id),  # Алексей на Математику
        (students[1].id, course1.id),  # Мария на Математику
        (students[0].id, course2.id),  # Алексей на Python
        (students[2].id, course2.id),  # Дмитрий на Python
        (students[3].id, course2.id),  # Ольга на Python
        (students[1].id, course3.id),  # Мария на Физику
        (students[4].id, course3.id),  # Сергей на Физику
        (students[5].id, course4.id),  # Екатерина на Историю
        (students[5].id, course5.id),  # Екатерина на Литературу
    ]
    
    for student_id, course_id in enrollments:
        storage.enroll_student(student_id, course_id)
    
    # ===== Выставляем оценки =====
    grades = [
        (students[0].id, course1.id, 85),  # Алексей - Математика
        (students[1].id, course1.id, 92),  # Мария - Математика
        (students[0].id, course2.id, 78),  # Алексей - Python
        (students[2].id, course2.id, 95),  # Дмитрий - Python
        (students[3].id, course2.id, 88),  # Ольга - Python
        (students[1].id, course3.id, 90),  # Мария - Физика
        (students[4].id, course3.id, 76),  # Сергей - Физика
        (students[5].id, course4.id, 93),  # Екатерина - История
        (students[5].id, course5.id, 87),  # Екатерина - Литература
    ]
    
    for student_id, course_id, grade in grades:
        storage.add_grade(student_id, course_id, grade)
    
    # ===== Оценки за ДЗ =====
    homework_grades = [
        (course1.id, l1[2].id, students[0].id, 90),
        (course1.id, l1[2].id, students[1].id, 95),
        (course1.id, l2[2].id, students[0].id, 80),
        (course1.id, l2[2].id, students[1].id, 88),
        (course2.id, l3[2].id, students[0].id, 75),
        (course2.id, l3[2].id, students[2].id, 100),
        (course2.id, l3[2].id, students[3].id, 85),
        (course2.id, l4[2].id, students[0].id, 82),
        (course2.id, l4[2].id, students[2].id, 92),
        (course2.id, l4[2].id, students[3].id, 78),
        (course3.id, l5[2].id, students[1].id, 88),
        (course3.id, l5[2].id, students[4].id, 70),
        (course5.id, l7[2].id, students[5].id, 85),
    ]
    
    for course_id, lesson_id, student_id, score in homework_grades:
        storage.grade_homework(course_id, lesson_id, student_id, score)
    
    # ===== Завершаем курсы =====
    # Завершаем курс 4 и 5
    storage.complete_course(course4.id)
    storage.complete_course(course5.id)
    
    print("✅ База данных успешно наполнена!")
    print(f"   - Преподавателей: {len(storage.teachers)}")
    print(f"   - Студентов: {len(storage.students)}")
    print(f"   - Курсов: {len(storage.courses)}")
    print(f"   - Модулей: {sum(len(c.modules) for c in storage.courses.values())}")
    print(f"   - Уроков: {sum(c.get_total_lessons() for c in storage.courses.values())}")


if __name__ == "__main__":
    seed_database()
