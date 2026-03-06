from exceptions import InvalidDataError


class Program:
    """Program class"""
    def __init__(self, name: str, ram_required: float, cpu_cores_required: int,
                 vram_required: float = 0, storage_required: float = 0):
        self._name: str = name
        self._ram_required: float = ram_required
        self._cpu_cores_required: int = cpu_cores_required
        self._vram_required: float = vram_required
        self._storage_required: float = storage_required

    @property
    def name(self) -> str:
        return self._name

    @property
    def ram_required(self) -> float:
        return self._ram_required

    @property
    def cpu_cores_required(self) -> int:
        return self._cpu_cores_required

    @property
    def vram_required(self) -> float:
        return self._vram_required

    @property
    def storage_required(self) -> float:
        return self._storage_required

    def __str__(self) -> str:
        return f"Программа: {self._name} (ОЗУ:{self._ram_required}ГБ CPU:{self._cpu_cores_required} ядер VRAM:{self._vram_required}ГБ)"