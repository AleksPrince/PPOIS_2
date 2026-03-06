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


class TestComputerIntegration(unittest.TestCase):
    """Интеграционные тесты"""

    def setUp(self):
        """Создаём компьютер и все компоненты"""
        self.computer = Computer("Gaming PC")

        # Компоненты для игрового ПК
        self.motherboard = Motherboard("X570", "ASUS", 70, "AM4", "DDR4", 128, 4, 3, "ATX")
        self.cpu = CPU("Ryzen 9", "AMD", "AM4", 16, 105)
        self.ram1 = RAM("DDR4 16GB", "Corsair", 5, 16, "DDR4", 3600)
        self.ram2 = RAM("DDR4 16GB", "Corsair", 5, 16, "DDR4", 3600)
        self.gpu = GPU("RTX 4090", "NVIDIA", 450, 24, 2500, "PCIe 4.0")
        self.storage = Storage("SSD 2TB", "Samsung", 6, 2000, "SSD", "NVMe")
        self.psu = PowerSupply("RM1000", "Corsair", 0, 1000)

        # Программы
        self.game = Program("Cyberpunk", 16, 8, 12, 100)
        self.browser = Program("Chrome", 4, 2, 1, 1)
        self.office = Program("Word", 2, 1, 0, 0.5)

    def test_full_gaming_pc_build(self):
        """Тест полной сборки игрового ПК"""

        # 1. Устанавливаем компоненты
        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram1)
        self.computer.install_ram(self.ram2)
        self.computer.install_gpu(self.gpu)
        self.computer.install_storage(self.storage)
        self.computer.install_psu(self.psu)

        # Проверяем, что всё установлено
        self.assertIsNotNone(self.computer.motherboard)
        self.assertIsNotNone(self.computer.cpu)
        self.assertEqual(len(self.computer.ram), 2)
        self.assertEqual(len(self.computer.gpu), 1)
        self.assertEqual(len(self.computer.storage), 1)
        self.assertIsNotNone(self.computer.psu)

        # 2. Проверяем потребление
        total_power = self.computer.get_total_power_consumption()
        expected = 70 + 105 + 5 + 5 + 450 + 6  # = 641
        self.assertEqual(total_power, expected)

        # 3. Включаем
        self.computer.power_on()
        self.assertEqual(self.computer.status, ComputerStatus.ON)

        # 4. Запускаем игру
        result = self.computer.run_program(self.game)
        self.assertEqual(self.computer.status, ComputerStatus.RUNNING)
        self.assertIn("успешно", result)

        # 5. Проверяем, что ресурсы заняты
        self.assertTrue(self.cpu.is_busy)
        self.assertTrue(self.ram1.is_busy)
        self.assertTrue(self.ram2.is_busy)
        self.assertTrue(self.gpu.is_busy)

        # 6. Останавливаем игру
        self.computer.stop_program()
        self.assertEqual(self.computer.status, ComputerStatus.ON)

        # 7. Проверяем, что ресурсы освободились
        self.assertFalse(self.cpu.is_busy)
        self.assertFalse(self.ram1.is_busy)
        self.assertFalse(self.ram2.is_busy)
        self.assertFalse(self.gpu.is_busy)

        # 8. Выключаем
        self.computer.power_off()
        self.assertEqual(self.computer.status, ComputerStatus.OFF)

    def test_incompatible_components(self):
        """Тест несовместимых компонентов"""

        # Неправильный CPU для материнской платы
        intel_cpu = CPU("i5", "Intel", "LGA1200", 6, 65)

        self.computer.install_motherboard(self.motherboard)

        with self.assertRaises(Exception):
            self.computer.install_cpu(intel_cpu)

        # Неправильная RAM
        ddr3_ram = RAM("DDR3", "Old", 8, 8, "DDR3", 1600)

        with self.assertRaises(Exception):
            self.computer.install_ram(ddr3_ram)

    def test_insufficient_power(self):
        """Тест недостаточного питания"""

        # Слабый БП
        weak_psu = PowerSupply("Weak", "Noname", 0, 300)

        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram1)
        self.computer.install_ram(self.ram2)
        self.computer.install_gpu(self.gpu)
        self.computer.install_psu(weak_psu)

        with self.assertRaises(Exception):
            self.computer.power_on()

    def test_remove_while_running(self):
        """Тест удаления компонентов во время работы"""

        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram1)
        self.computer.install_psu(self.psu)
        self.computer.power_on()
        self.computer.run_program(self.browser)

        # Нельзя удалить во время работы
        with self.assertRaises(Exception):
            self.computer.remove_cpu()

        with self.assertRaises(Exception):
            self.computer.remove_ram(0)

        # Останавливаем
        self.computer.stop_program()

        # Теперь можно удалить
        self.computer.remove_cpu()
        self.assertIsNone(self.computer.cpu)

    def test_multiple_programs_sequence(self):
        """Тест последовательного запуска программ"""

        self.computer.install_motherboard(self.motherboard)
        self.computer.install_cpu(self.cpu)
        self.computer.install_ram(self.ram1)
        self.computer.install_ram(self.ram2)
        self.computer.install_psu(self.psu)
        self.computer.power_on()

        # Запускаем офис
        self.computer.run_program(self.office)
        self.assertEqual(self.computer.status, ComputerStatus.RUNNING)
        self.computer.stop_program()

        # Запускаем браузер
        self.computer.run_program(self.browser)
        self.assertEqual(self.computer.status, ComputerStatus.RUNNING)
        self.computer.stop_program()

        # Нельзя запустить две сразу
        self.computer.run_program(self.browser)
        with self.assertRaises(Exception):
            self.computer.run_program(self.office)


if __name__ == '__main__':
    unittest.main()