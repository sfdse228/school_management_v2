#!/usr/bin/env python3
"""
main.py - Система управления онлайн-школой v2.0 (CLI)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.storage import SchoolStorage
from src.analytics import Analytics
from src.export import CSVExporter
from src.visualizer import Visualizer
from src.logger_setup import logger


class SchoolCLI:
    """Консольный интерфейс школы v2.0"""
    
    def __init__(self):
        self.storage = SchoolStorage()
        self.analytics = Analytics(self.storage)
        self.exporter = CSVExporter(self.storage)
        self.visualizer = Visualizer(self.storage)
    
    def show_menu(self):
        print("\n" + "=" * 50)
        print("🏫 СИСТЕМА УПРАВЛЕНИЯ ОНЛАЙН-ШКОЛОЙ v2.0")
        print("=" * 50)
        print("1. 👨‍🎓 Добавить студента")
        print("2. 👨‍🏫 Добавить преподавателя")
        print("3. 📚 Создать курс")
        print("4. 📋 Список всех курсов")
        print("5. ➕ Зачислить студента на курс")
        print("6. 👨‍🏫 Назначить преподавателя на курс")
        print("7. 📝 Выставить оценку")
        print("8. ✅ Завершить курс")
        print("9. 📊 Отчёт по студенту")
        print("10. 🏆 Топ студентов")
        print("11. 📈 Статистика курса")
        print("12. 👨‍🏫 Отчёт по преподавателю")  # НОВОЕ
        print("13. 📚 Управление модулями и уроками")  # НОВОЕ
        print("14. 💾 Сохранить и выйти")
        print("15. 📊 Визуализация статистики студента")  # НОВОЕ
        print("16. 📤 Экспорт в CSV")  # НОВОЕ
        print("0. ❌ Выйти без сохранения")
        print("=" * 50)
    
    def add_student(self):
        print("\n👨‍🎓 ДОБАВЛЕНИЕ СТУДЕНТА")
        name = input("Имя: ").strip()
        email = input("Email: ").strip()
        if not name or not email:
            print("❌ Имя и email обязательны!")
            return
        student = self.storage.add_student(name, email)
        print(f"✅ Студент добавлен! ID: {student.id}")
    
    def add_teacher(self):
        print("\n👨‍🏫 ДОБАВЛЕНИЕ ПРЕПОДАВАТЕЛЯ")
        name = input("Имя: ").strip()
        specialization = input("Специализация: ").strip()
        if not name or not specialization:
            print("❌ Имя и специализация обязательны!")
            return
        teacher = self.storage.add_teacher(name, specialization)
        print(f"✅ Преподаватель добавлен! ID: {teacher.id}")
    
    def add_course(self):
        print("\n📚 СОЗДАНИЕ КУРСА")
        name = input("Название: ").strip()
        topic = input("Тема: ").strip()
        if not name or not topic:
            print("❌ Название и тема обязательны!")
            return
        teachers = self.storage.get_all_teachers()
        teacher_id = None
        if teachers:
            print("\nДоступные преподаватели:")
            for i, t in enumerate(teachers, 1):
                print(f"  {i}. {t.name} ({t.specialization})")
            choice = input("Выберите преподавателя (номер, или Enter пропустить): ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(teachers):
                    teacher_id = teachers[idx].id
        course = self.storage.add_course(name, topic, teacher_id)
        print(f"✅ Курс создан! ID: {course.id}")
    
    def list_courses(self):
        print("\n📋 СПИСОК КУРСОВ")
        courses = self.storage.get_all_courses()
        if not courses:
            print("📭 Нет курсов")
            return
        for course in courses:
            teacher = self.storage.get_teacher(course.teacher_id)
            teacher_name = teacher.name if teacher else "Не назначен"
            print(f"\n📚 {course}")
            print(f"   ID: {course.id}")
            print(f"   Преподаватель: {teacher_name}")
            print(f"   Студентов: {len(course.students)}")
            print(f"   Модулей: {len(course.modules)}")
            print(f"   Уроков: {course.get_total_lessons()}")
            print(f"   Статус: {course.status}")
    
    def enroll_student(self):
        print("\n➕ ЗАЧИСЛЕНИЕ СТУДЕНТА")
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        choice = input("Выберите студента (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(students)):
            return
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nАктивные курсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name} ({c.topic})")
        choice = input("Выберите курс (номер): ").strip()
        if not choice.isdigit():
            return
        idx2 = int(choice) - 1
        if not (0 <= idx2 < len(courses)):
            return
        success, msg = self.storage.enroll_student(students[idx].id, courses[idx2].id)
        print(f"{'✅' if success else '❌'} {msg}")
    
    def assign_teacher_to_course(self):
        print("\n👨‍🏫 НАЗНАЧЕНИЕ ПРЕПОДАВАТЕЛЯ")
        teachers = self.storage.get_all_teachers()
        if not teachers:
            print("❌ Нет преподавателей")
            return
        print("\nПреподаватели:")
        for i, t in enumerate(teachers, 1):
            print(f"  {i}. {t.name} ({t.specialization})")
        choice = input("Выберите преподавателя (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(teachers)):
            return
        courses = [c for c in self.storage.get_active_courses() if c.teacher_id != teachers[idx].id]
        if not courses:
            print("❌ Нет доступных курсов")
            return
        print("\nДоступные курсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name}")
        choice = input("Выберите курс (номер): ").strip()
        if not choice.isdigit():
            return
        idx2 = int(choice) - 1
        if not (0 <= idx2 < len(courses)):
            return
        success, msg = self.storage.assign_teacher(teachers[idx].id, courses[idx2].id)
        print(f"{'✅' if success else '❌'} {msg}")
    
    def add_grade(self):
        print("\n📝 ВЫСТАВЛЕНИЕ ОЦЕНКИ")
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        choice = input("Выберите студента (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(students)):
            return
        student = students[idx]
        if not student.courses:
            print(f"❌ Студент {student.name} не зачислен ни на один курс")
            return
        print(f"\nКурсы {student.name}:")
        for i, course_id in enumerate(student.courses, 1):
            course = self.storage.get_course(course_id)
            if course:
                print(f"  {i}. {course.name}")
        choice = input("Выберите курс (номер): ").strip()
        if not choice.isdigit():
            return
        idx2 = int(choice) - 1
        if not (0 <= idx2 < len(student.courses)):
            return
        grade = input("Введите оценку (0-100): ").strip()
        if not grade.isdigit():
            print("❌ Оценка должна быть числом!")
            return
        success, msg = self.storage.add_grade(student.id, student.courses[idx2], int(grade))
        print(f"{'✅' if success else '❌'} {msg}")
    
    def complete_course(self):
        print("\n✅ ЗАВЕРШЕНИЕ КУРСА")
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nАктивные курсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name} ({c.topic}) - {len(c.students)} студентов")
        choice = input("Выберите курс для завершения (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            return
        success, msg = self.storage.complete_course(courses[idx].id)
        print(f"{'✅' if success else '❌'} {msg}")
    
    def student_report(self):
        print("\n📊 ОТЧЁТ ПО СТУДЕНТУ")
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        choice = input("Выберите студента (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(students)):
            return
        report = self.storage.get_student_report(students[idx].id)
        if not report:
            print("❌ Студент не найден")
            return
        print("\n" + "=" * 50)
        print(f"📊 ОТЧЁТ ПО СТУДЕНТУ: {report['student']}")
        print("=" * 50)
        print(f"📧 Email: {report['email']}")
        print(f"📚 Всего курсов: {report['total_courses']}")
        print(f"⭐ Средняя оценка: {report['average_grade']:.2f}")
        if report['active_courses']:
            print(f"\n🟢 Активные курсы ({len(report['active_courses'])}):")
            for c in report['active_courses']:
                print(f"  • {c['name']} (Преподаватель: {c['teacher']})")
        if report['completed_courses']:
            print(f"\n✅ Завершённые курсы ({len(report['completed_courses'])}):")
            for c in report['completed_courses']:
                hw_str = f", ДЗ: {c.get('homework_scores', [])}" if c.get('homework_scores') else ""
                print(f"  • {c['name']} - Оценки: {c['grades']} (ср.: {c['average']}){hw_str}")
        print("=" * 50)
    
    def top_students(self):
        print("\n🏆 ТОП СТУДЕНТОВ")
        top = self.analytics.get_top_students(5)
        if not top:
            print("📭 Нет данных об успеваемости")
            return
        print("=" * 50)
        print(f"{'#':>3} {'Имя':<20} {'Ср. оценка':<12} {'Курсов':<8}")
        print("-" * 50)
        for i, student in enumerate(top, 1):
            print(f"{i:>3} {student['name']:<20} {student['average_grade']:<12} {student['courses_completed']:<8}")
        print("=" * 50)
    
    def course_statistics(self):
        print("\n📈 СТАТИСТИКА КУРСА")
        courses = self.storage.get_all_courses()
        if not courses:
            print("❌ Нет курсов")
            return
        print("\nКурсы:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name} ({c.status})")
        choice = input("Выберите курс (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            return
        stats = self.analytics.get_course_statistics(courses[idx].id)
        if not stats:
            print("❌ Курс не найден")
            return
        print("\n" + "=" * 50)
        print(f"📈 СТАТИСТИКА КУРСА: {stats['course_name']}")
        print("=" * 50)
        print(f"📚 Тема: {stats['topic']}")
        print(f"📊 Статус: {stats['status']}")
        print(f"👨‍🏫 Преподаватель: {stats['teacher']}")
        print(f"👨‍🎓 Студентов: {stats['students_count']}")
        print(f"📦 Модулей: {stats['modules_count']}")
        print(f"📖 Уроков: {stats['lessons_count']}")
        print(f"📝 Всего оценок: {stats['grades_count']}")
        print(f"⭐ Средняя оценка: {stats['average_grade']:.2f}")
        print(f"⬆ Максимальная: {stats['max_grade']}")
        print(f"⬇ Минимальная: {stats['min_grade']}")
        print(f"📝 Оценок за ДЗ: {stats['homework_scores_count']}")
        print(f"⭐ Средняя за ДЗ: {stats['homework_avg']:.2f}")
        print("=" * 50)
    
    def teacher_report(self):
        """Задание 8: Отчёт по преподавателю"""
        print("\n👨‍🏫 ОТЧЁТ ПО ПРЕПОДАВАТЕЛЮ")
        teachers = self.storage.get_all_teachers()
        if not teachers:
            print("❌ Нет преподавателей")
            return
        print("\nПреподаватели:")
        for i, t in enumerate(teachers, 1):
            print(f"  {i}. {t.name} ({t.specialization})")
        choice = input("Выберите преподавателя (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(teachers)):
            return
        stats = self.analytics.get_teacher_statistics(teachers[idx].id)
        if not stats:
            print("❌ Статистика не найдена")
            return
        print("\n" + "=" * 50)
        print(f"👨‍🏫 ОТЧЁТ ПО ПРЕПОДАВАТЕЛЮ: {stats['teacher_name']}")
        print("=" * 50)
        print(f"📚 Специализация: {stats['specialization']}")
        print(f"📊 Всего курсов: {stats['total_courses']}")
        print(f"🟢 Активных курсов: {stats['active_courses_count']}")
        print(f"✅ Завершённых курсов: {stats['completed_courses_count']}")
        print(f"👨‍🎓 Всего студентов: {stats['total_students']}")
        print(f"⭐ Средняя успеваемость студентов: {stats['average_student_grade']:.2f}")
        
        if stats['active_courses']:
            print("\n🟢 Активные курсы:")
            for c in stats['active_courses']:
                print(f"  • {c['name']} ({c['students']} студентов)")
        
        if stats['completed_courses']:
            print("\n✅ Завершённые курсы:")
            for c in stats['completed_courses']:
                print(f"  • {c['name']} - завершён: {c['completed_at']}, студентов: {c['students_count']}, ср. оценка: {c['average_grade']:.2f}")
        print("=" * 50)
    
    def manage_modules(self):
        """Задание 6: Управление модулями и уроками"""
        print("\n📚 УПРАВЛЕНИЕ МОДУЛЯМИ И УРОКАМИ")
        print("1. Добавить модуль в курс")
        print("2. Добавить урок в модуль")
        print("3. Добавить ДЗ к уроку")
        print("4. Выставить оценку за ДЗ")
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            self._add_module()
        elif choice == "2":
            self._add_lesson()
        elif choice == "3":
            self._add_homework()
        elif choice == "4":
            self._grade_homework()
        else:
            print("❌ Неверный выбор!")
    
    def _add_module(self):
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nВыберите курс:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name}")
        choice = input("Номер курса: ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            return
        title = input("Название модуля: ").strip()
        desc = input("Описание (опционально): ").strip()
        success, msg, _ = self.storage.add_module_to_course(courses[idx].id, title, desc)
        print(f"{'✅' if success else '❌'} {msg}")
    
    def _add_lesson(self):
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nВыберите курс:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name}")
        choice = input("Номер курса: ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            return
        course = courses[idx]
        if not course.modules:
            print("❌ В курсе нет модулей. Сначала добавьте модуль.")
            return
        print("\nВыберите модуль:")
        for i, m in enumerate(course.modules, 1):
            print(f"  {i}. {m.title}")
        choice = input("Номер модуля: ").strip()
        if not choice.isdigit():
            return
        idx2 = int(choice) - 1
        if not (0 <= idx2 < len(course.modules)):
            return
        title = input("Название урока: ").strip()
        desc = input("Описание (опционально): ").strip()
        success, msg, _ = self.storage.add_lesson_to_module(
            course.id, course.modules[idx2].id, title, desc
        )
        print(f"{'✅' if success else '❌'} {msg}")
    
    def _add_homework(self):
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nВыберите курс:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name}")
        choice = input("Номер курса: ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            return
        course = courses[idx]
        lessons = course.get_all_lessons()
        if not lessons:
            print("❌ В курсе нет уроков")
            return
        print("\nВыберите урок:")
        for i, l in enumerate(lessons, 1):
            print(f"  {i}. {l.title}")
        choice = input("Номер урока: ").strip()
        if not choice.isdigit():
            return
        idx2 = int(choice) - 1
        if not (0 <= idx2 < len(lessons)):
            return
        title = input("Название ДЗ: ").strip()
        desc = input("Описание: ").strip()
        max_score = input("Максимальный балл (по умолчанию 100): ").strip()
        max_score = int(max_score) if max_score.isdigit() else 100
        success, msg = self.storage.add_homework_to_lesson(
            course.id, lessons[idx2].id, title, desc, max_score
        )
        print(f"{'✅' if success else '❌'} {msg}")
    
    def _grade_homework(self):
        """Задание 7: Выставить оценку за ДЗ"""
        print("\n📝 ВЫСТАВЛЕНИЕ ОЦЕНКИ ЗА ДЗ")
        courses = self.storage.get_active_courses()
        if not courses:
            print("❌ Нет активных курсов")
            return
        print("\nВыберите курс:")
        for i, c in enumerate(courses, 1):
            print(f"  {i}. {c.name}")
        choice = input("Номер курса: ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(courses)):
            return
        course = courses[idx]
        lessons = [l for l in course.get_all_lessons() if l.homework]
        if not lessons:
            print("❌ В курсе нет уроков с ДЗ")
            return
        print("\nВыберите урок с ДЗ:")
        for i, l in enumerate(lessons, 1):
            print(f"  {i}. {l.title} (ДЗ: {l.homework.title})")
        choice = input("Номер урока: ").strip()
        if not choice.isdigit():
            return
        idx2 = int(choice) - 1
        if not (0 <= idx2 < len(lessons)):
            return
        lesson = lessons[idx2]
        if not course.students:
            print("❌ На курсе нет студентов")
            return
        print("\nСтуденты на курсе:")
        for i, sid in enumerate(course.students, 1):
            student = self.storage.get_student(sid)
            if student:
                print(f"  {i}. {student.name}")
        choice = input("Выберите студента: ").strip()
        if not choice.isdigit():
            return
        idx3 = int(choice) - 1
        if not (0 <= idx3 < len(course.students)):
            return
        student_id = course.students[idx3]
        score = input(f"Оценка (0-{lesson.homework.max_score}): ").strip()
        if not score.isdigit():
            print("❌ Оценка должна быть числом")
            return
        success, msg = self.storage.grade_homework(
            course.id, lesson.id, student_id, int(score)
        )
        print(f"{'✅' if success else '❌'} {msg}")
    
    def visualize_student(self):
        """Задание 10: Визуализация статистики студента"""
        print("\n📊 ВИЗУАЛИЗАЦИЯ СТАТИСТИКИ СТУДЕНТА")
        students = self.storage.get_all_students()
        if not students:
            print("❌ Нет студентов")
            return
        print("\nСтуденты:")
        for i, s in enumerate(students, 1):
            print(f"  {i}. {s.name} ({s.email})")
        choice = input("Выберите студента (номер): ").strip()
        if not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(students)):
            return
        self.visualizer.plot_student_progress(students[idx].id)
    
    def export_csv(self):
        """Задание 9: Экспорт в CSV"""
        print("\n📤 ЭКСПОРТ В CSV")
        print("1. Экспорт отчёта по студенту")
        print("2. Экспорт отчёта по преподавателю")
        print("3. Экспорт отчёта по курсу")
        choice = input("Выберите тип отчёта: ").strip()
        if choice == "1":
            students = self.storage.get_all_students()
            if not students:
                print("❌ Нет студентов")
                return
            print("\nСтуденты:")
            for i, s in enumerate(students, 1):
                print(f"  {i}. {s.name} ({s.email})")
            c = input("Выберите студента (номер): ").strip()
            if not c.isdigit():
                return
            idx = int(c) - 1
            if not (0 <= idx < len(students)):
                return
            filename = self.exporter.export_student_report(students[idx].id)
            if filename:
                print(f"✅ Отчёт сохранён: {filename}")
        elif choice == "2":
            teachers = self.storage.get_all_teachers()
            if not teachers:
                print("❌ Нет преподавателей")
                return
            print("\nПреподаватели:")
            for i, t in enumerate(teachers, 1):
                print(f"  {i}. {t.name} ({t.specialization})")
            c = input("Выберите преподавателя (номер): ").strip()
            if not c.isdigit():
                return
            idx = int(c) - 1
            if not (0 <= idx < len(teachers)):
                return
            filename = self.exporter.export_teacher_report(teachers[idx].id, self.analytics)
            if filename:
                print(f"✅ Отчёт сохранён: {filename}")
        elif choice == "3":
            courses = self.storage.get_all_courses()
            if not courses:
                print("❌ Нет курсов")
                return
            print("\nКурсы:")
            for i, c in enumerate(courses, 1):
                print(f"  {i}. {c.name}")
            c = input("Выберите курс (номер): ").strip()
            if not c.isdigit():
                return
            idx = int(c) - 1
            if not (0 <= idx < len(courses)):
                return
            filename = self.exporter.export_course_report(courses[idx].id, self.analytics)
            if filename:
                print(f"✅ Отчёт сохранён: {filename}")
        else:
            print("❌ Неверный выбор!")
    
    def run(self):
        print("\n🏫 ДОБРО ПОЖАЛОВАТЬ В СИСТЕМУ УПРАВЛЕНИЯ ШКОЛОЙ v2.0")
        print(f"📊 Загружено: {len(self.storage.students)} студентов, "
              f"{len(self.storage.teachers)} преподавателей, "
              f"{len(self.storage.courses)} курсов")
        while True:
            self.show_menu()
            choice = input("Выберите действие: ").strip()
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.add_teacher()
            elif choice == "3":
                self.add_course()
            elif choice == "4":
                self.list_courses()
            elif choice == "5":
                self.enroll_student()
            elif choice == "6":
                self.assign_teacher_to_course()
            elif choice == "7":
                self.add_grade()
            elif choice == "8":
                self.complete_course()
            elif choice == "9":
                self.student_report()
            elif choice == "10":
                self.top_students()
            elif choice == "11":
                self.course_statistics()
            elif choice == "12":
                self.teacher_report()
            elif choice == "13":
                self.manage_modules()
            elif choice == "14":
                self.storage.save_all()
                print("✅ Данные сохранены. До свидания!")
                break
            elif choice == "15":
                self.visualize_student()
            elif choice == "16":
                self.export_csv()
            elif choice == "0":
                print("⚠️ Выход без сохранения!")
                break
            else:
                print("❌ Неверный выбор!")
            input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    try:
        cli = SchoolCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Принудительное завершение...")
        sys.exit(0)
