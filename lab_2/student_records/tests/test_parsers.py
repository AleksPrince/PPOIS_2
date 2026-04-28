import unittest
import sys
import os
import tempfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.student import Student
from parsers.xml_writer import XMLWriter
from parsers.xml_reader import XMLReader


class TestXMLWriter(unittest.TestCase):
    """Тесты для класса XMLWriter (DOM парсер)"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.students = [
            Student(
                full_name="Иванов Иван Иванович",
                course=3,
                group="ИС-31",
                total_works=15,
                completed_works=12,
                programming_language="Python"
            ),
            Student(
                full_name="Петров Петр Петрович",
                course=2,
                group="ИС-22",
                total_works=12,
                completed_works=10,
                programming_language="Java"
            )
        ]

    def test_write_valid_data(self):
        """Тест записи валидных данных в XML"""
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Записываем данные
            result = XMLWriter.write(self.students, tmp_path)
            self.assertTrue(result)

            # Проверяем, что файл создан и содержит данные
            self.assertTrue(os.path.exists(tmp_path))
            self.assertGreater(os.path.getsize(tmp_path), 0)

            # Проверяем структуру XML
            tree = ET.parse(tmp_path)
            root = tree.getroot()

            self.assertEqual(root.tag, 'students')
            self.assertEqual(len(root.findall('student')), 2)

            # Проверяем первого студента
            first_student = root.findall('student')[0]
            self.assertEqual(first_student.find('full_name').text, "Иванов Иван Иванович")
            self.assertEqual(first_student.find('course').text, "3")
            self.assertEqual(first_student.find('group').text, "ИС-31")
            self.assertEqual(first_student.find('total_works').text, "15")
            self.assertEqual(first_student.find('completed_works').text, "12")
            self.assertEqual(first_student.find('programming_language').text, "Python")

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_write_empty_list(self):
        """Тест записи пустого списка"""
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name

        try:
            result = XMLWriter.write([], tmp_path)
            self.assertTrue(result)

            tree = ET.parse(tmp_path)
            root = tree.getroot()

            self.assertEqual(root.tag, 'students')
            self.assertEqual(len(root.findall('student')), 0)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_write_invalid_path(self):
        """Тест записи в несуществующий путь"""
        result = XMLWriter.write(self.students, "/non/existent/path/file.xml")
        self.assertFalse(result)


class TestXMLReader(unittest.TestCase):
    """Тесты для класса XMLReader (SAX парсер)"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.students = [
            Student(
                full_name="Иванов Иван Иванович",
                course=3,
                group="ИС-31",
                total_works=15,
                completed_works=12,
                programming_language="Python"
            ),
            Student(
                full_name="Петров Петр Петрович",
                course=2,
                group="ИС-22",
                total_works=12,
                completed_works=10,
                programming_language="Java"
            )
        ]

        # Создаем временный XML файл с данными
        self.tmp_file = tempfile.NamedTemporaryFile(suffix='.xml', delete=False)
        self.tmp_path = self.tmp_file.name
        self.tmp_file.close()

        # Записываем данные
        XMLWriter.write(self.students, self.tmp_path)

    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.tmp_path):
            os.unlink(self.tmp_path)

    def test_read_valid_data(self):
        """Тест чтения валидных данных из XML"""
        students, error = XMLReader.read(self.tmp_path)

        self.assertIsNone(error)
        self.assertEqual(len(students), 2)

        # Проверяем первого студента
        self.assertEqual(students[0].full_name, "Иванов Иван Иванович")
        self.assertEqual(students[0].course, 3)
        self.assertEqual(students[0].group, "ИС-31")
        self.assertEqual(students[0].total_works, 15)
        self.assertEqual(students[0].completed_works, 12)
        self.assertEqual(students[0].programming_language, "Python")

        # Проверяем второго студента
        self.assertEqual(students[1].full_name, "Петров Петр Петрович")
        self.assertEqual(students[1].course, 2)
        self.assertEqual(students[1].group, "ИС-22")
        self.assertEqual(students[1].total_works, 12)
        self.assertEqual(students[1].completed_works, 10)
        self.assertEqual(students[1].programming_language, "Java")

    def test_read_nonexistent_file(self):
        """Тест чтения несуществующего файла"""
        students, error = XMLReader.read("/non/existent/file.xml")

        self.assertEqual(len(students), 0)
        self.assertIsNotNone(error)
        self.assertIn("Ошибка при чтении XML", error)

    def test_read_invalid_xml(self):
        """Тест чтения некорректного XML файла"""
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp.write(b"<invalid>xml</invalid>")
            tmp_path = tmp.name

        try:
            students, error = XMLReader.read(tmp_path)

            # Должна быть ошибка, так как структура не соответствует ожидаемой
            self.assertIsNotNone(error)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_read_empty_xml(self):
        """Тест чтения пустого XML файла"""
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp.write(b"<students></students>")
            tmp_path = tmp.name

        try:
            students, error = XMLReader.read(tmp_path)

            self.assertIsNone(error)
            self.assertEqual(len(students), 0)

        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()