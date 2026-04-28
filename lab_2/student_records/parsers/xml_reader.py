import xml.sax
from typing import List, Optional
from models.student import Student


class StudentHandler(xml.sax.ContentHandler):
    """Обработчик SAX парсера для чтения студентов из XML"""

    def __init__(self):
        self.students: List[Student] = []
        self.current_student_data = {}
        self.current_element = ""
        self.current_value = ""
        self.error: Optional[str] = None

    def startElement(self, name, attrs):
        self.current_element = name
        self.current_value = ""

        if name == "student":
            self.current_student_data = {}

    def endElement(self, name):
        if name == "student":
            try:
                student = Student.from_dict(self.current_student_data)
                self.students.append(student)
            except (ValueError, KeyError) as e:
                self.error = f"Ошибка при создании студента: {e}"

        elif name in ["full_name", "course", "group", "total_works",
                      "completed_works", "programming_language"]:
            self.current_student_data[name] = self.current_value.strip()

    def characters(self, content):
        self.current_value += content


class XMLReader:
    """Класс для чтения данных из XML с использованием SAX парсера"""

    @staticmethod
    def read(filepath: str) -> tuple[List[Student], Optional[str]]:
        """
        Чтение списка студентов из XML файла
        Возвращает кортеж (список студентов, сообщение об ошибке)
        """
        try:
            handler = StudentHandler()
            parser = xml.sax.make_parser()
            parser.setContentHandler(handler)
            parser.parse(filepath)

            return handler.students, handler.error

        except Exception as e:
            return [], f"Ошибка при чтении XML: {e}"