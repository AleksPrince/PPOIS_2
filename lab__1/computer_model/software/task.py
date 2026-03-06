from enum import Enum, auto
from typing import List, Optional
from hardware.cpu import CPU
from hardware.ram import RAM
from hardware.gpu import GPU
from hardware.storage import Storage
from exceptions import ResourceNotFoundError


class ComputerStatus(Enum):
    """Computer status enum"""
    OFF = auto()  # выключен
    ON = auto()  # включен
    RUNNING = auto()  # работает
    ERROR = auto()  # ошибка

    def __str__(self) -> str:
        names = {
            ComputerStatus.OFF: "ВЫКЛЮЧЕН",
            ComputerStatus.ON: "ВКЛЮЧЕН",
            ComputerStatus.RUNNING: "РАБОТАЕТ",
            ComputerStatus.ERROR: "ОШИБКА"
        }
        return names.get(self, "НЕИЗВЕСТНО")


class Task:
    """Task class - represents running program"""

    def __init__(self, program):
        from .program import Program
        if not isinstance(program, Program):
            raise ResourceNotFoundError("Task must be initialized with a Program object.")

        self._program = program
        self._status = ComputerStatus.OFF
        self._cpu: Optional[CPU] = None
        self._ram_modules: List[RAM] = []
        self._gpu_modules: List[GPU] = []
        self._storage_modules: List[Storage] = []
        self._result: Optional[str] = None

    @property
    def program(self):
        return self._program

    @property
    def status(self) -> ComputerStatus:
        return self._status

    @status.setter
    def status(self, value: ComputerStatus):
        self._status = value

    @property
    def cpu(self) -> Optional[CPU]:
        return self._cpu

    @cpu.setter
    def cpu(self, value: CPU):
        self._cpu = value

    @property
    def ram_modules(self) -> List[RAM]:
        return self._ram_modules

    def add_ram(self, ram: RAM):
        self._ram_modules.append(ram)

    @property
    def gpu_modules(self) -> List[GPU]:
        return self._gpu_modules

    def add_gpu(self, gpu: GPU):
        self._gpu_modules.append(gpu)

    @property
    def storage_modules(self) -> List[Storage]:
        return self._storage_modules

    def add_storage(self, storage: Storage):
        self._storage_modules.append(storage)

    @property
    def result(self) -> Optional[str]:
        return self._result

    @result.setter
    def result(self, value: str):
        self._result = value

    def __str__(self) -> str:
        cpu_name = self._cpu.name if self._cpu else "Нет"
        ram_count = len(self._ram_modules)
        gpu_count = len(self._gpu_modules)
        return (f"Задача: '{self._program.name}' | Статус: {self._status} | "
                f"CPU: {cpu_name} | ОЗУ: {ram_count} модулей | GPU: {gpu_count}")