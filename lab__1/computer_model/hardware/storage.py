from hardware.component import Component
from exceptions import InvalidDataError


class Storage(Component):
    """Storage class (HDD/SSD)"""
    def __init__(self, name: str, manufacturer: str, power_consumption: float,
                 capacity: int, storage_type: str, interface: str):
        super().__init__(name, manufacturer, power_consumption)
        self._capacity: int = capacity
        self._storage_type: str = storage_type
        self._interface: str = interface

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int):
        if value <= 0:
            raise InvalidDataError("Capacity must be positive.")
        self._capacity = value

    @property
    def storage_type(self) -> str:
        return self._storage_type

    @property
    def interface(self) -> str:
        return self._interface

    def __str__(self) -> str:
        status = "ЗАНЯТ" if self._is_busy else "СВОБОДЕН"
        return f"Накопитель: {self._name} {self._capacity}ГБ {self._storage_type} ({self._interface}) ({self._power_consumption}Вт) [{status}]"