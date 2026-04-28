from typing import List, Optional, Callable
from models.student import Student
from models.student_model import StudentModel
from parsers.xml_writer import XMLWriter
from parsers.xml_reader import XMLReader


class StudentController:
    """Контроллер для управления студентами"""

    def __init__(self):
        self.model = StudentModel()

    def add_student(self, student_data: dict) -> bool:
        """Добавление нового студента"""
        try:
            student = Student(**student_data)
            return self.model.add_student(student)
        except (ValueError, TypeError) as e:
            print(f"Ошибка при добавлении студента: {e}")
            return False

    def add_multiple_students(self, students_data: List[dict]) -> int:
        """Добавление нескольких студентов"""
        students = []
        for data in students_data:
            try:
                students.append(Student(**data))
            except (ValueError, TypeError):
                continue

        return self.model.add_students(students)

    def get_all_students(self) -> List[Student]:
        """Получение всех студентов"""
        return self.model.get_all_students()

    def search_students(self, criteria: dict) -> List[Student]:
        """Поиск студентов по критериям"""
        return self.model.search(**criteria)

    def delete_students(self, criteria: dict) -> int:
        """Удаление студентов по критериям"""
        return self.model.delete(**criteria)

    def save_to_file(self, filepath: str) -> bool:
        """Сохранение данных в XML файл"""
        students = self.model.get_all_students()
        success = XMLWriter.write(students, filepath)
        if success:
            self.model.current_file = filepath
        return success

    def load_from_file(self, filepath: str) -> tuple[bool, str]:
        """Загрузка данных из XML файла"""
        students, error = XMLReader.read(filepath)

        if error:
            return False, error

        self.model.clear()
        added = self.model.add_students(students)
        self.model.current_file = filepath

        return True, f"Загружено {added} записей"

    def get_unique_values(self, field: str) -> List[str]:
        """Получение уникальных значений для поля"""
        return self.model.get_unique_values(field)

    def add_observer(self, observer: Callable):
        """Добавление наблюдателя за изменениями модели"""
        self.model.add_observer(observer)

    def get_current_file(self) -> Optional[str]:
        """Получение текущего файла"""
        return self.model.current_file