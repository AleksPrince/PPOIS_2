"""
Модуль с классами компонентов компьютера.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class SocketType(Enum):
    """Типы сокетов процессора."""
    LGA1700 = "LGA1700"
    LGA1200 = "LGA1200"
    AM4 = "AM4"
    AM5 = "AM5"


class RAMType(Enum):
    """Типы оперативной памяти."""
    DDR3 = "DDR3"
    DDR4 = "DDR4"
    DDR5 = "DDR5"


class ConnectionType(Enum):
    """Типы подключения периферии."""
    USB = "USB"
    USB_3 = "USB 3.0"
    USB_C = "USB-C"
    HDMI = "HDMI"
    DISPLAY_PORT = "DisplayPort"
    PS2 = "PS/2"
    BLUETOOTH = "Bluetooth"


class Chipset(Enum):
    """Типы чипсетов материнской платы."""
    H610 = "H610"
    B660 = "B660"
    Z690 = "Z690"
    B760 = "B760"
    Z790 = "Z790"
    H510 = "H510"
    B560 = "B560"
    Z590 = "Z590"
    B650 = "B650"
    X670 = "X670"
    X670E = "X670E"
    A520 = "A520"
    B550 = "B550"
    X570 = "X570"


@dataclass
class Component:
    """Базовый класс для всех компонентов компьютера."""
    name: str
    manufacturer: str
    power_consumption: int
    price: float

    def get_info(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "manufacturer": self.manufacturer,
            "price": self.price,
            "power_consumption": self.power_consumption
        }


@dataclass
class CPU(Component):
    """Класс процессора."""
    socket: SocketType
    cores: int
    frequency: float
    tdp: int = 65

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = self.tdp

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "socket": self.socket.value,
            "cores": self.cores,
            "frequency": self.frequency,
            "tdp": self.tdp
        })
        return info


@dataclass
class RAM(Component):
    """Класс оперативной памяти."""
    ram_type: RAMType
    size: int
    frequency: int = 3200

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 5

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "type": self.ram_type.value,
            "size": self.size,
            "frequency": self.frequency
        })
        return info


@dataclass
class HardDisk(Component):
    """Класс жесткого диска."""
    capacity: int
    interface: str = "SATA III"
    used_space: int = 0

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 10

    def save_data(self, size: int) -> bool:
        if self.used_space + size > self.capacity:
            raise ValueError(f"Недостаточно места. Свободно: {self.capacity - self.used_space}ГБ")
        self.used_space += size
        return True

    def get_free_space(self) -> int:
        return self.capacity - self.used_space

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "capacity": self.capacity,
            "interface": self.interface,
            "used_space": self.used_space
        })
        return info


@dataclass
class VideoCard(Component):
    """Класс видеокарты."""
    memory_size: int
    memory_type: str
    pcie_version: int = 4

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 200

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "memory_size": self.memory_size,
            "memory_type": self.memory_type,
            "pcie_version": self.pcie_version
        })
        return info


@dataclass
class Motherboard(Component):
    """Класс материнской платы."""
    socket: SocketType
    chipset: Chipset
    supported_ram_types: List[RAMType]
    max_ram_size: int
    ram_slots: int
    pcie_version: int = 4
    m2_slots: int = 2
    sata_ports: int = 4
    form_factor: str = "ATX"

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 30

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "socket": self.socket.value,
            "chipset": self.chipset.value,
            "supported_ram_types": [t.value for t in self.supported_ram_types],
            "max_ram_size": self.max_ram_size,
            "ram_slots": self.ram_slots,
            "pcie_version": self.pcie_version,
            "m2_slots": self.m2_slots,
            "sata_ports": self.sata_ports,
            "form_factor": self.form_factor
        })
        return info


@dataclass
class PowerSupply(Component):
    """Класс блока питания."""
    wattage: int
    efficiency: str = "80+ Bronze"
    modular: bool = False

    def __post_init__(self):
        self.power_consumption = 0

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "wattage": self.wattage,
            "efficiency": self.efficiency,
            "modular": self.modular
        })
        return info


@dataclass
class Monitor(Component):
    """Класс монитора."""
    screen_size: float
    resolution: str
    connection_type: ConnectionType
    refresh_rate: int = 60
    is_connected: bool = False

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 30

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "screen_size": self.screen_size,
            "resolution": self.resolution,
            "connection_type": self.connection_type.value,
            "refresh_rate": self.refresh_rate,
            "is_connected": self.is_connected
        })
        return info


@dataclass
class Keyboard(Component):
    """Класс клавиатуры."""
    layout: str
    connection_type: ConnectionType
    is_wireless: bool
    is_connected: bool = False

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 2

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "layout": self.layout,
            "connection_type": self.connection_type.value,
            "is_wireless": self.is_wireless,
            "is_connected": self.is_connected
        })
        return info


@dataclass
class Mouse(Component):
    """Класс мыши."""
    dpi: int
    connection_type: ConnectionType
    is_wireless: bool
    is_connected: bool = False

    def __post_init__(self):
        if self.power_consumption == 0:
            self.power_consumption = 2

    def get_info(self) -> Dict[str, Any]:
        info = super().get_info()
        info.update({
            "dpi": self.dpi,
            "connection_type": self.connection_type.value,
            "is_wireless": self.is_wireless,
            "is_connected": self.is_connected
        })
        return info