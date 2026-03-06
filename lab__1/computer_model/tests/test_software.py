import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from software.program import Program
from software.task import Task, ComputerStatus
from hardware.cpu import CPU
from hardware.ram import RAM
from hardware.gpu import GPU
from hardware.storage import Storage
from exceptions import ResourceNotFoundError


class TestProgram(unittest.TestCase):
    """Тесты класса Program"""

    def test_program_creation(self):
        """Тест создания программы"""
        prog = Program("Test", 8, 4, 2, 10)
        self.assertEqual(prog.name, "Test")
        self.assertEqual(prog.ram_required, 8)
        self.assertEqual(prog.cpu_cores_required, 4)
        self.assertEqual(prog.vram_required, 2)
        self.assertEqual(prog.storage_required, 10)

    def test_program_with_defaults(self):
        """Тест программы со значениями по умолчанию"""
        prog = Program("Simple", 4, 2)
        self.assertEqual(prog.name, "Simple")
        self.assertEqual(prog.ram_required, 4)
        self.assertEqual(prog.cpu_cores_required, 2)
        self.assertEqual(prog.vram_required, 0)
        self.assertEqual(prog.storage_required, 0)

    def test_program_str(self):
        """Тест строкового представления"""
        prog = Program("Game", 16, 8, 8, 50)
        self.assertIn("Game", str(prog))
        self.assertIn("16ГБ", str(prog))
        self.assertIn("8 ядер", str(prog))


class TestTask(unittest.TestCase):
    """Тесты класса Task"""

    def setUp(self):
        self.program = Program("Test", 8, 4, 2, 10)
        self.task = Task(self.program)
        self.cpu = CPU("Ryzen", "AMD", "AM4", 6, 65)
        self.ram = RAM("DDR4", "Corsair", 5, 16, "DDR4", 3200)
        self.gpu = GPU("RTX", "NVIDIA", 170, 8, 1800, "PCIe")
        self.storage = Storage("SSD", "Samsung", 5, 500, "SSD", "NVMe")

    def test_task_creation(self):
        """Тест создания задачи"""
        self.assertEqual(self.task.program, self.program)
        self.assertEqual(self.task.status, ComputerStatus.OFF)
        self.assertIsNone(self.task.cpu)
        self.assertEqual(len(self.task.ram_modules), 0)
        self.assertEqual(len(self.task.gpu_modules), 0)
        self.assertEqual(len(self.task.storage_modules), 0)
        self.assertIsNone(self.task.result)

    def test_task_invalid_creation(self):
        """Тест создания задачи с неверными данными"""
        with self.assertRaises(ResourceNotFoundError):
            Task("not a program")

    def test_task_add_resources(self):
        """Тест добавления ресурсов в задачу"""
        self.task.cpu = self.cpu
        self.task.add_ram(self.ram)
        self.task.add_gpu(self.gpu)
        self.task.add_storage(self.storage)

        self.assertEqual(self.task.cpu, self.cpu)
        self.assertEqual(len(self.task.ram_modules), 1)
        self.assertEqual(len(self.task.gpu_modules), 1)
        self.assertEqual(len(self.task.storage_modules), 1)

    def test_task_status(self):
        """Тест изменения статуса"""
        self.task.status = ComputerStatus.RUNNING
        self.assertEqual(self.task.status, ComputerStatus.RUNNING)

        self.task.status = ComputerStatus.ON
        self.assertEqual(self.task.status, ComputerStatus.ON)

    def test_task_result(self):
        """Тест установки результата"""
        self.task.result = "Success"
        self.assertEqual(self.task.result, "Success")

    def test_task_str(self):
        """Тест строкового представления"""
        self.task.cpu = self.cpu
        self.task.add_ram(self.ram)
        task_str = str(self.task)
        self.assertIn("Test", task_str)
        self.assertIn("ОФФ", task_str)  # OFF по-русски


if __name__ == '__main__':
    unittest.main()