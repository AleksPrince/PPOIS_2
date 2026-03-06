class ComputerError(Exception):
    """Базовое исключение для всех ошибок компьютера"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg


class CompatibilityError(ComputerError):
    """Ошибка совместимости компонентов"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg


class PowerError(ComputerError):
    """Ошибка питания (не хватает мощности)"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg


class ResourceBusyError(ComputerError):
    """Ресурс уже используется"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg


class ComputerOffError(ComputerError):
    """Компьютер выключен"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg


class ResourceNotFoundError(ComputerError):
    """Компонент не найден"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg


class InvalidDataError(Exception):
    """Неверный формат данных"""
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg: str = msg