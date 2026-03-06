import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from computer import Computer
from hardware.cpu import CPU
from hardware.ram import RAM
from hardware.gpu import GPU
from hardware.storage import Storage
from hardware.motherboard import Motherboard
from hardware.powersupply import PowerSupply
from software.program import Program
from software.task import ComputerStatus
from exceptions import (
    CompatibilityError, PowerError, ResourceBusyError,
    ComputerOffError, ResourceNotFoundError
)


class TestComputer(unittest.TestCase):
    """Тесты класса Computer"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.computer = Computer("TestPC")

        # Создаём совместимые компоненты
        self.motherboard = Motherboard("B550", "MSI", 50, "AM4", "DDR4", 128, 4, 3, "ATX")
        self.cpu = CPU("Ryzen 5", "AMD", "AM4", 6, 65)
        self.ram = RAM("DDR4 16GB", "Corsair", 5, 16, "DDR4", 3200)
        self.ram2 = RAM("DDR4 8GB", "Kingston", 4, 8, "DDR4", 3200)
        self.gpu = GPU("RTX 3060", "NVIDIA", 170, 12, 1800, "PCIe 4.0")
        self.storage = Storage("SSD 500", "Samsung", 5, 500, "SSD", "NVMe")
        self.psu = PowerSupply("RM650", "Corsair", 0, 650)

        # Несовместимые компоненты
        self.intel_cpu = CPU("i5", "Intel", "LGA1200", 6, 65)
        self.ddr3_ram = RAM("DDR3", "Old", 8, 8, "DDR3", 1600)

    def test_initial_state(self):
        """Тест начального состояния"""
        self.assertEqual(self.computer.name, "TestPC")
        self.assertEqual(self.computer.status, ComputerStatus.OFF)
        self.assertIsNone(self.computer.motherboard)
        self.assertIsNone(self.computer.cpu)
        self.assertEqual(len(self.computer.ram), 0)
        self.assertEqual(len(self.computer.gpu), 0)
        self.assertEqual(len(self.computer.storage), 0)
        self.assertIsNone(self.computer.psu)
        self.assertIsNone(self.computer.current_task)

    def test_install_motherboard(self):
        """Тест установки материнской платы"""
        result = self.computer.install_motherboard(self.motherboard)
        self.assertEqual(self.computer.motherboard, self.motherboard)
        self.assertTrue(self.motherboard.is_busy)
        self.assertIn("установлена", result)

        # Попытка установить ещё одну
        with self.assertRaises(ResourceBusyError):
            self.computer.install_motherboard(self.motherboard)

    def test_install_cpu_compatible(self):
        """Тест установки совместимого процессора"""
        self.computer.install_motherboard(self.motherboard)
        result = self.computer.install_cpu(self.cpu)
        self.assertEqual(self.computer.cpu, self.cpu)
        self.assertTrue(self.cpu.is_busy)
        self.assertIn("установлен", result)

    def test_install_cpu_no_motherboard(self):
        """Тест установки CPU без материнской платы"""
        with self.assertRaises(CompatibilityError):
            self.computer.install_cpu(self.cpu)

    def test_install_cpu_incompatible(self):
        """Тест установки несовместимого процессора"""
        self.computer.install_motherboard(self.motherboard)
        with self.assertRaises(CompatibilityError):
            self.computer.install_cpu(self.intel_cpu)

    def test_install_cpu_twice(self):
        """Тест установки второго процессора"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        with self.assertRaises(ResourceBusyError):
            self.computer.install_cpu(self.cpu)

    def test_install_ram_compatible(self):
        """Тест установки совместимой ОЗУ"""
        self.computer.install_motherboard(self.motherboard)
        result = self.computer.install_ram(self.ram)
        self.assertEqual(len(self.computer.ram), 1)
        self.assertTrue(self.ram.is_busy)
        self.assertIn("установлена", result)

    def test_install_ram_no_motherboard(self):
        """Тест установки ОЗУ без материнской платы"""
        with self.assertRaises(CompatibilityError):
            self.computer.install_ram(self.ram)

    def test_install_ram_incompatible_type(self):
        """Тест установки ОЗУ несовместимого типа"""
        self.computer.install_motherboard(self.motherboard)
        with self.assertRaises(CompatibilityError):
            self.computer.install_ram(self.ddr3_ram)

    def test_install_multiple_ram(self):
        """Тест установки нескольких планок ОЗУ"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_ram(self.ram)
        self.computer.install_ram(self.ram2)
        self.assertEqual(len(self.computer.ram), 2)

    def test_install_ram_exceeds_max(self):
        """Тест превышения максимального объёма ОЗУ"""
        self.computer.install_motherboard(self.motherboard)
        big_ram = RAM("Big", "Kingston", 10, 256, "DDR4", 3200)
        with self.assertRaises(CompatibilityError):
            self.computer.install_ram(big_ram)

    def test_install_gpu(self):
        """Тест установки видеокарты"""
        self.computer.install_motherboard(self.motherboard)
        result = self.computer.install_gpu(self.gpu)
        self.assertEqual(len(self.computer.gpu), 1)
        self.assertTrue(self.gpu.is_busy)
        self.assertIn("установлена", result)

    def test_install_gpu_no_motherboard(self):
        """Тест установки видеокарты без материнской платы"""
        with self.assertRaises(CompatibilityError):
            self.computer.install_gpu(self.gpu)

    def test_install_storage(self):
        """Тест установки накопителя"""
        result = self.computer.install_storage(self.storage)
        self.assertEqual(len(self.computer.storage), 1)
        self.assertTrue(self.storage.is_busy)
        self.assertIn("установлен", result)

    def test_install_psu(self):
        """Тест установки блока питания"""
        result = self.computer.install_psu(self.psu)
        self.assertEqual(self.computer.psu, self.psu)
        self.assertTrue(self.psu.is_busy)
        self.assertIn("установлен", result)

    def test_install_psu_twice(self):
        """Тест установки второго БП"""
        self.computer.install_psu(self.psu)
        with self.assertRaises(ResourceBusyError):
            self.computer.install_psu(self.psu)

    def test_power_on_success(self):
        """Тест успешного включения"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)
        self.computer.install_psu(self.psu)

        result = self.computer.power_on()
        self.assertEqual(self.computer.status, ComputerStatus.ON)
        self.assertIn("включён", result)

    def test_power_on_no_motherboard(self):
        """Тест включения без материнской платы"""
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)
        self.computer.install_psu(self.psu)

        with self.assertRaises(ResourceNotFoundError):
            self.computer.power_on()

    def test_power_on_no_cpu(self):
        """Тест включения без процессора"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_ram(self.ram)
        self.computer.install_psu(self.psu)

        with self.assertRaises(ResourceNotFoundError):
            self.computer.power_on()

    def test_power_on_no_ram(self):
        """Тест включения без ОЗУ"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_psu(self.psu)

        with self.assertRaises(ResourceNotFoundError):
            self.computer.power_on()

    def test_power_on_no_psu(self):
        """Тест включения без БП"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)

        with self.assertRaises(ResourceNotFoundError):
            self.computer.power_on()

    def test_power_on_insufficient_power(self):
        """Тест включения с недостаточным питанием"""
        weak_psu = PowerSupply("Weak", "Noname", 0, 100)

        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)
        self.computer.install_gpu(self.gpu)
        self.computer.install_psu(weak_psu)

        with self.assertRaises(PowerError):
            self.computer.power_on()

    def test_power_off(self):
        """Тест выключения"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)
        self.computer.install_psu(self.psu)
        self.computer.power_on()

        result = self.computer.power_off()
        self.assertEqual(self.computer.status, ComputerStatus.OFF)
        self.assertIn("выключен", result)

    def test_remove_cpu_when_on(self):
        """Тест удаления CPU при включённом компьютере"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)
        self.computer.install_psu(self.psu)
        self.computer.power_on()

        with self.assertRaises(ComputerOffError):
            self.computer.remove_cpu()

    def test_remove_cpu_when_off(self):
        """Тест удаления CPU при выключенном компьютере"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.power_off()

        result = self.computer.remove_cpu()
        self.assertIsNone(self.computer.cpu)
        self.assertFalse(self.cpu.is_busy)
        self.assertIn("удалён", result)

    def test_remove_ram_when_off(self):
        """Тест удаления ОЗУ при выключенном компьютере"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_ram(self.ram)
        self.computer.install_ram(self.ram2)

        result = self.computer.remove_ram(1)
        self.assertEqual(len(self.computer.ram), 1)
        self.assertEqual(self.computer.ram[0], self.ram)
        self.assertFalse(self.ram2.is_busy)

    def test_remove_nonexistent_ram(self):
        """Тест удаления несуществующей ОЗУ"""
        with self.assertRaises(ResourceNotFoundError):
            self.computer.remove_ram(0)

    def test_total_power_consumption(self):
        """Тест расчёта энергопотребления"""
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram)
        self.computer.install_gpu(self.gpu)
        self.computer.install_storage(self.storage)

        expected = 50 + 65 + 5 + 170 + 5  # 295
        self.assertEqual(self.computer.get_total_power_consumption(), expected)


if __name__ == '__main__':
    unittest.main()