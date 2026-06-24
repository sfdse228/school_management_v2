"""
export.py - Экспорт данных в CSV
"""

import csv
import os
from typing import Dict, List
from src.storage import SchoolStorage


class CSVExporter:
    """Класс для экспорта данных в CSV"""
    
    def __init__(self, storage: SchoolStorage):
        self.storage = storage
        self.export_dir = "exports"
        self._ensure_export_dir()
    
    def _ensure_export_dir(self):
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_student_report(self, student_id: str) -> str:
        """Экспорт отчёта по студенту в CSV"""
        report = self.storage.get_student_report(student_id)
        if not report:
            return None
        
        filename = f"{self.export_dir}/student_{report['student']}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Заголовок
            writer.writerow(['ОТЧЁТ ПО СТУДЕНТУ'])
            writer.writerow(['Имя:', report['student']])
            writer.writerow(['Email:', report['email']])
            writer.writerow(['Средняя оценка:', report['average_grade']])
            writer.writerow(['Всего курсов:', report['total_courses']])
            writer.writerow([])
            
            # Активные курсы
            writer.writerow(['АКТИВНЫЕ КУРСЫ'])
            writer.writerow(['Название', 'Преподаватель'])
            for course in report['active_courses']:
                writer.writerow([course['name'], course['teacher']])
            writer.writerow([])
            
            # Завершённые курсы
            writer.writerow(['ЗАВЕРШЁННЫЕ КУРСЫ'])
            writer.writerow(['Название', 'Оценки', 'Средняя', 'Оценки за ДЗ'])
            for course in report['completed_courses']:
                writer.writerow([
                    course['name'],
                    ', '.join(map(str, course['grades'])),
                    course['average'],
                    ', '.join(map(str, course.get('homework_scores', [])))
                ])
        
        return filename
    
    def export_teacher_report(self, teacher_id: str, analytics) -> str:
        """Экспорт отчёта по преподавателю в CSV"""
        stats = analytics.get_teacher_statistics(teacher_id)
        if not stats:
            return None
        
        filename = f"{self.export_dir}/teacher_{stats['teacher_name']}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow(['ОТЧЁТ ПО ПРЕПОДАВАТЕЛЮ'])
            writer.writerow(['Имя:', stats['teacher_name']])
            writer.writerow(['Специализация:', stats['specialization']])
            writer.writerow(['Всего курсов:', stats['total_courses']])
            writer.writerow(['Активных курсов:', stats['active_courses_count']])
            writer.writerow(['Завершённых курсов:', stats['completed_courses_count']])
            writer.writerow(['Средняя успеваемость студентов:', stats['average_student_grade']])
            writer.writerow([])
            
            writer.writerow(['АКТИВНЫЕ КУРСЫ'])
            writer.writerow(['Название', 'Студентов'])
            for course in stats['active_courses']:
                writer.writerow([course['name'], course['students']])
            writer.writerow([])
            
            writer.writerow(['ЗАВЕРШЁННЫЕ КУРСЫ'])
            writer.writerow(['Название', 'Дата завершения', 'Студентов', 'Средняя оценка'])
            for course in stats['completed_courses']:
                writer.writerow([
                    course['name'],
                    course['completed_at'],
                    course['students_count'],
                    round(course['average_grade'], 2)
                ])
        
        return filename
    
    def export_course_report(self, course_id: str, analytics) -> str:
        """Экспорт отчёта по курсу в CSV"""
        stats = analytics.get_course_statistics(course_id)
        if not stats:
            return None
        
        filename = f"{self.export_dir}/course_{stats['course_name']}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            writer.writerow(['ОТЧЁТ ПО КУРСУ'])
            writer.writerow(['Название:', stats['course_name']])
            writer.writerow(['Тема:', stats['topic']])
            writer.writerow(['Статус:', stats['status']])
            writer.writerow(['Преподаватель:', stats['teacher']])
            writer.writerow(['Студентов:', stats['students_count']])
            writer.writerow(['Модулей:', stats['modules_count']])
            writer.writerow(['Уроков:', stats['lessons_count']])
            writer.writerow(['Средняя оценка:', round(stats['average_grade'], 2)])
            writer.writerow(['Максимальная:', stats['max_grade']])
            writer.writerow(['Минимальная:', stats['min_grade']])
            writer.writerow(['Средняя за ДЗ:', round(stats['homework_avg'], 2)])
        
        return filename
