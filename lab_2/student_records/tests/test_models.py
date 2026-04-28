import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.student import Student
from models.student_model import StudentModel


class TestStudent(unittest.TestCase):
    """Тесты для класса Student"""

    def test_student_creation_valid(self):
        """Тест создания студента с валидными данными"""
        student = Student(
            full_name="Иванов Иван Иванович",
            course=3,
            group="ИС-31",
            total_works=15,
            completed_works=12,
            programming_language="Python"
        )

        self.assertEqual(student.full_name, "Иванов Иван Иванович")
        self.assertEqual(student.course, 3)
        self.assertEqual(student.group, "ИС-31")
        self.assertEqual(student.total_works, 15)
        self.assertEqual(student.completed_works, 12)
        self.assertEqual(student.programming_language, "Python")
        self.assertEqual(student.incomplete_works, 3)

    def test_student_creation_invalid_name(self):
        """Тест создания студента с некорректным ФИО"""
        with self.assertRaises(ValueError):
            Student(
                full_name="AB",  # слишком короткое
                course=3,
                group="ИС-31",
                total_works=15,
                completed_works=12,
                programming_language="Python"
            )

    def test_student_creation_invalid_course(self):
        """Тест создания студента с некорректным курсом"""
        with self.assertRaises(ValueError):
            Student(
                full_name="Иванов Иван Иванович",
                course=7,  # курс > 6
                group="ИС-31",
                total_works=15,
                completed_works=12,
                programming_language="Python"
            )

        with self.assertRaises(ValueError):
            Student(
                full_name="Иванов Иван Иванович",
                course=0,  # курс < 1
                group="ИС-31",
                total_works=15,
                completed_works=12,
                programming_language="Python"
            )

    def test_student_creation_invalid_works(self):
        """Тест создания студента с некорректным количеством работ"""
        with self.assertRaises(ValueError):
            Student(
                full_name="Иванов Иван Иванович",
                course=3,
                group="ИС-31",
                total_works=10,
                completed_works=15,  # выполнено больше, чем всего
                programming_language="Python"
            )

    def test_student_to_dict(self):
        """Тест преобразования студента в словарь"""
        student = Student(
            full_name="Иванов Иван Иванович",
            course=3,
            group="ИС-31",
            total_works=15,
            completed_works=12,
            programming_language="Python"
        )

        data = student.to_dict()
        self.assertEqual(data['full_name'], "Иванов Иван Иванович")
        self.assertEqual(data['course'], "3")
        self.assertEqual(data['group'], "ИС-31")
        self.assertEqual(data['total_works'], "15")
        self.assertEqual(data['completed_works'], "12")
        self.assertEqual(data['programming_language'], "Python")

    def test_student_from_dict(self):
        """Тест создания студента из словаря"""
        data = {
            'full_name': "Петров Петр Петрович",
            'course': "2",
            'group': "ИС-22",
            'total_works': "12",
            'completed_works': "10",
            'programming_language': "Java"
        }

        student = Student.from_dict(data)
        self.assertEqual(student.full_name, "Петров Петр Петрович")
        self.assertEqual(student.course, 2)
        self.assertEqual(student.group, "ИС-22")
        self.assertEqual(student.total_works, 12)
        self.assertEqual(student.completed_works, 10)
        self.assertEqual(student.programming_language, "Java")


class TestStudentModel(unittest.TestCase):
    """Тесты для класса StudentModel"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.model = StudentModel()
        self.student1 = Student(
            full_name="Иванов Иван Иванович",
            course=3,
            group="ИС-31",
            total_works=15,
            completed_works=12,
            programming_language="Python"
        )
        self.student2 = Student(
            full_name="Петров Петр Петрович",
            course=2,
            group="ИС-22",
            total_works=12,
            completed_works=10,
            programming_language="Java"
        )

    def test_add_student(self):
        """Тест добавления студента"""
        result = self.model.add_student(self.student1)
        self.assertTrue(result)
        self.assertEqual(self.model.get_student_count(), 1)

        students = self.model.get_all_students()
        self.assertEqual(students[0].full_name, "Иванов Иван Иванович")

    def test_add_students(self):
        """Тест добавления нескольких студентов"""
        students = [self.student1, self.student2]
        added = self.model.add_students(students)
        self.assertEqual(added, 2)
        self.assertEqual(self.model.get_student_count(), 2)

    def test_search_by_full_name(self):
        """Тест поиска по ФИО"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        results = self.model.search(full_name="Иванов")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].full_name, "Иванов Иван Иванович")

    def test_search_by_group(self):
        """Тест поиска по группе"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        results = self.model.search(group="ИС-22")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].group, "ИС-22")

    def test_search_by_course(self):
        """Тест поиска по курсу"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        results = self.model.search(course=3)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].course, 3)

    def test_search_by_programming_language(self):
        """Тест поиска по языку программирования"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        results = self.model.search(programming_language="Python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].programming_language, "Python")

    def test_search_by_completed_works(self):
        """Тест поиска по количеству выполненных работ"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        results = self.model.search(completed_works=12)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].completed_works, 12)

    def test_search_by_incomplete_works(self):
        """Тест поиска по количеству невыполненных работ"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        results = self.model.search(incomplete_works=2)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].incomplete_works, 2)

    def test_delete_by_criteria(self):
        """Тест удаления по критериям"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        deleted = self.model.delete(group="ИС-31")
        self.assertEqual(deleted, 1)
        self.assertEqual(self.model.get_student_count(), 1)

        remaining = self.model.get_all_students()
        self.assertEqual(remaining[0].full_name, "Петров Петр Петрович")

    def test_delete_multiple(self):
        """Тест удаления нескольких записей"""
        student3 = Student(
            full_name="Сидоров Сидор Сидорович",
            course=3,
            group="ИС-31",
            total_works=15,
            completed_works=14,
            programming_language="Python"
        )

        self.model.add_student(self.student1)
        self.model.add_student(self.student2)
        self.model.add_student(student3)

        deleted = self.model.delete(programming_language="Python")
        self.assertEqual(deleted, 2)
        self.assertEqual(self.model.get_student_count(), 1)

    def test_get_unique_values(self):
        """Тест получения уникальных значений"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)

        languages = self.model.get_unique_values('programming_language')
        self.assertEqual(len(languages), 2)
        self.assertIn("Python", languages)
        self.assertIn("Java", languages)

        courses = self.model.get_unique_values('course')
        self.assertEqual(len(courses), 2)
        self.assertIn("3", courses)
        self.assertIn("2", courses)

    def test_clear(self):
        """Тест очистки модели"""
        self.model.add_student(self.student1)
        self.model.add_student(self.student2)
        self.assertEqual(self.model.get_student_count(), 2)

        self.model.clear()
        self.assertEqual(self.model.get_student_count(), 0)


if __name__ == '__main__':
    unittest.main()