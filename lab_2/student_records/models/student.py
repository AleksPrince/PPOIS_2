from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Student:
    """Модель студента"""
    full_name: str
    course: int
    group: str
    total_works: int
    completed_works: int
    programming_language: str

    def __post_init__(self):
        """Валидация данных"""
        if not self.full_name or len(self.full_name.strip()) < 3:
            raise ValueError("ФИО должно содержать минимум 3 символа")

        if not 1 <= self.course <= 6:
            raise ValueError("Курс должен быть от 1 до 6")

        if not self.group or len(self.group.strip()) < 2:
            raise ValueError("Группа должна содержать минимум 2 символа")

        if self.total_works < 0:
            raise ValueError("Общее число работ не может быть отрицательным")

        if self.completed_works < 0:
            raise ValueError("Количество выполненных работ не может быть отрицательным")

        if self.completed_works > self.total_works:
            raise ValueError("Выполненных работ не может быть больше общего числа")

        if not self.programming_language or len(self.programming_language.strip()) < 1:
            raise ValueError("Язык программирования должен быть указан")

    @property
    def incomplete_works(self) -> int:
        """Количество невыполненных работ"""
        return self.total_works - self.completed_works

    def to_dict(self) -> dict:
        """Преобразование в словарь для сохранения в XML"""
        return {
            'full_name': self.full_name,
            'course': str(self.course),
            'group': self.group,
            'total_works': str(self.total_works),
            'completed_works': str(self.completed_works),
            'programming_language': self.programming_language
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Student':
        """Создание студента из словаря"""
        return cls(
            full_name=data['full_name'],
            course=int(data['course']),
            group=data['group'],
            total_works=int(data['total_works']),
            completed_works=int(data['completed_works']),
            programming_language=data['programming_language']
        )