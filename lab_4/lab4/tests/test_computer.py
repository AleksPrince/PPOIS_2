
import unittest
from datetime import datetime
from model.computer import Computer, Software, File, ComputerError, ComponentNotFoundError, InsufficientSpaceError
from model.components import (
    CPU, RAM, HardDisk, VideoCard, Monitor, Keyboard, Mouse, Motherboard, PowerSupply,
    SocketType, RAMType, ConnectionType, Chipset
)
from model.exceptions import IncompatibleComponentError, PowerSupplyError


class TestComponents(unittest.TestCase):
    """Тесты для классов компонентов."""

    def test_cpu_creation(self):
        cpu = CPU("Test CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        self.assertEqual(cpu.name, "Test CPU")
        self.assertEqual(cpu.manufacturer, "Intel")
        self.assertEqual(cpu.socket, SocketType.LGA1700)
        self.assertEqual(cpu.cores, 6)
        self.assertEqual(cpu.frequency, 2.5)
        self.assertEqual(cpu.tdp, 65)

    def test_cpu_power_consumption_auto(self):
        cpu = CPU("Test CPU", "Intel", 0, 15000, SocketType.LGA1700, 6, 2.5, tdp=65)
        self.assertEqual(cpu.power_consumption, 65)

    def test_ram_creation(self):
        ram = RAM("Test RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        self.assertEqual(ram.name, "Test RAM")
        self.assertEqual(ram.ram_type, RAMType.DDR4)
        self.assertEqual(ram.size, 16)

    def test_hard_disk_save_data(self):
        hdd = HardDisk("Test HDD", "Samsung", 10, 7000, 100)
        hdd.save_data(30)
        self.assertEqual(hdd.used_space, 30)
        self.assertEqual(hdd.get_free_space(), 70)

    def test_hard_disk_save_data_insufficient_space(self):
        hdd = HardDisk("Test HDD", "Samsung", 10, 7000, 100)
        with self.assertRaises(ValueError):
            hdd.save_data(150)

    def test_video_card_creation(self):
        gpu = VideoCard("Test GPU", "NVIDIA", 170, 30000, 12, "GDDR6")
        self.assertEqual(gpu.memory_size, 12)
        self.assertEqual(gpu.memory_type, "GDDR6")

    def test_monitor_creation(self):
        monitor = Monitor("Test Monitor", "LG", 30, 20000, 27, "1920x1080", ConnectionType.HDMI)
        self.assertEqual(monitor.screen_size, 27)
        self.assertEqual(monitor.resolution, "1920x1080")

    def test_keyboard_creation(self):
        kb = Keyboard("Test KB", "Logitech", 2, 3000, "ANSI", ConnectionType.USB, False)
        self.assertEqual(kb.layout, "ANSI")
        self.assertFalse(kb.is_wireless)

    def test_mouse_creation(self):
        mouse = Mouse("Test Mouse", "Logitech", 2, 4000, 25600, ConnectionType.USB, False)
        self.assertEqual(mouse.dpi, 25600)


class TestSoftware(unittest.TestCase):
    """Тесты для класса Software."""

    def test_software_creation(self):
        sw = Software("TestApp", "1.0", 10, is_os=False)
        self.assertEqual(sw.name, "TestApp")
        self.assertEqual(sw.version, "1.0")
        self.assertEqual(sw.size, 10)
        self.assertFalse(sw.is_os)

    def test_software_to_dict(self):
        sw = Software("TestApp", "1.0", 10, is_os=True)
        sw.installation_date = datetime.now()
        sw.is_installed = True
        result = sw.to_dict()
        self.assertEqual(result["name"], "TestApp")
        self.assertEqual(result["version"], "1.0")
        self.assertEqual(result["size"], 10)
        self.assertTrue(result["is_os"])


class TestFile(unittest.TestCase):
    """Тесты для класса File."""

    def test_file_creation(self):
        f = File("test.txt", 5, "document")
        self.assertEqual(f.name, "test.txt")
        self.assertEqual(f.size, 5)
        self.assertEqual(f.file_type, "document")

    def test_file_to_dict(self):
        f = File("test.txt", 5, "document")
        result = f.to_dict()
        self.assertEqual(result["name"], "test.txt")
        self.assertEqual(result["size"], 5)
        self.assertEqual(result["type"], "document")


class TestComputerCompatibility(unittest.TestCase):
    """Тесты совместимости компонентов."""

    def setUp(self):
        self.pc = Computer("Test PC")
        self.motherboard = Motherboard(
            "ASUS B660M", "ASUS", 30, 8000,
            SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4
        )
        self.cpu = CPU("i5-12400", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        self.ram = RAM("DDR4 16GB", "Kingston", 5, 5000, RAMType.DDR4, 16)
        self.hdd = HardDisk("SSD 512GB", "Samsung", 10, 7000, 512)
        self.gpu = VideoCard("RTX 3060", "NVIDIA", 170, 30000, 12, "GDDR6")
        self.psu = PowerSupply("CV650", "Corsair", 0, 5000, 650)

    def test_compatible_components(self):
        self.pc.install_motherboard(self.motherboard)
        self.pc.install_cpu(self.cpu)
        self.pc.add_ram(self.ram)
        self.pc.install_hard_disk(self.hdd)
        self.pc.install_video_card(self.gpu)
        self.pc.install_power_supply(self.psu)

        # Должно работать без ошибок
        self.assertEqual(self.pc.cpu.name, "i5-12400")

    def test_incompatible_cpu_socket(self):
        wrong_cpu = CPU("Ryzen", "AMD", 65, 15000, SocketType.AM4, 6, 3.5)
        self.pc.install_motherboard(self.motherboard)

        with self.assertRaises(IncompatibleComponentError):
            self.pc.install_cpu(wrong_cpu)

    def test_incompatible_ram_type(self):
        wrong_ram = RAM("DDR5 16GB", "Kingston", 5, 5000, RAMType.DDR5, 16)
        self.pc.install_motherboard(self.motherboard)

        with self.assertRaises(IncompatibleComponentError):
            self.pc.add_ram(wrong_ram)

    def test_ram_slots_limit(self):
        self.pc.install_motherboard(self.motherboard)
        # Добавляем 5 модулей при 4 слотах
        for i in range(5):
            ram = RAM(f"RAM{i}", "Kingston", 5, 5000, RAMType.DDR4, 8)
            self.pc.add_ram(ram)

        # 5-й модуль должен вызвать ошибку
        with self.assertRaises(IncompatibleComponentError):
            self.pc._check_compatibility()

    def test_insufficient_power_supply(self):
        self.pc.install_motherboard(self.motherboard)
        self.pc.install_cpu(self.cpu)
        self.pc.add_ram(self.ram)
        weak_psu = PowerSupply("Weak PSU", "Test", 0, 1000, 200)

        with self.assertRaises(PowerSupplyError):
            self.pc.install_power_supply(weak_psu)


class TestComputerPower(unittest.TestCase):
    """Тесты включения/выключения компьютера."""

    def setUp(self):
        self.pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 512)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)

    def test_power_on(self):
        result = self.pc.power_on()
        self.assertTrue(self.pc.is_powered_on)
        self.assertIn("включен", result)

    def test_power_off(self):
        self.pc.power_on()
        result = self.pc.power_off()
        self.assertFalse(self.pc.is_powered_on)
        self.assertIn("выключен", result)

    def test_power_on_missing_cpu(self):
        pc2 = Computer("Test PC2")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        pc2.install_motherboard(mb)
        # Нет CPU, RAM, HDD

        with self.assertRaises(ComputerError):
            pc2.power_on()

    def test_power_on_twice(self):
        self.pc.power_on()
        result = self.pc.power_on()
        self.assertIn("уже включен", result)

    def test_power_off_when_off(self):
        result = self.pc.power_off()
        self.assertIn("уже выключен", result)


class TestComputerSoftware(unittest.TestCase):
    """Тесты установки и удаления ПО."""

    def setUp(self):
        self.pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 512)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)
        self.pc.power_on()

    def test_install_software(self):
        sw = Software("TestApp", "1.0", 10)
        result = self.pc.install_software(sw)
        self.assertIn("установлено", result)
        self.assertEqual(len(self.pc.list_installed_software()), 1)

    def test_install_os(self):
        sw = Software("Windows", "11", 20, is_os=True)
        self.pc.install_software(sw)
        self.assertEqual(self.pc.os_name, "Windows")
        self.assertEqual(self.pc.os_version, "11")

    def test_install_software_when_off(self):
        self.pc.power_off()
        sw = Software("TestApp", "1.0", 10)
        with self.assertRaises(ComputerError):
            self.pc.install_software(sw)

    def test_install_software_no_hdd(self):
        pc2 = Computer("Test PC2")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        pc2.install_motherboard(mb)
        pc2.install_cpu(cpu)
        pc2.power_on()

        sw = Software("TestApp", "1.0", 10)
        with self.assertRaises(ComputerError):
            pc2.install_software(sw)

    def test_install_software_insufficient_space(self):
        # Заполняем диск
        big_file = Software("BigApp", "1.0", 500)
        with self.assertRaises(InsufficientSpaceError):
            self.pc.install_software(big_file)

    def test_uninstall_software(self):
        sw = Software("TestApp", "1.0", 10)
        self.pc.install_software(sw)
        result = self.pc.uninstall_software("TestApp")
        self.assertIn("удалено", result)

    def test_uninstall_nonexistent_software(self):
        with self.assertRaises(ComponentNotFoundError):
            self.pc.uninstall_software("Nonexistent")

    def test_list_installed_software(self):
        sw1 = Software("App1", "1.0", 10)
        sw2 = Software("App2", "2.0", 20)
        self.pc.install_software(sw1)
        self.pc.install_software(sw2)

        result = self.pc.list_installed_software()
        self.assertEqual(len(result), 2)


class TestComputerFiles(unittest.TestCase):
    """Тесты работы с файлами."""

    def setUp(self):
        self.pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 100)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)
        self.pc.power_on()

    def test_save_file(self):
        result = self.pc.save_file("test.txt", 10, "document")
        self.assertIn("сохранен", result)
        self.assertEqual(len(self.pc.list_files()), 1)

    def test_save_file_when_off(self):
        self.pc.power_off()
        with self.assertRaises(ComputerError):
            self.pc.save_file("test.txt", 10)

    def test_save_file_no_hdd(self):
        pc2 = Computer("Test PC2")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        pc2.install_motherboard(mb)
        pc2.install_cpu(cpu)
        pc2.power_on()

        with self.assertRaises(ComputerError):
            pc2.save_file("test.txt", 10)

    def test_save_file_insufficient_space(self):
        self.pc.save_file("file1.txt", 60)
        with self.assertRaises(InsufficientSpaceError):
            self.pc.save_file("file2.txt", 50)

    def test_save_duplicate_file(self):
        self.pc.save_file("test.txt", 10)
        with self.assertRaises(ComputerError):
            self.pc.save_file("test.txt", 20)

    def test_delete_file(self):
        self.pc.save_file("test.txt", 10)
        result = self.pc.delete_file("test.txt")
        self.assertIn("удален", result)
        self.assertEqual(len(self.pc.list_files()), 0)

    def test_delete_nonexistent_file(self):
        with self.assertRaises(ComponentNotFoundError):
            self.pc.delete_file("nonexistent.txt")

    def test_list_files(self):
        self.pc.save_file("file1.txt", 10)
        self.pc.save_file("file2.pdf", 20)
        files = self.pc.list_files()
        self.assertEqual(len(files), 2)


class TestComputerPeripherals(unittest.TestCase):
    """Тесты подключения периферии."""

    def setUp(self):
        self.pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 512)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)
        self.pc.power_on()

    def test_connect_monitor(self):
        monitor = Monitor("LG", "LG", 30, 20000, 27, "1920x1080", ConnectionType.HDMI)
        result = self.pc.connect_peripheral(monitor)
        self.assertIn("подключен", result)
        self.assertTrue(self.pc.get_connected_peripherals()['monitor'])

    def test_connect_keyboard(self):
        kb = Keyboard("G413", "Logitech", 2, 3000, "ANSI", ConnectionType.USB, False)
        result = self.pc.connect_peripheral(kb)
        self.assertIn("подключена", result)

    def test_connect_mouse(self):
        mouse = Mouse("G502", "Logitech", 2, 4000, 25600, ConnectionType.USB, False)
        result = self.pc.connect_peripheral(mouse)
        self.assertIn("подключена", result)

    def test_connect_when_off(self):
        self.pc.power_off()
        monitor = Monitor("LG", "LG", 30, 20000, 27, "1920x1080", ConnectionType.HDMI)
        with self.assertRaises(ComputerError):
            self.pc.connect_peripheral(monitor)

    def test_disconnect_monitor(self):
        monitor = Monitor("LG", "LG", 30, 20000, 27, "1920x1080", ConnectionType.HDMI)
        self.pc.connect_peripheral(monitor)
        result = self.pc.disconnect_peripheral("monitor")
        self.assertIn("отключен", result)
        self.assertFalse(self.pc.get_connected_peripherals()['monitor'])

    def test_disconnect_nonexistent(self):
        with self.assertRaises(ComponentNotFoundError):
            self.pc.disconnect_peripheral("monitor")

    def test_get_connected_peripherals(self):
        result = self.pc.get_connected_peripherals()
        self.assertIsInstance(result, dict)
        self.assertIn('monitor', result)
        self.assertIn('keyboard', result)
        self.assertIn('mouse', result)


class TestComputerOSUpdate(unittest.TestCase):
    """Тесты обновления ОС."""

    def setUp(self):
        self.pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 100)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)
        self.pc.power_on()

        # Устанавливаем ОС
        os = Software("Windows", "10", 20, is_os=True)
        self.pc.install_software(os)

    def test_update_os(self):
        result = self.pc.update_os("Windows 11", 5)
        self.assertIn("обновлена", result)
        self.assertEqual(self.pc.os_version, "Windows 11")

    def test_update_os_when_off(self):
        self.pc.power_off()
        with self.assertRaises(ComputerError):
            self.pc.update_os("Windows 11", 5)

    def test_update_os_no_os(self):
        pc2 = Computer("Test PC2")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 100)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        pc2.install_motherboard(mb)
        pc2.install_cpu(cpu)
        pc2.add_ram(ram)
        pc2.install_hard_disk(hdd)
        pc2.install_power_supply(psu)
        pc2.power_on()

        with self.assertRaises(ComputerError):
            pc2.update_os("Windows 11", 5)

    def test_update_os_insufficient_space(self):
        # Заполняем диск
        self.pc.save_file("bigfile.dat", 70)
        with self.assertRaises(InsufficientSpaceError):
            self.pc.update_os("Windows 11", 50)


class TestComputerStorageInfo(unittest.TestCase):
    """Тесты информации о хранилище."""

    def setUp(self):
        self.pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 100)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)
        self.pc.power_on()

    def test_get_storage_info(self):
        info = self.pc.get_storage_info()
        self.assertEqual(info['total'], 100)
        self.assertEqual(info['used'], 0)
        self.assertEqual(info['free'], 100)

    def test_get_storage_info_after_save(self):
        self.pc.save_file("test.txt", 30)
        info = self.pc.get_storage_info()
        self.assertEqual(info['used'], 30)
        self.assertEqual(info['free'], 70)

    def test_get_storage_info_no_hdd(self):
        pc2 = Computer("Test PC2")
        info = pc2.get_storage_info()
        self.assertIn("error", info)


class TestComputerSystemInfo(unittest.TestCase):
    """Тесты получения системной информации."""

    def setUp(self):
        self.pc = Computer("Test PC")
        self.motherboard = Motherboard("ASUS B660M", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4],
                                       128, 4)
        self.cpu = CPU("i5-12400", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        self.ram = RAM("DDR4 16GB", "Kingston", 5, 5000, RAMType.DDR4, 16)
        self.hdd = HardDisk("SSD 512GB", "Samsung", 10, 7000, 512)

        self.pc.install_motherboard(self.motherboard)
        self.pc.install_cpu(self.cpu)
        self.pc.add_ram(self.ram)
        self.pc.install_hard_disk(self.hdd)

    def test_get_system_info(self):
        info = self.pc.get_system_info()
        self.assertEqual(info['name'], "Test PC")
        self.assertEqual(info['status'], "выключен")
        self.assertIsNotNone(info['components']['cpu'])
        self.assertEqual(len(info['components']['ram']), 1)

    def test_get_system_info_after_power_on(self):
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)
        self.pc.install_power_supply(psu)
        self.pc.power_on()
        info = self.pc.get_system_info()
        self.assertEqual(info['status'], "включен")

    def test_get_system_info_with_software(self):
        sw = Software("TestApp", "1.0", 10)
        self.pc.power_on()
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)
        self.pc.install_power_supply(psu)
        self.pc.install_software(sw)
        info = self.pc.get_system_info()
        self.assertEqual(info['software_count'], 1)


class TestComputerCompatibilityReport(unittest.TestCase):
    """Тесты отчета о совместимости."""

    def setUp(self):
        self.pc = Computer("Test PC")

    def test_compatible_configuration(self):
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_power_supply(psu)

        report = self.pc.get_compatibility_report()
        self.assertTrue(report['compatible'])

    def test_incompatible_cpu_socket_report(self):
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "AMD", 65, 15000, SocketType.AM4, 6, 3.5)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)

        report = self.pc.get_compatibility_report()
        self.assertFalse(report['compatible'])
        self.assertTrue(len(report['issues']) > 0)

    def test_incompatible_ram_report(self):
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR5, 16)

        self.pc.install_motherboard(mb)
        self.pc.add_ram(ram)

        report = self.pc.get_compatibility_report()
        self.assertFalse(report['compatible'])


class TestObserverPattern(unittest.TestCase):
    """Тесты паттерна Observer."""

    def setUp(self):
        self.pc = Computer("Test PC")
        self.notifications = []

        class TestObserver:
            def __init__(self, notifications):
                self.notifications = notifications

            def update(self, event, data):
                self.notifications.append((event, data))

        self.observer = TestObserver(self.notifications)
        self.pc.add_observer(self.observer)

        # Добавляем минимальные компоненты
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 512)
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)

        self.pc.install_motherboard(mb)
        self.pc.install_cpu(cpu)
        self.pc.add_ram(ram)
        self.pc.install_hard_disk(hdd)
        self.pc.install_power_supply(psu)

    def test_power_on_notification(self):
        self.pc.power_on()
        events = [e for e, _ in self.notifications]
        self.assertIn("power_on", events)

    def test_power_off_notification(self):
        self.pc.power_on()
        self.pc.power_off()
        events = [e for e, _ in self.notifications]
        self.assertIn("power_off", events)

    def test_software_install_notification(self):
        sw = Software("TestApp", "1.0", 10)
        self.pc.power_on()
        self.pc.install_software(sw)
        events = [e for e, _ in self.notifications]
        self.assertIn("software_installed", events)

    def test_file_save_notification(self):
        self.pc.power_on()
        self.pc.save_file("test.txt", 10)
        events = [e for e, _ in self.notifications]
        self.assertIn("file_saved", events)


class TestPowerCalculation(unittest.TestCase):
    """Тесты расчета энергопотребления."""

    def test_power_calculation(self):
        pc = Computer("Test PC")
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5, tdp=65)
        ram = RAM("RAM", "Kingston", 5, 5000, RAMType.DDR4, 16)
        gpu = VideoCard("GPU", "NVIDIA", 170, 30000, 12, "GDDR6")
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 512)

        pc.install_motherboard(mb)
        pc.install_cpu(cpu)
        pc.add_ram(ram)
        pc.install_video_card(gpu)
        pc.install_hard_disk(hdd)

        power = pc._calculate_power_consumption()
        self.assertGreater(power, 200)  # Должно быть >200W


class TestGetComponentsList(unittest.TestCase):
    """Тесты получения списка компонентов."""

    def test_get_components_list(self):
        pc = Computer("Test PC")
        components = pc.get_components_list()

        self.assertIn("motherboard", components)
        self.assertIn("cpu", components)
        self.assertIn("ram", components)
        self.assertIn("gpu", components)
        self.assertIn("hdd", components)
        self.assertIn("psu", components)

        self.assertGreater(len(components["cpu"]), 0)
        self.assertGreater(len(components["ram"]), 0)


class TestComponentInstallation(unittest.TestCase):
    """Тесты установки компонентов."""

    def setUp(self):
        self.pc = Computer("Test PC")

    def test_install_motherboard(self):
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        result = self.pc.install_motherboard(mb)
        self.assertIn("установлена", result)
        self.assertIsNotNone(self.pc.motherboard)

    def test_install_cpu(self):
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        cpu = CPU("CPU", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)

        self.pc.install_motherboard(mb)
        result = self.pc.install_cpu(cpu)
        self.assertIn("установлен", result)

    def test_install_hard_disk(self):
        hdd = HardDisk("HDD", "Samsung", 10, 7000, 512)
        result = self.pc.install_hard_disk(hdd)
        self.assertIn("установлен", result)

    def test_install_video_card(self):
        mb = Motherboard("MB", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
        gpu = VideoCard("GPU", "NVIDIA", 170, 30000, 12, "GDDR6")

        self.pc.install_motherboard(mb)
        result = self.pc.install_video_card(gpu)
        self.assertIn("установлена", result)

    def test_install_power_supply(self):
        psu = PowerSupply("PSU", "Corsair", 0, 5000, 650)
        result = self.pc.install_power_supply(psu)
        self.assertIn("установлен", result)


if __name__ == "__main__":
    unittest.main()