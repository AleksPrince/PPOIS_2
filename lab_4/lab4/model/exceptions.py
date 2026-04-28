
class ComputerError(Exception):
    """Базовое исключение для ошибок компьютера."""
    pass


class ComponentNotFoundError(ComputerError):
    """Исключение при отсутствии компонента."""
    pass


class IncompatibleComponentError(ComputerError):
    """Исключение при несовместимости компонентов."""
    pass


class PowerSupplyError(ComputerError):
    """Исключение при проблемах с питанием."""
    pass


class InsufficientSpaceError(ComputerError):
    """Исключение при недостатке места."""
    pass