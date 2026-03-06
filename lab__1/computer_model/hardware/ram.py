
from hardware.component import Component
from exceptions import InvalidDataError

class RAM(Component):
    """RAM class"""
    def __init__(self, name: str, manufacturer: str, power_consumption: float,
                 size: int, memory_type: str, frequency: int):
        super().__init__(name, manufacturer, power_consumption)
        self._size: int = size
        self._memory_type: str = memory_type
        self._frequency: int = frequency

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int):
        if value <= 0:
            raise InvalidDataError("RAM size must be positive.")
        self._size = value

    @property
    def memory_type(self) -> str:
        return self._memory_type

    @memory_type.setter
    def memory_type(self, value: str):
        if not value:
            raise InvalidDataError("Memory type cannot be empty.")
        self._memory_type = value

    @property
    def frequency(self) -> int:
        return self._frequency

    def __str__(self) -> str:
        status = "ЗАНЯТ" if self._is_busy else "СВОБОДЕН"
        return f"ОЗУ: {self._name} {self._size}ГБ {self._memory_type} @{self._frequency}МГц ({self._power_consumption}Вт) [{status}]"