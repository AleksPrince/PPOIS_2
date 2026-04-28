
"""
Запуск GUI версии приложения.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model.computer import Computer
from model.components import (
    CPU, RAM, HardDisk, VideoCard, Motherboard, PowerSupply,
    SocketType, RAMType, Chipset
)
from controller.controller import ComputerController
from view.gui import ComputerGUI


def setup_demo_computer(computer: Computer):
    mb = Motherboard("ASUS PRIME B660M", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4)
    computer.install_motherboard(mb)

    cpu = CPU("Intel Core i5-12400", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5)
    computer.install_cpu(cpu)

    ram = RAM("Kingston DDR4 16GB", "Kingston", 5, 5000, RAMType.DDR4, 16)
    computer.add_ram(ram)

    hdd = HardDisk("Samsung 980 512GB", "Samsung", 10, 7000, 512)
    computer.install_hard_disk(hdd)

    gpu = VideoCard("NVIDIA RTX 3060", "NVIDIA", 170, 30000, 12, "GDDR6")
    computer.install_video_card(gpu)

    psu = PowerSupply("Corsair CV650", "Corsair", 0, 5000, 650)
    computer.install_power_supply(psu)


def main():
    computer = Computer("Мой компьютер")
    setup_demo_computer(computer)
    controller = ComputerController(computer)
    app = ComputerGUI(controller)
    app.run()


if __name__ == "__main__":
    main()