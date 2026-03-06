import unittest
import sys
import os

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hardware.cpu import CPU
from hardware.ram import RAM
from hardware.gpu import GPU
from hardware.storage import Storage
from hardware.motherboard import Motherboard
from hardware.powersupply import PowerSupply
from hardware.component import Component
from exceptions import InvalidDataError


class TestComponent(unittest.TestCase):
    """Тесты базового класса Component"""

    def test_component_creation(self):
        """Тест создания компонента"""
        component = Component("Test", "TestMan", 100)
        self.assertEqual(component.name, "Test")
        self.assertEqual(component.manufacturer, "TestMan")
        self.assertEqual(component.power_consumption, 100)
        self.assertFalse(component.is_busy)

    def test_component_name_setter(self):
        """Тест установки имени"""
        component = Component("Test", "TestMan", 100)
        component.name = "NewName"
        self.assertEqual(component.name, "NewName")

        with self.assertRaises(InvalidDataError):
            component.name = ""

    def test_component_manufacturer_setter(self):
        """Тест установки производителя"""
        component = Component("Test", "TestMan", 100)
        component.manufacturer = "NewMan"
        self.assertEqual(component.manufacturer, "NewMan")

        with self.assertRaises(InvalidDataError):
            component.manufacturer = ""

    def test_component_busy_status(self):
        """Тест статуса занятости"""
        component = Component("Test", "TestMan", 100)
        component.is_busy = True
        self.assertTrue(component.is_busy)

        with self.assertRaises(InvalidDataError):
            component.is_busy = "not boolean"


class TestCPU(unittest.TestCase):
    """Тесты класса CPU"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.cpu = CPU("Ryzen 5", "AMD", "AM4", 6, 65)

    def test_cpu_creation(self):
        """Тест создания процессора"""
        self.assertEqual(self.cpu.name, "Ryzen 5")
        self.assertEqual(self.cpu.manufacturer, "AMD")
        self.assertEqual(self.cpu.socket, "AM4")
        self.assertEqual(self.cpu.cores, 6)
        self.assertEqual(self.cpu.power_consumption, 65)
        self.assertEqual(self.cpu.frequency, 3.0)  # default

    def test_cpu_socket_setter(self):
        """Тест установки сокета"""
        self.cpu.socket = "LGA1200"
        self.assertEqual(self.cpu.socket, "LGA1200")

        with self.assertRaises(InvalidDataError):
            self.cpu.socket = ""

    def test_cpu_cores_setter(self):
        """Тест установки количества ядер"""
        self.cpu.cores = 8
        self.assertEqual(self.cpu.cores, 8)

        with self.assertRaises(InvalidDataError):
            self.cpu.cores = 0

        with self.assertRaises(InvalidDataError):
            self.cpu.cores = -5

    def test_cpu_frequency_setter(self):
        """Тест установки частоты"""
        self.cpu.frequency = 4.2
        self.assertEqual(self.cpu.frequency, 4.2)

        with self.assertRaises(InvalidDataError):
            self.cpu.frequency = 0

        with self.assertRaises(InvalidDataError):
            self.cpu.frequency = -1.5

    def test_cpu_str(self):
        """Тест строкового представления"""
        self.assertIn("Процессор:", str(self.cpu))
        self.assertIn("Ryzen 5", str(self.cpu))
        self.assertIn("AM4", str(self.cpu))
        self.assertIn("6 ядер", str(self.cpu))


class TestRAM(unittest.TestCase):
    """Тесты класса RAM"""

    def setUp(self):
        self.ram = RAM("DDR4", "Corsair", 5, 16, "DDR4", 3200)

    def test_ram_creation(self):
        self.assertEqual(self.ram.name, "DDR4")
        self.assertEqual(self.ram.manufacturer, "Corsair")
        self.assertEqual(self.ram.power_consumption, 5)
        self.assertEqual(self.ram.size, 16)
        self.assertEqual(self.ram.memory_type, "DDR4")
        self.assertEqual(self.ram.frequency, 3200)

    def test_ram_size_setter(self):
        self.ram.size = 32
        self.assertEqual(self.ram.size, 32)

        with self.assertRaises(InvalidDataError):
            self.ram.size = 0

    def test_ram_type_setter(self):
        self.ram.memory_type = "DDR5"
        self.assertEqual(self.ram.memory_type, "DDR5")

        with self.assertRaises(InvalidDataError):
            self.ram.memory_type = ""

    def test_ram_str(self):
        self.assertIn("ОЗУ:", str(self.ram))
        self.assertIn("16ГБ", str(self.ram))
        self.assertIn("DDR4", str(self.ram))


class TestGPU(unittest.TestCase):
    """Тесты класса GPU"""

    def setUp(self):
        self.gpu = GPU("RTX 3060", "NVIDIA", 170, 12, 1800, "PCIe 4.0")

    def test_gpu_creation(self):
        self.assertEqual(self.gpu.name, "RTX 3060")
        self.assertEqual(self.gpu.manufacturer, "NVIDIA")
        self.assertEqual(self.gpu.power_consumption, 170)
        self.assertEqual(self.gpu.vram, 12)
        self.assertEqual(self.gpu.frequency, 1800)
        self.assertEqual(self.gpu.interface, "PCIe 4.0")

    def test_gpu_vram_setter(self):
        self.gpu.vram = 24
        self.assertEqual(self.gpu.vram, 24)

        with self.assertRaises(InvalidDataError):
            self.gpu.vram = 0

    def test_gpu_str(self):
        self.assertIn("Видеокарта:", str(self.gpu))
        self.assertIn("12ГБ VRAM", str(self.gpu))


class TestStorage(unittest.TestCase):
    """Тесты класса Storage"""

    def setUp(self):
        self.storage = Storage("SSD 500", "Samsung", 5, 500, "SSD", "NVMe")

    def test_storage_creation(self):
        self.assertEqual(self.storage.name, "SSD 500")
        self.assertEqual(self.storage.manufacturer, "Samsung")
        self.assertEqual(self.storage.power_consumption, 5)
        self.assertEqual(self.storage.capacity, 500)
        self.assertEqual(self.storage.storage_type, "SSD")
        self.assertEqual(self.storage.interface, "NVMe")

    def test_storage_capacity_setter(self):
        self.storage.capacity = 1000
        self.assertEqual(self.storage.capacity, 1000)

        with self.assertRaises(InvalidDataError):
            self.storage.capacity = 0

    def test_storage_str(self):
        self.assertIn("Накопитель:", str(self.storage))
        self.assertIn("500ГБ", str(self.storage))
        self.assertIn("SSD", str(self.storage))


class TestMotherboard(unittest.TestCase):
    """Тесты класса Motherboard"""

    def setUp(self):
        self.mb = Motherboard("B550", "MSI", 50, "AM4", "DDR4", 128, 4, 3, "ATX")

    def test_motherboard_creation(self):
        self.assertEqual(self.mb.name, "B550")
        self.assertEqual(self.mb.manufacturer, "MSI")
        self.assertEqual(self.mb.power_consumption, 50)
        self.assertEqual(self.mb.socket, "AM4")
        self.assertEqual(self.mb.memory_type, "DDR4")
        self.assertEqual(self.mb.max_memory, 128)
        self.assertEqual(self.mb.memory_slots, 4)
        self.assertEqual(self.mb.pcie_slots, 3)

    def test_motherboard_str(self):
        self.assertIn("Материнская плата:", str(self.mb))
        self.assertIn("AM4", str(self.mb))
        self.assertIn("DDR4", str(self.mb))


class TestPowerSupply(unittest.TestCase):
    """Тесты класса PowerSupply"""

    def setUp(self):
        self.psu = PowerSupply("RM650", "Corsair", 0, 650)

    def test_psu_creation(self):
        self.assertEqual(self.psu.name, "RM650")
        self.assertEqual(self.psu.manufacturer, "Corsair")
        self.assertEqual(self.psu.power_consumption, 0)
        self.assertEqual(self.psu.wattage, 650)

    def test_psu_wattage_setter(self):
        self.psu.wattage = 850
        self.assertEqual(self.psu.wattage, 850)

        with self.assertRaises(InvalidDataError):
            self.psu.wattage = 0

    def test_psu_str(self):
        self.assertIn("Блок питания:", str(self.psu))
        self.assertIn("650Вт", str(self.psu))


if __name__ == '__main__':
    unittest.main()