"""
Модуль с основным классом Computer (Модель).
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from .components import (
    CPU, RAM, HardDisk, VideoCard, Monitor, Keyboard, Mouse, Motherboard, PowerSupply,
    SocketType, RAMType, ConnectionType, Chipset
)
from .exceptions import (
    ComputerError, ComponentNotFoundError, IncompatibleComponentError,
    PowerSupplyError, InsufficientSpaceError
)


class File:
    """Класс для представления файла на диске."""

    def __init__(self, name: str, size: int, file_type: str = "unknown"):
        self.name = name
        self.size = size
        self.file_type = file_type
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "size": self.size,
            "type": self.file_type,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }


class Software:
    """Класс для представления программного обеспечения."""

    def __init__(self, name: str, version: str, size: int, is_os: bool = False):
        self.name = name
        self.version = version
        self.size = size
        self.is_os = is_os
        self.installation_date: Optional[datetime] = None
        self.is_installed = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "size": self.size,
            "is_os": self.is_os,
            "installation_date": self.installation_date.strftime("%Y-%m-%d %H:%M") if self.installation_date else None,
            "is_installed": self.is_installed
        }


class Computer:
    """Класс, представляющий компьютер."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_powered_on = False
        self.os_name: Optional[str] = None
        self.os_version: Optional[str] = None

        # Компоненты
        self.cpu: Optional[CPU] = None
        self.motherboard: Optional[Motherboard] = None
        self.ram: List[RAM] = []
        self.hard_disk: Optional[HardDisk] = None
        self.video_card: Optional[VideoCard] = None
        self.power_supply: Optional[PowerSupply] = None

        # Периферия
        self.monitor: Optional[Monitor] = None
        self.keyboard: Optional[Keyboard] = None
        self.mouse: Optional[Mouse] = None

        # ПО и файлы
        self.installed_software: List[Software] = []
        self.files: List[File] = []

        # Наблюдатели
        self._observers = []

    def add_observer(self, observer) -> None:
        self._observers.append(observer)

    def _notify(self, event: str, data: Any = None) -> None:
        for observer in self._observers:
            observer.update(event, data)

    # === Вспомогательные методы ===
    def _calculate_power_consumption(self) -> int:
        """Рассчитать общее энергопотребление."""
        total = 0
        if self.cpu:
            total += self.cpu.tdp
        if self.video_card:
            total += self.video_card.power_consumption
        if self.hard_disk:
            total += 10
        for ram in self.ram:
            total += 5
        total += 30
        return total

    def _check_compatibility(self) -> None:
        """Проверить совместимость компонентов."""
        if not self.motherboard:
            return

        if self.cpu and self.cpu.socket != self.motherboard.socket:
            raise IncompatibleComponentError(
                f"Сокет процессора {self.cpu.socket.value} несовместим "
                f"с сокетом материнской платы {self.motherboard.socket.value}"
            )

        for ram in self.ram:
            if ram.ram_type not in self.motherboard.supported_ram_types:
                raise IncompatibleComponentError(
                    f"Тип памяти {ram.ram_type.value} не поддерживается"
                )

        total_ram = sum(r.size for r in self.ram)
        if total_ram > self.motherboard.max_ram_size:
            raise IncompatibleComponentError(
                f"Объем ОЗУ ({total_ram}ГБ) превышает максимум ({self.motherboard.max_ram_size}ГБ)"
            )

        if len(self.ram) > self.motherboard.ram_slots:
            raise IncompatibleComponentError(
                f"Количество модулей ОЗУ ({len(self.ram)}) превышает количество слотов ({self.motherboard.ram_slots})"
            )

        if self.power_supply:
            total_power = self._calculate_power_consumption()
            if self.power_supply.wattage < total_power:
                raise PowerSupplyError(
                    f"Мощность БП ({self.power_supply.wattage}Вт) недостаточна для системы ({total_power}Вт)"
                )

    # === Установка компонентов ===
    def install_motherboard(self, motherboard: Motherboard) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно установить: компьютер включен")
        self.motherboard = motherboard
        self._notify("component_changed", {"type": "motherboard", "name": motherboard.name})
        return f"Материнская плата {motherboard.name} установлена"

    def install_cpu(self, cpu: CPU) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно установить: компьютер включен")
        old_cpu = self.cpu
        self.cpu = cpu
        try:
            self._check_compatibility()
        except Exception as e:
            self.cpu = old_cpu
            raise e
        self._notify("component_changed", {"type": "cpu", "name": cpu.name})
        return f"Процессор {cpu.name} установлен"

    def add_ram(self, ram: RAM) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно добавить: компьютер включен")
        self.ram.append(ram)
        try:
            self._check_compatibility()
        except Exception as e:
            self.ram.pop()
            raise e
        self._notify("component_changed", {"type": "ram", "action": "add", "name": ram.name})
        return f"Модуль памяти {ram.name} добавлен"

    def remove_ram(self, index: int) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно удалить: компьютер включен")
        if index < 0 or index >= len(self.ram):
            raise ComponentNotFoundError("Модуль памяти не найден")
        removed = self.ram.pop(index)
        self._notify("component_changed", {"type": "ram", "action": "remove", "name": removed.name})
        return f"Модуль памяти {removed.name} удален"

    def install_hard_disk(self, hard_disk: HardDisk) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно установить: компьютер включен")
        self.hard_disk = hard_disk
        self._notify("component_changed", {"type": "hard_disk", "name": hard_disk.name})
        return f"Жесткий диск {hard_disk.name} установлен"

    def install_video_card(self, video_card: VideoCard) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно установить: компьютер включен")
        old_gpu = self.video_card
        self.video_card = video_card
        try:
            self._check_compatibility()
        except Exception as e:
            self.video_card = old_gpu
            raise e
        self._notify("component_changed", {"type": "video_card", "name": video_card.name})
        return f"Видеокарта {video_card.name} установлена"

    def install_power_supply(self, power_supply: PowerSupply) -> str:
        if self.is_powered_on:
            raise ComputerError("Невозможно установить: компьютер включен")
        old_psu = self.power_supply
        self.power_supply = power_supply
        try:
            self._check_compatibility()
        except Exception as e:
            self.power_supply = old_psu
            raise e
        self._notify("component_changed", {"type": "power_supply", "name": power_supply.name})
        return f"Блок питания {power_supply.name} установлен"

    # === Операции питания ===
    def power_on(self) -> str:
        if self.is_powered_on:
            return "Компьютер уже включен"

        try:
            self._check_compatibility()
        except Exception as e:
            raise ComputerError(f"Нельзя включить: {e}")

        missing = []
        if not self.cpu:
            missing.append("процессор")
        if not self.motherboard:
            missing.append("материнская плата")
        if not self.ram:
            missing.append("ОЗУ")
        if not self.hard_disk:
            missing.append("жесткий диск")
        if not self.power_supply:
            missing.append("блок питания")

        if missing:
            raise ComputerError(f"Отсутствуют: {', '.join(missing)}")

        self.is_powered_on = True
        self._notify("power_on", None)
        return f"Компьютер {self.name} включен"

    def power_off(self) -> str:
        if not self.is_powered_on:
            return "Компьютер уже выключен"
        self.is_powered_on = False
        self._notify("power_off", None)
        return f"Компьютер {self.name} выключен"

    # === Операции с ПО ===
    def install_software(self, software: Software) -> str:
        if not self.is_powered_on:
            raise ComputerError("Невозможно установить: компьютер выключен")
        if not self.hard_disk:
            raise ComputerError("Нет жесткого диска")

        total_software = sum(sw.size for sw in self.installed_software if sw.is_installed)
        total_files = sum(f.size for f in self.files)
        used_space = total_software + total_files

        if used_space + software.size > self.hard_disk.capacity:
            free = self.hard_disk.capacity - used_space
            raise InsufficientSpaceError(f"Недостаточно места. Нужно: {software.size}ГБ, свободно: {free}ГБ")

        software.installation_date = datetime.now()
        software.is_installed = True
        self.installed_software.append(software)

        if software.is_os:
            self.os_name = software.name
            self.os_version = software.version

        self._notify("software_installed", software.to_dict())
        return f"ПО {software.name} версии {software.version} установлено"

    def uninstall_software(self, software_name: str) -> str:
        for sw in self.installed_software:
            if sw.name == software_name and sw.is_installed:
                sw.is_installed = False
                self._notify("software_uninstalled", sw.to_dict())
                return f"ПО {software_name} удалено"
        raise ComponentNotFoundError(f"ПО {software_name} не найдено")

    def list_installed_software(self) -> List[Dict[str, Any]]:
        return [sw.to_dict() for sw in self.installed_software if sw.is_installed]

    # === Операции с файлами ===
    def save_file(self, filename: str, size: int, file_type: str = "document") -> str:
        if not self.is_powered_on:
            raise ComputerError("Невозможно сохранить: компьютер выключен")
        if not self.hard_disk:
            raise ComputerError("Нет жесткого диска")

        for f in self.files:
            if f.name == filename:
                raise ComputerError(f"Файл {filename} уже существует")

        total_software = sum(sw.size for sw in self.installed_software if sw.is_installed)
        total_files = sum(f.size for f in self.files)
        used_space = total_software + total_files

        if used_space + size > self.hard_disk.capacity:
            free = self.hard_disk.capacity - used_space
            raise InsufficientSpaceError(f"Недостаточно места. Нужно: {size}ГБ, свободно: {free}ГБ")

        new_file = File(filename, size, file_type)
        self.files.append(new_file)
        self._notify("file_saved", new_file.to_dict())
        self._notify("storage_updated", self.get_storage_info())
        return f"Файл {filename} сохранен ({size}ГБ)"

    def delete_file(self, filename: str) -> str:
        for file in self.files:
            if file.name == filename:
                self.files.remove(file)
                self._notify("file_deleted", {"filename": filename})
                self._notify("storage_updated", self.get_storage_info())
                return f"Файл {filename} удален"
        raise ComponentNotFoundError(f"Файл {filename} не найден")

    def list_files(self) -> List[Dict[str, Any]]:
        return [f.to_dict() for f in self.files]

    def get_storage_info(self) -> Dict[str, Any]:
        if not self.hard_disk:
            return {"error": "Жесткий диск не установлен"}

        total_software = sum(sw.size for sw in self.installed_software if sw.is_installed)
        total_files = sum(f.size for f in self.files)
        used_space = total_software + total_files

        return {
            "total": self.hard_disk.capacity,
            "used": used_space,
            "free": self.hard_disk.capacity - used_space,
            "software_size": total_software,
            "files_size": total_files,
            "usage_percent": (used_space / self.hard_disk.capacity) * 100 if self.hard_disk.capacity > 0 else 0
        }

    # === Операции с периферией ===
    def connect_peripheral(self, device) -> str:
        if not self.is_powered_on:
            raise ComputerError("Невозможно подключить: компьютер выключен")

        if isinstance(device, Monitor):
            self.monitor = device
            device.is_connected = True
        elif isinstance(device, Keyboard):
            self.keyboard = device
            device.is_connected = True
        elif isinstance(device, Mouse):
            self.mouse = device
            device.is_connected = True
        else:
            raise ComputerError("Неизвестный тип устройства")

        self._notify("peripheral_connected", {"type": type(device).__name__.lower(), "name": device.name})
        return f"{device.name} подключен"

    def disconnect_peripheral(self, device_type: str) -> str:
        device_type = device_type.lower()

        if device_type == "monitor" and self.monitor:
            name = self.monitor.name
            self.monitor = None
        elif device_type == "keyboard" and self.keyboard:
            name = self.keyboard.name
            self.keyboard = None
        elif device_type == "mouse" and self.mouse:
            name = self.mouse.name
            self.mouse = None
        else:
            raise ComponentNotFoundError(f"Устройство {device_type} не подключено")

        self._notify("peripheral_disconnected", {"type": device_type})
        return f"{name} отключен"

    def get_connected_peripherals(self) -> Dict[str, bool]:
        return {
            "monitor": self.monitor is not None,
            "keyboard": self.keyboard is not None,
            "mouse": self.mouse is not None
        }

    # === Обновление ОС ===
    def update_os(self, new_version: str, update_size: int) -> str:
        if not self.is_powered_on:
            raise ComputerError("Невозможно обновить: компьютер выключен")
        if not self.os_name or not self.os_version:
            raise ComputerError("Операционная система не установлена")

        total_software = sum(sw.size for sw in self.installed_software if sw.is_installed)
        total_files = sum(f.size for f in self.files)
        used_space = total_software + total_files

        if used_space + update_size > self.hard_disk.capacity:
            free = self.hard_disk.capacity - used_space
            raise InsufficientSpaceError(f"Недостаточно места. Нужно: {update_size}ГБ, свободно: {free}ГБ")

        update_file = File(f"os_update_{new_version}", update_size, "system_update")
        self.files.append(update_file)

        old_version = self.os_version
        self.os_version = new_version

        for sw in self.installed_software:
            if sw.is_os and sw.is_installed:
                sw.version = new_version

        self._notify("os_updated", {"old": old_version, "new": new_version})
        self._notify("storage_updated", self.get_storage_info())
        return f"ОС обновлена с {old_version} до {new_version}"

    # === Информация о системе ===
    def get_system_info(self) -> Dict[str, Any]:
        total_ram = sum(r.size for r in self.ram)
        total_software = sum(sw.size for sw in self.installed_software if sw.is_installed)
        total_files = sum(f.size for f in self.files)

        return {
            "name": self.name,
            "status": "включен" if self.is_powered_on else "выключен",
            "os": f"{self.os_name} {self.os_version}" if self.os_name else "не установлена",
            "components": {
                "cpu": self.cpu.get_info() if self.cpu else None,
                "motherboard": self.motherboard.get_info() if self.motherboard else None,
                "ram": [r.get_info() for r in self.ram],
                "total_ram": total_ram,
                "video_card": self.video_card.get_info() if self.video_card else None,
                "hard_disk": self.hard_disk.get_info() if self.hard_disk else None,
                "power_supply": self.power_supply.get_info() if self.power_supply else None
            },
            "peripherals": self.get_connected_peripherals(),
            "storage": self.get_storage_info(),
            "software_count": len(self.list_installed_software()),
            "files_count": len(self.files),
            "power_consumption": self._calculate_power_consumption()
        }

    def get_compatibility_report(self) -> Dict[str, Any]:
        report = {
            "compatible": True,
            "issues": [],
            "warnings": [],
            "details": {}
        }

        if self.cpu and self.motherboard:
            if self.cpu.socket != self.motherboard.socket:
                report["compatible"] = False
                report["issues"].append(
                    f"Сокет процессора {self.cpu.socket.value} несовместим "
                    f"с сокетом материнской платы {self.motherboard.socket.value}"
                )

        if self.motherboard and self.ram:
            supported = [t.value for t in self.motherboard.supported_ram_types]
            for ram in self.ram:
                if ram.ram_type.value not in supported:
                    report["compatible"] = False
                    report["issues"].append(f"Тип памяти {ram.ram_type.value} не поддерживается")
                    break

        if self.power_supply:
            total_power = self._calculate_power_consumption()
            if self.power_supply.wattage < total_power:
                report["compatible"] = False
                report["issues"].append(f"Мощность БП ({self.power_supply.wattage}Вт) недостаточна")
            elif self.power_supply.wattage < total_power * 1.2:
                report["warnings"].append(f"БП работает на пределе, запас 20% не обеспечен")

        report["details"]["power_consumption"] = self._calculate_power_consumption()
        report["details"]["ram_total"] = sum(r.size for r in self.ram)
        if self.motherboard:
            report["details"]["ram_max"] = self.motherboard.max_ram_size
            report["details"]["ram_slots"] = f"{len(self.ram)}/{self.motherboard.ram_slots}"

        return report

    def get_components_list(self) -> Dict[str, List]:
        """Список доступных компонентов."""
        motherboards = [
            Motherboard("ASUS PRIME B660M", "ASUS", 30, 8000, SocketType.LGA1700, Chipset.B660, [RAMType.DDR4], 128, 4),
            Motherboard("MSI PRO Z690-A", "MSI", 35, 12000, SocketType.LGA1700, Chipset.Z690,
                        [RAMType.DDR4, RAMType.DDR5], 128, 4),
            Motherboard("Gigabyte B650 AORUS", "Gigabyte", 30, 10000, SocketType.AM5, Chipset.B650, [RAMType.DDR5], 128,
                        4),
        ]

        cpus = [
            CPU("Intel Core i5-12400", "Intel", 65, 15000, SocketType.LGA1700, 6, 2.5),
            CPU("Intel Core i7-13700K", "Intel", 125, 35000, SocketType.LGA1700, 16, 3.4),
            CPU("AMD Ryzen 7 5800X", "AMD", 105, 25000, SocketType.AM4, 8, 3.8),
        ]

        ram_modules = [
            RAM("Kingston DDR4 16GB", "Kingston", 5, 5000, RAMType.DDR4, 16),
            RAM("Kingston DDR4 32GB", "Kingston", 5, 10000, RAMType.DDR4, 32),
            RAM("Corsair DDR5 16GB", "Corsair", 5, 8000, RAMType.DDR5, 16),
        ]

        gpus = [
            VideoCard("NVIDIA RTX 3060", "NVIDIA", 170, 30000, 12, "GDDR6"),
            VideoCard("NVIDIA RTX 4070", "NVIDIA", 200, 60000, 12, "GDDR6X"),
        ]

        hdds = [
            HardDisk("Samsung 980 512GB", "Samsung", 10, 7000, 512),
            HardDisk("Samsung 980 1TB", "Samsung", 10, 12000, 1024),
        ]

        psus = [
            PowerSupply("Corsair CV650", "Corsair", 0, 5000, 650),
            PowerSupply("Corsair RM750", "Corsair", 0, 9000, 750),
        ]

        return {
            "motherboard": motherboards,
            "cpu": cpus,
            "ram": ram_modules,
            "gpu": gpus,
            "hdd": hdds,
            "psu": psus
        }