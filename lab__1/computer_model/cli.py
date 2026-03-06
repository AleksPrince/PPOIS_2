import sys
import os
import cmd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from computer import Computer
from hardware.cpu import CPU
from hardware.ram import RAM
from hardware.gpu import GPU
from hardware.storage import Storage
from hardware.motherboard import Motherboard
from hardware.powersupply import PowerSupply
from software.program import Program
from exceptions import ComputerError


class ComputerCLI(cmd.Cmd):
    prompt = "<Компютер> "

    def __init__(self):
        super().__init__()
        self.computer = Computer()

        # Каталог компонентов
        self.catalog = {
            'cpu': [
                CPU("Ryzen 5 5600X", "AMD", "AM4", 6, 65),
                CPU("Core i5-11400", "Intel", "LGA1200", 6, 65),
                CPU("Ryzen 9 5950X", "AMD", "AM4", 16, 105),
            ],
            'ram': [
                RAM("DDR4 8GB", "Corsair", 5, 8, "DDR4", 3200),
                RAM("DDR4 16GB", "Kingston", 8, 16, "DDR4", 3200),
                RAM("DDR5 16GB", "G.Skill", 10, 16, "DDR5", 4800),
            ],
            'gpu': [
                GPU("RTX 3060", "NVIDIA", 170, 12, 1800, "PCIe 4.0"),
                GPU("RX 6600", "AMD", 132, 8, 2000, "PCIe 4.0"),
                GPU("RTX 4090", "NVIDIA", 450, 24, 2500, "PCIe 4.0"),
            ],
            'storage': [
                Storage("SSD 500GB", "Samsung", 5, 500, "SSD", "NVMe"),
                Storage("HDD 2TB", "Seagate", 10, 2000, "HDD", "SATA"),
                Storage("SSD 1TB", "WD", 6, 1000, "SSD", "NVMe"),
            ],
            'motherboard': [
                Motherboard("B550 Tomahawk", "MSI", 50, "AM4", "DDR4", 128, 4, 3, "ATX"),
                Motherboard("Z590 Aorus", "Gigabyte", 60, "LGA1200", "DDR4", 128, 4, 4, "ATX"),
                Motherboard("X570 Hero", "ASUS", 70, "AM4", "DDR4", 128, 4, 3, "ATX"),
            ],
            'psu': [
                PowerSupply("RM650x", "Corsair", 0, 650),
                PowerSupply("Focus 850", "Seasonic", 0, 850),
                PowerSupply("TX1000", "Corsair", 0, 1000),
            ]
        }

        # Программы
        self.programs = [
            Program("Калькулятор", 0.5, 1, 0, 0.1),
            Program("Браузер", 4, 2, 1, 1),
            Program("Игра", 16, 8, 8, 50),
            Program("Видеоредактор", 32, 16, 12, 100),
        ]

        # Соответствие цифр командам
        self.commands = {
            '1': 'Показать каталог',
            '2': 'Показать сборку',
            '3': 'Установить компонент',
            '4': 'Удалить компонент',
            '5': 'Включить ПК',
            '6': 'Выключить ПК',
            '7': 'Запустить программу',
            '8': 'Остановить программу',
            '9': 'Проверить совместимость',
            '0': 'Выход'
        }

    def show_menu(self):
        """Показать главное меню"""
        print("\n" + "=" * 50)
        print(" ГЛАВНОЕ МЕНЮ")
        print("=" * 50)
        for key, desc in self.commands.items():
            print(f"  {key}. {desc}")
        print("=" * 50)

    def show_catalog(self):
        """Показать каталог компонентов"""
        print("\n" + "=" * 50)
        print(" КАТАЛОГ КОМПОНЕНТОВ")
        print("=" * 50)

        # Процессоры
        print("\n1. ПРОЦЕССОРЫ:")
        for i, cpu in enumerate(self.catalog['cpu']):
            print(f"   [{i}] {cpu}")

        # ОЗУ
        print("\n2. ОПЕРАТИВНАЯ ПАМЯТЬ:")
        for i, ram in enumerate(self.catalog['ram']):
            print(f"   [{i}] {ram}")

        # Видеокарты
        print("\n3. ВИДЕОКАРТЫ:")
        for i, gpu in enumerate(self.catalog['gpu']):
            print(f"   [{i}] {gpu}")

        # Накопители
        print("\n4. НАКОПИТЕЛИ:")
        for i, storage in enumerate(self.catalog['storage']):
            print(f"   [{i}] {storage}")

        # Материнские платы
        print("\n5. МАТЕРИНСКИЕ ПЛАТЫ:")
        for i, mb in enumerate(self.catalog['motherboard']):
            print(f"   [{i}] {mb}")

        # Блоки питания
        print("\n6. БЛОКИ ПИТАНИЯ:")
        for i, psu in enumerate(self.catalog['psu']):
            print(f"   [{i}] {psu}")

    def show_programs(self):
        """Показать доступные программы"""
        print("\n" + "=" * 50)
        print("📱 ПРОГРАММЫ")
        print("=" * 50)
        for i, prog in enumerate(self.programs):
            print(f"  [{i}] {prog}")

    def install_component(self):
        """Установка компонента"""
        self.show_catalog()

        try:
            cat = input("\nВыберите категорию (1-6): ").strip()
            idx = input("Выберите индекс компонента: ").strip()

            cat_map = {
                '1': 'cpu', '2': 'ram', '3': 'gpu',
                '4': 'storage', '5': 'motherboard', '6': 'psu'
            }

            if cat not in cat_map:
                print(" Неверная категория")
                return

            comp_type = cat_map[cat]
            idx = int(idx)

            if idx < 0 or idx >= len(self.catalog[comp_type]):
                print(" Неверный индекс")
                return

            component = self.catalog[comp_type][idx]

            if comp_type == 'cpu':
                result = self.computer.install_cpu(component)
            elif comp_type == 'ram':
                result = self.computer.install_ram(component)
            elif comp_type == 'gpu':
                result = self.computer.install_gpu(component)
            elif comp_type == 'storage':
                result = self.computer.install_storage(component)
            elif comp_type == 'motherboard':
                result = self.computer.install_motherboard(component)
            elif comp_type == 'psu':
                result = self.computer.install_psu(component)

            print(result)

        except ValueError:
            print(" Введите числа")
        except ComputerError as e:
            print(f" Ошибка: {e}")

    def remove_component(self):
        """Удаление компонента"""
        print("\n🗑  УДАЛЕНИЕ КОМПОНЕНТА")
        print("1. Процессор")
        print("2. ОЗУ")
        print("3. Видеокарта")
        print("4. Накопитель")
        print("5. Материнская плата")
        print("6. Блок питания")

        try:
            cat = input("\nВыберите категорию (1-6): ").strip()

            if cat == '1':
                result = self.computer.remove_cpu()
            elif cat == '2':
                idx = input("Индекс планки ОЗУ (0,1,...): ").strip()
                result = self.computer.remove_ram(int(idx))
            elif cat == '3':
                idx = input("Индекс видеокарты (0,1,...): ").strip()
                result = self.computer.remove_gpu(int(idx))
            elif cat == '4':
                idx = input("Индекс накопителя (0,1,...): ").strip()
                result = self.computer.remove_storage(int(idx))
            elif cat == '5':
                result = self.computer.remove_motherboard()
            elif cat == '6':
                result = self.computer.remove_psu()
            else:
                print(" Неверная категория")
                return

            print(result)

        except ValueError:
            print(" Введите число")
        except ComputerError as e:
            print(f" Ошибка: {e}")

    def run_program(self):
        """Запуск программы"""
        self.show_programs()

        try:
            idx = input("\nВыберите программу (индекс): ").strip()
            idx = int(idx)

            if idx < 0 or idx >= len(self.programs):
                print(" Неверный индекс")
                return

            result = self.computer.run_program(self.programs[idx])
            print(result)

        except ValueError:
            print(" Введите число")
        except ComputerError as e:
            print(f" Ошибка: {e}")

    def check_compatibility(self):
        """Проверка совместимости"""
        print("\n ПРОВЕРКА КОМПЬЮТЕРА:")

        # Проверка наличия компонентов
        missing = []
        if not self.computer.motherboard:
            missing.append("материнская плата")
        if not self.computer.cpu:
            missing.append("процессор")
        if not self.computer.ram:
            missing.append("ОЗУ")
        if not self.computer.psu:
            missing.append("блок питания")

        if missing:
            print(" Отсутствуют: " + ", ".join(missing))
        else:
            print(" Все основные компоненты на месте")

        # Проверка совместимости
        if self.computer.cpu and self.computer.motherboard:
            if self.computer.cpu.socket != self.computer.motherboard.socket:
                print(f" Сокеты: CPU {self.computer.cpu.socket} != MB {self.computer.motherboard.socket}")
            else:
                print(" Сокеты совместимы")

        # Проверка питания
        if self.computer.psu:
            total_power = self.computer.get_total_power_consumption()
            print(f"\n Потребление: {total_power}Вт / {self.computer.psu.wattage}Вт")

            if total_power <= self.computer.psu.wattage:
                print(" Питания достаточно")
            else:
                print(f" Не хватает {total_power - self.computer.psu.wattage}Вт")

    def do_menu(self, arg):
        """Показать меню"""
        self.show_menu()

    def default(self, line):
        """Обработка ввода"""
        if line == 'menu':
            self.show_menu()
            return

        if line == '0' or line == 'exit' or line == 'quit':
            print(" До следующей лабы!")
            return True

        if line == '1':
            self.show_catalog()
        elif line == '2':
            print(self.computer.get_info())
        elif line == '3':
            self.install_component()
        elif line == '4':
            self.remove_component()
        elif line == '5':
            try:
                result = self.computer.power_on()
                print(result)
            except ComputerError as e:
                print(f" {e}")
        elif line == '6':
            result = self.computer.power_off()
            print(result)
        elif line == '7':
            self.run_program()
        elif line == '8':
            try:
                result = self.computer.stop_program()
                print(result)
            except ComputerError as e:
                print(f" {e}")
        elif line == '9':
            self.check_compatibility()
        else:
            print(" Неверная команда. Введите 'menu' для списка команд")

    def emptyline(self):
        self.show_menu()


def main():
    cli = ComputerCLI()
    print("\n" + "=" * 50)
    print("МОДЕЛЬ КОМПЬЮТЕРА")
    print("=" * 50)
    print("Вводите цифры для выбора действий")
    print("Введите 'menu' для показа меню")
    print("=" * 50)
    cli.cmdloop()


if __name__ == "__main__":
    main()