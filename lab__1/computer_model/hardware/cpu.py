from hardware.component import Component
from exceptions import InvalidDataError


class CPU(Component):
    """CPU class"""
    def __init__(self, name: str, manufacturer: str, socket: str, cores: int, power_consumption: float):
        super().__init__(name, manufacturer, power_consumption)
        self._socket: str = socket
        self._cores: int = cores
        self._frequency: float = 3.0

    @property
    def socket(self) -> str:
        return self._socket

    @socket.setter
    def socket(self, value: str):
        if not value:
            raise InvalidDataError("Socket cannot be empty.")
        self._socket = value

    @property
    def cores(self) -> int:
        return self._cores

    @cores.setter
    def cores(self, value: int):
        if value <= 0:
            raise InvalidDataError("Cores count must be positive.")
        self._cores = value

    @property
    def frequency(self) -> float:
        return self._frequency

    @frequency.setter
    def frequency(self, value: float):
        if value <= 0:
            raise InvalidDataError("Frequency must be positive.")
        self._frequency = value

    def __str__(self) -> str:
        status = "ЗАНЯТ" if self._is_busy else "СВОБОДЕН"
        return f"Процессор: {self._name} [Сокет: {self._socket}] {self._cores} ядер @{self._frequency}ГГц ({self._power_consumption}Вт) [{status}]"