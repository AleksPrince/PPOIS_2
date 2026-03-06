from hardware.component import Component
from exceptions import InvalidDataError


class Motherboard(Component):
    """Motherboard class"""
    def __init__(self, name: str, manufacturer: str, power_consumption: float,
                 socket: str, memory_type: str, max_memory: int,
                 memory_slots: int, pcie_slots: int, form_factor: str):
        super().__init__(name, manufacturer, power_consumption)
        self._socket: str = socket
        self._memory_type: str = memory_type
        self._max_memory: int = max_memory
        self._memory_slots: int = memory_slots
        self._pcie_slots: int = pcie_slots
        self._form_factor: str = form_factor

    @property
    def socket(self) -> str:
        return self._socket

    @property
    def memory_type(self) -> str:
        return self._memory_type

    @property
    def max_memory(self) -> int:
        return self._max_memory

    @property
    def memory_slots(self) -> int:
        return self._memory_slots

    @property
    def pcie_slots(self) -> int:
        return self._pcie_slots

    def __str__(self) -> str:
        status = "ЗАНЯТ" if self._is_busy else "СВОБОДЕН"
        return f"Материнская плата: {self._name} [Сокет: {self._socket}] {self._memory_type} слотов:{self._memory_slots} ({self._power_consumption}Вт) [{status}]"