from hardware.component import Component
from exceptions import InvalidDataError

class GPU(Component):
    """GPU class"""
    def __init__(self, name: str, manufacturer: str, power_consumption: float,
                 vram: int, frequency: int, interface: str):
        super().__init__(name, manufacturer, power_consumption)
        self._vram: int = vram
        self._frequency: int = frequency
        self._interface: str = interface

    @property
    def vram(self) -> int:
        return self._vram

    @vram.setter
    def vram(self, value: int):
        if value <= 0:
            raise InvalidDataError("VRAM must be positive.")
        self._vram = value

    @property
    def frequency(self) -> int:
        return self._frequency

    @property
    def interface(self) -> str:
        return self._interface

    def __str__(self) -> str:
        status = "ЗАНЯТ" if self._is_busy else "СВОБОДЕН"
        return f"Видеокарта: {self._name} {self._vram}ГБ VRAM @{self._frequency}МГц ({self._power_consumption}Вт) [{status}]"