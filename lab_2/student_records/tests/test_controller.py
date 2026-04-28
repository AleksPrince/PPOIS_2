import unittest
import sys
import os
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.student_controller import StudentController
from models.student import Student


class TestStudentController(unittest.TestCase):
    """Тесты для класса StudentController"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.controller = StudentController()

        self.student_data1 = {
            'full_name': "Иванов Иван Иванович",
            'course': 3,
            'group': "ИС-31",
            'total_works': 15,
            'completed_works': 12,
            'programming_language': "Python"
        }

        self.student_data2 = {
            'full_name': "Петров Петр Петрович",
            'course': 2,
            'group': "ИС-22",
            'total_works': 12,
            'completed_works': 10,
            'programming_language': "Java"
        }

    def test_add_student(self):
        """Тест добавления студента через контроллер"""
        result = self.controller.add_student(self.student_data1)
        self.assertTrue(result)

        students = self.controller.get_all_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].full_name, "Иванов Иван Иванович")

    def test_add_student_invalid_data(self):
        """Тест добавления студента с некорректными данными"""
        invalid_data = self.student_data1.copy()
        invalid_data['course'] = 7  # некорректный курс

        result = self.controller.add_student(invalid_data)
        self.assertFalse(result)

        students = self.controller.get_all_students()
        self.assertEqual(len(students), 0)

    def test_add_multiple_students(self):
        """Тест добавления нескольких студентов"""
        students_data = [self.student_data1, self.student_data2]
        added = self.controller.add_multiple_students(students_data)
        self.assertEqual(added, 2)

        students = self.controller.get_all_students()
        self.assertEqual(len(students), 2)

    def test_search_students(self):
        """Тест поиска студентов через контроллер"""
        self.controller.add_student(self.student_data1)
        self.controller.add_student(self.student_data2)

        results = self.controller.search_students({'group': 'ИС-31'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].full_name, "Иванов Иван Иванович")

        results = self.controller.search_students({'programming_language': 'Java'})
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].full_name, "Петров Петр Петрович")

    def test_delete_students(self):
        """Тест удаления студентов через контроллер"""
        self.controller.add_student(self.student_data1)
        self.controller.add_student(self.student_data2)

        deleted = self.controller.delete_students({'course': 3})
        self.assertEqual(deleted, 1)

        students = self.controller.get_all_students()
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0].full_name, "Петров Петр Петрович")

    def test_save_and_load(self):
        """Тест сохранения и загрузки данных"""
        self.controller.add_student(self.student_data1)
        self.controller.add_student(self.student_data2)

        # Сохраняем во временный файл
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Сохраняем
            save_result = self.controller.save_to_file(tmp_path)
            self.assertTrue(save_result)

            # Создаем новый контроллер и загружаем
            new_controller = StudentController()
            load_result, message = new_controller.load_from_file(tmp_path)

            self.assertTrue(load_result)
            self.assertEqual(new_controller.get_all_students(), 2)

        finally:
            # Удаляем временный файл
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_get_unique_values(self):
        """Тест получения уникальных значений через контроллер"""
        self.controller.add_student(self.student_data1)
        self.controller.add_student(self.student_data2)

        languages = self.controller.get_unique_values('programming_language')
        self.assertEqual(len(languages), 2)
        self.assertIn("Python", languages)
        self.assertIn("Java", languages)

    def test_observer_notification(self):
        """Тест уведомления наблюдателей"""
        self.notification_count = 0

        def observer():
            self.notification_count += 1

        self.controller.add_observer(observer)

        self.controller.add_student(self.student_data1)
        self.assertEqual(self.notification_count, 1)

        self.controller.delete_students({'course': 3})
        self.assertEqual(self.notification_count, 2)

        self.controller.model.clear()
        self.assertEqual(self.notification_count, 3)


if __name__ == '__main__':
    unittest.main()