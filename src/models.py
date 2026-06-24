"""
models.py - Модели данных (Студент, Преподаватель, Курс, Модуль, Урок, ДЗ)
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional, Any


class Lesson:
    """Модель урока"""
    
    def __init__(self, title: str, description: str = "", lesson_id: Optional[str] = None):
        self.id = lesson_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.homework: Optional['Homework'] = None
        self.created_at = datetime.now().isoformat()
    
    def add_homework(self, title: str, description: str, max_score: int = 100):
        """Добавить домашнее задание к уроку"""
        self.homework = Homework(title, description, max_score)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'homework': self.homework.to_dict() if self.homework else None,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Lesson':
        lesson = cls(
            title=data['title'],
            description=data.get('description', ''),
            lesson_id=data.get('id')
        )
        if data.get('homework'):
            lesson.homework = Homework.from_dict(data['homework'])
        lesson.created_at = data.get('created_at', datetime.now().isoformat())
        return lesson
    
    def __str__(self) -> str:
        return f"📖 {self.title}"


class Module:
    """Модель модуля курса"""
    
    def __init__(self, title: str, description: str = "", module_id: Optional[str] = None):
        self.id = module_id or str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.lessons: List[Lesson] = []
        self.created_at = datetime.now().isoformat()
    
    def add_lesson(self, title: str, description: str = "") -> Lesson:
        """Добавить урок в модуль"""
        lesson = Lesson(title, description)
        self.lessons.append(lesson)
        return lesson
    
    def get_lesson(self, lesson_id: str) -> Optional[Lesson]:
        for lesson in self.lessons:
            if lesson.id == lesson_id:
                return lesson
        return None
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'lessons': [lesson.to_dict() for lesson in self.lessons],
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Module':
        module = cls(
            title=data['title'],
            description=data.get('description', ''),
            module_id=data.get('id')
        )
        for lesson_data in data.get('lessons', []):
            module.lessons.append(Lesson.from_dict(lesson_data))
        module.created_at = data.get('created_at', datetime.now().isoformat())
        return module
    
    def __str__(self) -> str:
        return f"📚 {self.title} ({len(self.lessons)} уроков)"


class Homework:
    """Модель домашнего задания"""
    
    def __init__(self, title: str, description: str, max_score: int = 100):
        self.id = str(uuid.uuid4())[:8]
        self.title = title
        self.description = description
        self.max_score = max_score
        self.submissions: Dict[str, int] = {}  # {student_id: score}
        self.created_at = datetime.now().isoformat()
    
    def submit_grade(self, student_id: str, score: int):
        """Выставить оценку за ДЗ"""
        if 0 <= score <= self.max_score:
            self.submissions[student_id] = score
    
    def get_student_score(self, student_id: str) -> Optional[int]:
        return self.submissions.get(student_id)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'max_score': self.max_score,
            'submissions': self.submissions,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Homework':
        homework = cls(
            title=data['title'],
            description=data.get('description', ''),
            max_score=data.get('max_score', 100)
        )
        homework.id = data.get('id', homework.id)
        homework.submissions = data.get('submissions', {})
        homework.created_at = data.get('created_at', datetime.now().isoformat())
        return homework


class Course:
    """Модель курса (обновлена)"""
    
    STATUS_ACTIVE = "активен"
    STATUS_COMPLETED = "завершён"
    
    def __init__(
        self,
        name: str,
        topic: str,
        course_id: Optional[str] = None,
        teacher_id: Optional[str] = None,
        status: str = STATUS_ACTIVE
    ):
        self.id = course_id or str(uuid.uuid4())[:8]
        self.name = name
        self.topic = topic
        self.teacher_id = teacher_id
        self.status = status
        self.students: List[str] = []  # ID студентов
        self.grades: Dict[str, List[int]] = {}  # {student_id: [grades]}
        self.modules: List[Module] = []  # Модули курса
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def add_module(self, title: str, description: str = "") -> Module:
        """Добавить модуль в курс"""
        module = Module(title, description)
        self.modules.append(module)
        return module
    
    def get_module(self, module_id: str) -> Optional[Module]:
        for module in self.modules:
            if module.id == module_id:
                return module
        return None
    
    def get_all_lessons(self) -> List[Lesson]:
        """Получить все уроки курса"""
        lessons = []
        for module in self.modules:
            lessons.extend(module.lessons)
        return lessons
    
    def get_total_lessons(self) -> int:
        return len(self.get_all_lessons())
    
    def add_student(self, student_id: str):
        if student_id not in self.students:
            self.students.append(student_id)
    
    def remove_student(self, student_id: str):
        if student_id in self.students:
            self.students.remove(student_id)
    
    def assign_teacher(self, teacher_id: str):
        self.teacher_id = teacher_id
    
    def add_grade(self, student_id: str, grade: int):
        if student_id not in self.grades:
            self.grades[student_id] = []
        self.grades[student_id].append(grade)
    
    def complete(self):
        self.status = self.STATUS_COMPLETED
        self.completed_at = datetime.now().isoformat()
    
    def get_average_grade(self) -> float:
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0.0
    
    def get_student_grades(self, student_id: str) -> List[int]:
        return self.grades.get(student_id, [])
    
    def get_student_homework_scores(self, student_id: str) -> List[int]:
        """Получить все оценки за ДЗ студента по курсу"""
        scores = []
        for lesson in self.get_all_lessons():
            if lesson.homework:
                score = lesson.homework.get_student_score(student_id)
                if score is not None:
                    scores.append(score)
        return scores
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'topic': self.topic,
            'teacher_id': self.teacher_id,
            'status': self.status,
            'students': self.students,
            'grades': self.grades,
            'modules': [m.to_dict() for m in self.modules],
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Course':
        course = cls(
            name=data['name'],
            topic=data['topic'],
            course_id=data.get('id'),
            teacher_id=data.get('teacher_id'),
            status=data.get('status', cls.STATUS_ACTIVE)
        )
        course.students = data.get('students', [])
        course.grades = data.get('grades', {})
        for module_data in data.get('modules', []):
            course.modules.append(Module.from_dict(module_data))
        course.created_at = data.get('created_at', datetime.now().isoformat())
        course.completed_at = data.get('completed_at')
        return course
    
    def __str__(self) -> str:
        status_icon = "🟢" if self.status == self.STATUS_ACTIVE else "🔴"
        return f"{status_icon} {self.name} ({self.topic}) - {self.get_total_lessons()} уроков"


# Сохраняем старые модели (Student, Teacher) без изменений
class Student:
    """Модель студента (без изменений)"""
    
    def __init__(self, name: str, email: str, student_id: Optional[str] = None):
        self.id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.courses: List[str] = []
        self.grades: Dict[str, List[int]] = {}
        self.completed_courses: List[str] = []
        self.created_at = datetime.now().isoformat()
    
    def enroll(self, course_id: str):
        if course_id not in self.courses:
            self.courses.append(course_id)
    
    def add_grade(self, course_id: str, grade: int):
        if course_id not in self.grades:
            self.grades[course_id] = []
        self.grades[course_id].append(grade)
    
    def complete_course(self, course_id: str):
        if course_id in self.courses:
            self.courses.remove(course_id)
        if course_id not in self.completed_courses:
            self.completed_courses.append(course_id)
    
    def get_average_grade(self, course_id: Optional[str] = None) -> float:
        if course_id:
            grades = self.grades.get(course_id, [])
            return sum(grades) / len(grades) if grades else 0.0
        all_grades = []
        for grades in self.grades.values():
            all_grades.extend(grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0.0
    
    def get_course_homework_scores(self, course_id: str) -> List[int]:
        """Получить оценки за ДЗ по конкретному курсу"""
        # Этот метод будет использоваться через Course
        return []
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'courses': self.courses,
            'grades': self.grades,
            'completed_courses': self.completed_courses,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        student = cls(
            name=data['name'],
            email=data['email'],
            student_id=data.get('id')
        )
        student.courses = data.get('courses', [])
        student.grades = data.get('grades', {})
        student.completed_courses = data.get('completed_courses', [])
        student.created_at = data.get('created_at', datetime.now().isoformat())
        return student
    
    def __str__(self) -> str:
        return f"{self.name} ({self.email})"


class Teacher:
    """Модель преподавателя (без изменений)"""
    
    def __init__(self, name: str, specialization: str, teacher_id: Optional[str] = None):
        self.id = teacher_id or str(uuid.uuid4())[:8]
        self.name = name
        self.specialization = specialization
        self.courses: List[str] = []
        self.created_at = datetime.now().isoformat()
    
    def assign_course(self, course_id: str):
        if course_id not in self.courses:
            self.courses.append(course_id)
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'courses': self.courses,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Teacher':
        teacher = cls(
            name=data['name'],
            specialization=data['specialization'],
            teacher_id=data.get('id')
        )
        teacher.courses = data.get('courses', [])
        teacher.created_at = data.get('created_at', datetime.now().isoformat())
        return teacher
    
    def __str__(self) -> str:
        return f"{self.name} ({self.specialization})"
