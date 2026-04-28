#!/usr/bin/env python3
"""
Запуск CLI версии приложения.
"""

import argparse
from model.computer import Computer, Software, ComputerError, InsufficientSpaceError
from model.components import (
    Monitor, Keyboard, Mouse, ConnectionType,
    CPU, RAM, HardDisk, VideoCard, Motherboard, PowerSupply,
    SocketType, RAMType, Chipset
)
from model.exceptions import IncompatibleComponentError, PowerSupplyError


def create_computer() -> Computer:
    pc = Computer("Мой ПК")

    mb = Motherboard("ASUS PRIME B660M", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
    pc.install_motherboard(mb)

    cpu = CPU("Intel Core i5-12400", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
    pc.install_cpu(cpu)

    ram = RAM("Kingston DDR4 16GB", "Kingston", 5, 5000, RAMType.DDR4, 16)
    pc.add_ram(ram)

    hdd = HardDisk("Samsung 980 512GB", "Samsung", 10, 7000, 512)
    pc.install_hard_disk(hdd)

    gpu = VideoCard("NVIDIA RTX 3060", "NVIDIA", 170, 30000, 12, "GDDR6")
    pc.install_video_card(gpu)

    psu = PowerSupply("Corsair CV650", "Corsair", 0, 5000, 650)
    pc.install_power_supply(psu)

    return pc


def main():
    parser = argparse.ArgumentParser(description="Модель компьютера (CLI)")
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser('power-on', help='Включить')
    subparsers.add_parser('power-off', help='Выключить')
    subparsers.add_parser('info', help='Информация')
    subparsers.add_parser('check', help='Проверить совместимость')
    subparsers.add_parser('storage', help='Информация о диске')
    subparsers.add_parser('files', help='Список файлов')
    subparsers.add_parser('list', help='Список ПО')

    install_parser = subparsers.add_parser('install', help='Установить ПО')
    install_parser.add_argument('--name', required=True)
    install_parser.add_argument('--version', required=True)
    install_parser.add_argument('--size', type=int, required=True)
    install_parser.add_argument('--os', action='store_true')

    uninstall_parser = subparsers.add_parser('uninstall', help='Удалить ПО')
    uninstall_parser.add_argument('name')

    save_parser = subparsers.add_parser('save', help='Сохранить файл')
    save_parser.add_argument('filename')
    save_parser.add_argument('size', type=int)
    save_parser.add_argument('--type', default='document')

    delete_parser = subparsers.add_parser('delete', help='Удалить файл')
    delete_parser.add_argument('filename')

    connect_parser = subparsers.add_parser('connect', help='Подключить')
    connect_parser.add_argument('device', choices=['monitor', 'keyboard', 'mouse'])

    disconnect_parser = subparsers.add_parser('disconnect', help='Отключить')
    disconnect_parser.add_argument('device', choices=['monitor', 'keyboard', 'mouse'])

    update_parser = subparsers.add_parser('update-os', help='Обновить ОС')
    update_parser.add_argument('version')
    update_parser.add_argument('--size', type=int, default=5)

    args = parser.parse_args()
    computer = create_computer()

    try:
        if args.command == 'power-on':
            print(computer.power_on())
        elif args.command == 'power-off':
            print(computer.power_off())
        elif args.command == 'info':
            info = computer.get_system_info()
            print(f"\n=== {info['name']} ===")
            print(f"Статус: {info['status']}")
            print(f"ОС: {info['os']}")
            print(f"ПО: {info['software_count']}")
            print(f"Файлы: {info['files_count']}")
            print(f"Питание: {info['power_consumption']} Вт")
        elif args.command == 'check':
            report = computer.get_compatibility_report()
            print("\n=== СОВМЕСТИМОСТЬ ===")
            print("✅ Совместима" if report['compatible'] else "❌ Несовместима")
            for issue in report['issues']:
                print(f"  ❌ {issue}")
            for warn in report['warnings']:
                print(f"  ⚠️ {warn}")
        elif args.command == 'storage':
            s = computer.get_storage_info()
            print(f"Всего: {s['total']} ГБ")
            print(f"Использовано: {s['used']} ГБ")
            print(f"Свободно: {s['free']} ГБ")
        elif args.command == 'files':
            for f in computer.list_files():
                print(f"  • {f['name']} ({f['type']}) - {f['size']} ГБ")
        elif args.command == 'list':
            for sw in computer.list_installed_software():
                print(f"  • {sw['name']} {sw['version']} - {sw['size']} ГБ")
        elif args.command == 'install':
            sw = Software(args.name, args.version, args.size, args.os)
            print(computer.install_software(sw))
        elif args.command == 'uninstall':
            print(computer.uninstall_software(args.name))
        elif args.command == 'save':
            print(computer.save_file(args.filename, args.size, args.type))
        elif args.command == 'delete':
            print(computer.delete_file(args.filename))
        elif args.command == 'connect':
            if args.device == 'monitor':
                d = Monitor("LG", "LG", 30, 20000, 27, "1920x1080", ConnectionType.HDMI)
            elif args.device == 'keyboard':
                d = Keyboard("Logitech", "Logitech", 2, 3000, "ANSI", ConnectionType.USB, False)
            else:
                d = Mouse("Logitech", "Logitech", 2, 4000, 25600, ConnectionType.USB, False)
            print(computer.connect_peripheral(d))
        elif args.command == 'disconnect':
            print(computer.disconnect_peripheral(args.device))
        elif args.command == 'update-os':
            print(computer.update_os(args.version, args.size))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()