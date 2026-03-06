from hardware.component import Component
from exceptions import InvalidDataError


class PowerSupply(Component):
    """Power Supply class"""
    def __init__(self, name: str, manufacturer: str, power_consumption: float, wattage: int):
        super().__init__(name, manufacturer, power_consumption)
        self._wattage: int = wattage

    @property
    def wattage(self) -> int:
        return self._wattage

    @wattage.setter
    def wattage(self, value: int):
        if value <= 0:
            raise InvalidDataError("Wattage must be positive.")
        self._wattage = value

    def __str__(self) -> str:
        status = "ЗАНЯТ" if self._is_busy else "СВОБОДЕН"
        return f"Блок питания: {self._name} {self._wattage}Вт ({self._power_consumption}Вт) [{status}]"