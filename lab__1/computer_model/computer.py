from typing import List, Optional, Dict
from hardware.cpu import CPU
from hardware.ram import RAM
from hardware.gpu import GPU
from hardware.storage import Storage
from hardware.motherboard import Motherboard
from hardware.powersupply import PowerSupply
from software.program import Program
from software.task import Task, ComputerStatus
from exceptions import (
    CompatibilityError, PowerError, ResourceBusyError,
    ComputerOffError, ResourceNotFoundError
)


class Computer:
    """Main Computer class"""

    def __init__(self, name: str = "Мой ПК"):
        self._name: str = name
        self._status: ComputerStatus = ComputerStatus.OFF
        self._current_task: Optional[Task] = None

        # Components
        self._cpu: Optional[CPU] = None
        self._ram: List[RAM] = []
        self._gpu: List[GPU] = []
        self._storage: List[Storage] = []
        self._motherboard: Optional[Motherboard] = None
        self._psu: Optional[PowerSupply] = None

    # ===== PROPERTIES =====
    @property
    def name(self) -> str:
        return self._name

    @property
    def status(self) -> ComputerStatus:
        return self._status

    @property
    def status_name(self) -> str:

        return str(self._status)

    @property
    def cpu(self) -> Optional[CPU]:
        return self._cpu

    @property
    def ram(self) -> List[RAM]:
        return self._ram

    @property
    def gpu(self) -> List[GPU]:
        return self._gpu

    @property
    def storage(self) -> List[Storage]:
        return self._storage

    @property
    def motherboard(self) -> Optional[Motherboard]:
        return self._motherboard

    @property
    def psu(self) -> Optional[PowerSupply]:
        return self._psu

    @property
    def current_task(self) -> Optional[Task]:
        return self._current_task

    # ===== INSTALL COMPONENTS =====
    def install_motherboard(self, motherboard: Motherboard) -> str:
        """Install motherboard"""
        if self._motherboard:
            raise ResourceBusyError("Материнская плата уже установлена. Сначала удалите её.")

        if motherboard.is_busy:
            raise ResourceBusyError(f"Материнская плата {motherboard.name} занята в другом компьютере.")

        self._motherboard = motherboard
        motherboard.is_busy = True
        return f" Материнская плата {motherboard.name} установлена"

    def install_cpu(self, cpu: CPU) -> str:
        """Install CPU"""
        if not self._motherboard:
            raise CompatibilityError("Нельзя установить процессор без материнской платы.")

        if self._cpu:
            raise ResourceBusyError("Процессор уже установлен. Сначала удалите его.")

        if cpu.is_busy:
            raise ResourceBusyError(f"Процессор {cpu.name} занят в другом компьютере.")

        # Check socket compatibility
        if cpu.socket != self._motherboard.socket:
            raise CompatibilityError(
                f"Сокет процессора {cpu.socket} не совместим с сокетом материнской платы {self._motherboard.socket}"
            )

        self._cpu = cpu
        cpu.is_busy = True
        return f" Процессор {cpu.name} установлен"

    def install_ram(self, ram: RAM) -> str:
        """Install RAM"""
        if not self._motherboard:
            raise CompatibilityError("Нельзя установить ОЗУ без материнской платы.")

        if len(self._ram) >= self._motherboard.memory_slots:
            raise ResourceBusyError(f"Все {self._motherboard.memory_slots} слотов памяти заняты.")

        if ram.is_busy:
            raise ResourceBusyError(f"ОЗУ {ram.name} занята в другом компьютере.")

        # Check memory type compatibility
        if ram.memory_type != self._motherboard.memory_type:
            raise CompatibilityError(
                f"Тип памяти {ram.memory_type} не совместим с материнской платой ({self._motherboard.memory_type})"
            )

        # Check max memory
        total_ram = sum(r.size for r in self._ram) + ram.size
        if total_ram > self._motherboard.max_memory:
            raise CompatibilityError(
                f"Общий объём ОЗУ {total_ram}ГБ превышает максимум материнской платы ({self._motherboard.max_memory}ГБ)"
            )

        self._ram.append(ram)
        ram.is_busy = True
        return f" ОЗУ {ram.name} установлена"

    def install_gpu(self, gpu: GPU) -> str:
        """Install GPU"""
        if not self._motherboard:
            raise CompatibilityError("Нельзя установить видеокарту без материнской платы.")

        if len(self._gpu) >= self._motherboard.pcie_slots:
            raise ResourceBusyError(f"Все {self._motherboard.pcie_slots} слотов PCIe заняты.")

        if gpu.is_busy:
            raise ResourceBusyError(f"Видеокарта {gpu.name} занята в другом компьютере.")

        self._gpu.append(gpu)
        gpu.is_busy = True
        return f" Видеокарта {gpu.name} установлена"

    def install_storage(self, storage: Storage) -> str:
        """Install storage device"""
        if storage.is_busy:
            raise ResourceBusyError(f"Накопитель {storage.name} занят в другом компьютере.")

        self._storage.append(storage)
        storage.is_busy = True
        return f" Накопитель {storage.name} установлен"

    def install_psu(self, psu: PowerSupply) -> str:
        """Install power supply"""
        if self._psu:
            raise ResourceBusyError("Блок питания уже установлен. Сначала удалите его.")

        if psu.is_busy:
            raise ResourceBusyError(f"Блок питания {psu.name} занят в другом компьютере.")

        self._psu = psu
        psu.is_busy = True
        return f" Блок питания {psu.name} установлен"

    # ===== REMOVE COMPONENTS =====
    def remove_cpu(self) -> str:
        """Remove CPU"""
        if not self._cpu:
            raise ResourceNotFoundError("Процессор не установлен.")

        if self._status != ComputerStatus.OFF:
            raise ComputerOffError("Нельзя удалить процессор когда компьютер включён.")

        self._cpu.is_busy = False
        self._cpu = None
        return " Процессор удалён"

    def remove_ram(self, index: int = 0) -> str:
        """Remove RAM module"""
        if not self._ram:
            raise ResourceNotFoundError("ОЗУ не установлена.")

        if index < 0 or index >= len(self._ram):
            raise ResourceNotFoundError(f"Индекс {index} вне диапазона. Доступно: 0-{len(self._ram) - 1}")

        if self._status != ComputerStatus.OFF:
            raise ComputerOffError("Нельзя удалить ОЗУ когда компьютер включён.")

        ram = self._ram.pop(index)
        ram.is_busy = False
        return f" ОЗУ {ram.name} удалена"

    def remove_gpu(self, index: int = 0) -> str:
        """Remove GPU"""
        if not self._gpu:
            raise ResourceNotFoundError("Видеокарта не установлена.")

        if index < 0 or index >= len(self._gpu):
            raise ResourceNotFoundError(f"Индекс {index} вне диапазона. Доступно: 0-{len(self._gpu) - 1}")

        if self._status != ComputerStatus.OFF:
            raise ComputerOffError("Нельзя удалить видеокарту когда компьютер включён.")

        gpu = self._gpu.pop(index)
        gpu.is_busy = False
        return f" Видеокарта {gpu.name} удалена"

    def remove_storage(self, index: int = 0) -> str:
        """Remove storage device"""
        if not self._storage:
            raise ResourceNotFoundError("Накопитель не установлен.")

        if index < 0 or index >= len(self._storage):
            raise ResourceNotFoundError(f"Индекс {index} вне диапазона. Доступно: 0-{len(self._storage) - 1}")

        storage = self._storage.pop(index)
        storage.is_busy = False
        return f" Накопитель {storage.name} удалён"

    def remove_motherboard(self) -> str:
        """Remove motherboard"""
        if not self._motherboard:
            raise ResourceNotFoundError("Материнская плата не установлена.")

        if self._status != ComputerStatus.OFF:
            raise ComputerOffError("Нельзя удалить материнскую плату когда компьютер включён.")

        # Can't remove motherboard if other components are installed
        if self._cpu or self._ram or self._gpu:
            raise ResourceBusyError("Удалите все остальные компоненты перед удалением материнской платы.")

        self._motherboard.is_busy = False
        self._motherboard = None
        return " Материнская плата удалена"

    def remove_psu(self) -> str:
        """Remove power supply"""
        if not self._psu:
            raise ResourceNotFoundError("Блок питания не установлен.")

        if self._status != ComputerStatus.OFF:
            raise ComputerOffError("Нельзя удалить блок питания когда компьютер включён.")

        self._psu.is_busy = False
        self._psu = None
        return " Блок питания удалён"

    # ===== POWER MANAGEMENT =====
    def get_total_power_consumption(self) -> float:
        """Get total power consumption"""
        total = 0.0

        if self._cpu:
            total += self._cpu.power_consumption
        if self._motherboard:
            total += self._motherboard.power_consumption
        if self._psu:
            total += self._psu.power_consumption

        for ram in self._ram:
            total += ram.power_consumption
        for gpu in self._gpu:
            total += gpu.power_consumption
        for storage in self._storage:
            total += storage.power_consumption

        return total

    def power_on(self) -> str:
        """Turn on computer"""
        if self._status != ComputerStatus.OFF:
            raise ComputerOffError("Компьютер уже включён.")

        # Check required components
        if not self._motherboard:
            raise ResourceNotFoundError("Нельзя включить: нет материнской платы.")

        if not self._cpu:
            raise ResourceNotFoundError("Нельзя включить: нет процессора.")

        if not self._ram:
            raise ResourceNotFoundError("Нельзя включить: нет ОЗУ.")

        if not self._psu:
            raise ResourceNotFoundError("Нельзя включить: нет блока питания.")

        # Check power
        total_power = self.get_total_power_consumption()
        if total_power > self._psu.wattage:
            raise PowerError(
                f"Недостаточно питания: требуется {total_power}Вт, БП выдаёт {self._psu.wattage}Вт"
            )

        self._status = ComputerStatus.ON
        return " Компьютер включён"

    def power_off(self) -> str:
        """Turn off computer"""
        if self._status == ComputerStatus.OFF:
            return " Компьютер уже выключен"

        # If something is running, free resources
        if self._current_task:
            self._stop_current_task()

        self._status = ComputerStatus.OFF
        return " Компьютер выключен"

    def _stop_current_task(self):
        """Stop current task and free resources"""
        if not self._current_task:
            return

        # Free resources
        if self._cpu:
            self._cpu.is_busy = False

        for ram in self._ram:
            ram.is_busy = False

        for gpu in self._gpu:
            gpu.is_busy = False

        for storage in self._storage:
            storage.is_busy = False

        self._current_task = None

    # ===== RUN PROGRAMS =====
    def run_program(self, program: Program) -> str:
        """Run a program"""
        if self._status == ComputerStatus.OFF:
            raise ComputerOffError("Нельзя запустить программу: компьютер выключен.")

        if self._status == ComputerStatus.RUNNING:
            raise ResourceBusyError("Другая программа уже запущена.")

        # Check resources
        errors = []

        # RAM
        total_ram = sum(r.size for r in self._ram)
        if total_ram < program.ram_required:
            errors.append(f"ОЗУ: доступно {total_ram}ГБ, требуется {program.ram_required}ГБ")

        # CPU cores
        if self._cpu.cores < program.cpu_cores_required:
            errors.append(f"Ядра CPU: доступно {self._cpu.cores}, требуется {program.cpu_cores_required}")

        # VRAM
        if program.vram_required > 0:
            total_vram = sum(g.vram for g in self._gpu)
            if total_vram < program.vram_required:
                errors.append(f"VRAM: доступно {total_vram}ГБ, требуется {program.vram_required}ГБ")

        # Storage
        if program.storage_required > 0:
            total_storage = sum(s.capacity for s in self._storage)
            if total_storage < program.storage_required:
                errors.append(f"Накопитель: доступно {total_storage}ГБ, требуется {program.storage_required}ГБ")

        if errors:
            error_msg = "Недостаточно ресурсов:\n  " + "\n  ".join(errors)
            raise ResourceBusyError(error_msg)

        # Create task and occupy resources
        task = Task(program)
        task.cpu = self._cpu
        self._cpu.is_busy = True

        for ram in self._ram:
            task.add_ram(ram)
            ram.is_busy = True

        for gpu in self._gpu:
            task.add_gpu(gpu)
            gpu.is_busy = True

        for storage in self._storage:
            task.add_storage(storage)
            storage.is_busy = True

        task.status = ComputerStatus.RUNNING
        self._current_task = task
        self._status = ComputerStatus.RUNNING

        task.result = f"Программа '{program.name}' успешно запущена"
        return f" {task.result}"

    def stop_program(self) -> str:
        """Stop running program"""
        if not self._current_task:
            raise ResourceNotFoundError("Нет запущенных программ.")

        program_name = self._current_task.program.name
        self._stop_current_task()
        self._status = ComputerStatus.ON
        return f" Программа '{program_name}' остановлена"

    # ===== UTILITY METHODS =====
    def get_info(self) -> str:

        lines = [f" КОМПЬЮТЕР: {self._name}"]
        lines.append(f" Статус: {self.status_name}")
        lines.append("")

        if self._motherboard:
            lines.append(f"  {self._motherboard}")
        else:
            lines.append("   Материнская плата: не установлена")

        if self._cpu:
            lines.append(f"  {self._cpu}")
        else:
            lines.append("   Процессор: не установлен")

        if self._ram:
            total_ram = sum(r.size for r in self._ram)
            lines.append(f"   ОЗУ: {len(self._ram)} модулей (всего {total_ram}ГБ)")
            for i, ram in enumerate(self._ram):
                lines.append(f"    [{i}] {ram}")
        else:
            lines.append("   ОЗУ: не установлена")

        if self._gpu:
            total_vram = sum(g.vram for g in self._gpu)
            lines.append(f"   Видеокарты: {len(self._gpu)} шт. (всего {total_vram}ГБ VRAM)")
            for i, gpu in enumerate(self._gpu):
                lines.append(f"    [{i}] {gpu}")
        else:
            lines.append("   Видеокарта: не установлена")

        if self._storage:
            total_storage = sum(s.capacity for s in self._storage)
            lines.append(f"   Накопители: {len(self._storage)} шт. (всего {total_storage}ГБ)")
            for i, storage in enumerate(self._storage):
                lines.append(f"    [{i}] {storage}")
        else:
            lines.append("   Накопитель: не установлен")

        if self._psu:
            total_power = self.get_total_power_consumption()
            lines.append(f"   {self._psu}")
            lines.append(f"     Потребление: {total_power}Вт / {self._psu.wattage}Вт")
            if total_power > self._psu.wattage:
                lines.append("       ПРЕВЫШЕНИЕ МОЩНОСТИ!")
        else:
            lines.append("   Блок питания: не установлен")

        if self._current_task:
            lines.append("")
            lines.append(f" Текущая задача: {self._current_task}")

        return "\n".join(lines)

    def get_installed_components(self) -> Dict:
        """Get dictionary of installed components"""
        return {
            'cpu': [self._cpu] if self._cpu else [],
            'ram': self._ram,
            'gpu': self._gpu,
            'storage': self._storage,
            'motherboard': [self._motherboard] if self._motherboard else [],
            'psu': [self._psu] if self._psu else []
        }

    def __str__(self) -> str:
        """String representation"""
        return self.get_info()