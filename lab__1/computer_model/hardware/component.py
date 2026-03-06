from abc import ABC
from exceptions import InvalidDataError


class Component(ABC):
    """Base class for all hardware components"""
    def __init__(self, name: str, manufacturer: str, power_consumption: float):
        self._name: str = name
        self._manufacturer: str = manufacturer
        self._power_consumption: float = power_consumption
        self._is_busy: bool = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise InvalidDataError("Name cannot be empty.")
        self._name = value

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @manufacturer.setter
    def manufacturer(self, value: str):
        if not value:
            raise InvalidDataError("Manufacturer cannot be empty.")
        self._manufacturer = value

    @property
    def power_consumption(self) -> float:
        return self._power_consumption

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @is_busy.setter
    def is_busy(self, value: bool):
        if not isinstance(value, bool):
            raise InvalidDataError("is_busy must be a boolean.")
        self._is_busy = value

    def __repr__(self) -> str:
        status = "[ЗАНЯТ]" if self._is_busy else "[СВОБОДЕН]"
        return f"{self.__class__.__name__}: {self._name} ({self._manufacturer}) {self._power_consumption}Вт {status}"