import os
import pickle
from typing import List, Optional, Callable
from .student import Student


class StudentModel:
    """Модель для хранения списка студентов"""

    def __init__(self):
        self.students: List[Student] = []
        self.observers: List[Callable] = []
        self.current_file: Optional[str] = None

    def add_observer(self, observer: Callable):
        """Добавление наблюдателя за изменениями"""
        self.observers.append(observer)

    def notify_observers(self):
        """Уведомление наблюдателей об изменениях"""
        for observer in self.observers:
            observer()

    def add_student(self, student: Student) -> bool:
        """Добавление студента"""
        try:
            self.students.append(student)
            self.notify_observers()
            return True
        except Exception:
            return False

    def add_students(self, students: List[Student]) -> int:
        """Добавление нескольких студентов"""
        added = 0
        for student in students:
            if self.add_student(student):
                added += 1
        return added

    def get_all_students(self) -> List[Student]:
        """Получение всех студентов"""
        return self.students.copy()

    def get_student_count(self) -> int:
        """Получение количества студентов"""
        return len(self.students)

    def search(self, **criteria) -> List[Student]:
        """
        Поиск студентов по критериям
        Поддерживаемые критерии: full_name, group, course, programming_language,
                               total_works, completed_works, incomplete_works
        """
        results = self.students.copy()

        for key, value in criteria.items():
            if value is None or value == '':
                continue

            if key == 'full_name':
                results = [s for s in results if value.lower() in s.full_name.lower()]
            elif key == 'group':
                results = [s for s in results if value.lower() in s.group.lower()]
            elif key == 'course':
                try:
                    course_val = int(value)
                    results = [s for s in results if s.course == course_val]
                except ValueError:
                    pass
            elif key == 'programming_language':
                results = [s for s in results if value.lower() in s.programming_language.lower()]
            elif key == 'total_works':
                try:
                    total_val = int(value)
                    results = [s for s in results if s.total_works == total_val]
                except ValueError:
                    pass
            elif key == 'completed_works':
                try:
                    completed_val = int(value)
                    results = [s for s in results if s.completed_works == completed_val]
                except ValueError:
                    pass
            elif key == 'incomplete_works':
                try:
                    incomplete_val = int(value)
                    results = [s for s in results if s.incomplete_works == incomplete_val]
                except ValueError:
                    pass
            elif key == 'min_total_works':
                try:
                    min_val = int(value)
                    results = [s for s in results if s.total_works >= min_val]
                except ValueError:
                    pass
            elif key == 'max_total_works':
                try:
                    max_val = int(value)
                    results = [s for s in results if s.total_works <= max_val]
                except ValueError:
                    pass
            elif key == 'min_completed_works':
                try:
                    min_val = int(value)
                    results = [s for s in results if s.completed_works >= min_val]
                except ValueError:
                    pass
            elif key == 'max_completed_works':
                try:
                    max_val = int(value)
                    results = [s for s in results if s.completed_works <= max_val]
                except ValueError:
                    pass
            elif key == 'min_incomplete_works':
                try:
                    min_val = int(value)
                    results = [s for s in results if s.incomplete_works >= min_val]
                except ValueError:
                    pass
            elif key == 'max_incomplete_works':
                try:
                    max_val = int(value)
                    results = [s for s in results if s.incomplete_works <= max_val]
                except ValueError:
                    pass

        return results

    def delete(self, **criteria) -> int:
        """
        Удаление студентов по критериям
        Возвращает количество удаленных записей
        """
        to_delete = self.search(**criteria)
        deleted_count = len(to_delete)

        # Удаляем найденных студентов
        self.students = [s for s in self.students if s not in to_delete]

        if deleted_count > 0:
            self.notify_observers()

        return deleted_count

    def get_unique_values(self, field: str) -> List[str]:
        """Получение уникальных значений для поля"""
        values = set()
        for student in self.students:
            if field == 'programming_language':
                values.add(student.programming_language)
            elif field == 'course':
                values.add(str(student.course))
            elif field == 'total_works':
                values.add(str(student.total_works))
            elif field == 'completed_works':
                values.add(str(student.completed_works))

        return sorted(list(values))

    def clear(self):
        """Очистка модели"""
        self.students.clear()
        self.current_file = None
        self.notify_observers()