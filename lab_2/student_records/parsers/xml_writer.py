import xml.dom.minidom as minidom
from xml.dom import minidom
from typing import List
from models.student import Student


class XMLWriter:
    """Класс для записи данных в XML с использованием DOM парсера"""

    @staticmethod
    def write(students: List[Student], filepath: str) -> bool:
        """
        Запись списка студентов в XML файл
        Использует DOM парсер
        """
        try:
            # Создаем корневой элемент
            doc = minidom.Document()
            root = doc.createElement('students')
            doc.appendChild(root)

            for student in students:
                student_elem = doc.createElement('student')

                # Добавляем поля студента как элементы
                for field, value in student.to_dict().items():
                    field_elem = doc.createElement(field)
                    field_elem.appendChild(doc.createTextNode(str(value)))
                    student_elem.appendChild(field_elem)

                root.appendChild(student_elem)

            # Записываем в файл с отступами
            with open(filepath, 'w', encoding='utf-8') as f:
                doc.writexml(f, indent='  ', addindent='  ', newl='\n', encoding='utf-8')

            return True

        except Exception as e:
            print(f"Ошибка при записи XML: {e}")
            return False