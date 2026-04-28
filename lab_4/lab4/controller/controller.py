"""
Контроллер - связь между Model и View.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, Any, List

from model.computer import Computer, Software
from model.components import Monitor, Keyboard, Mouse, ConnectionType


class ComputerController:
    """Контроллер для управления компьютером."""

    def __init__(self, computer: Computer):
        self.computer = computer
        self.view = None

    def register_view(self, view):
        self.view = view
        self.computer.add_observer(view)

    # === Питание ===
    def power_on(self):
        try:
            result = self.computer.power_on()
            if self.view:
                self.view.add_to_log(result)
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))

    def power_off(self):
        try:
            result = self.computer.power_off()
            if self.view:
                self.view.add_to_log(result)
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))

    # === ПО ===
    def install_software(self):
        if not self.view:
            return
        name = self.view.soft_name.get()
        version = self.view.soft_version.get()
        size_str = self.view.soft_size.get()
        is_os = self.view.is_os_var.get()

        if not name or not version or not size_str:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        try:
            size = int(size_str)
            sw = Software(name, version, size, is_os)
            result = self.computer.install_software(sw)
            self.view.add_to_log(result)
            self.view.soft_name.delete(0, tk.END)
            self.view.soft_version.delete(0, tk.END)
            self.view.soft_size.delete(0, tk.END)
            self.view.is_os_var.set(False)
        except ValueError:
            messagebox.showerror("Ошибка", "Размер должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def uninstall_software(self):
        if not self.view:
            return
        selected = self.view.soft_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите ПО")
            return
        name = self.view.soft_tree.item(selected[0])['values'][0]
        try:
            result = self.computer.uninstall_software(name)
            self.view.add_to_log(result)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def list_installed_software(self) -> List[Dict]:
        return self.computer.list_installed_software()

    # === Файлы ===
    def save_file(self):
        if not self.view:
            return
        filename = self.view.filename_entry.get()
        size_str = self.view.filesize_entry.get()
        file_type = self.view.file_type_combo.get()

        if not filename or not size_str:
            messagebox.showerror("Ошибка", "Заполните поля")
            return
        try:
            size = int(size_str)
            result = self.computer.save_file(filename, size, file_type)
            self.view.add_to_log(result)
            self.view.filename_entry.delete(0, tk.END)
            self.view.filesize_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Размер должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_file(self):
        if not self.view:
            return
        selected = self.view.files_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите файл")
            return
        filename = self.view.files_tree.item(selected[0])['values'][0]
        try:
            result = self.computer.delete_file(filename)
            self.view.add_to_log(result)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def list_files(self) -> List[Dict]:
        return self.computer.list_files()

    # === Периферия ===
    def connect_peripheral(self, device_type: str) -> str:
        if device_type == "monitor":
            device = Monitor("LG UltraGear", "LG", 30, 20000, 27, "2560x1440", ConnectionType.HDMI, 144)
        elif device_type == "keyboard":
            device = Keyboard("Logitech G413", "Logitech", 2, 3000, "ANSI", ConnectionType.USB, False)
        else:
            device = Mouse("Logitech G502", "Logitech", 2, 4000, 25600, ConnectionType.USB, False)
        return self.computer.connect_peripheral(device)

    def disconnect_peripheral(self, device_type: str):
        try:
            result = self.computer.disconnect_peripheral(device_type)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))

    # === ОС ===
    def update_os(self):
        if not self.view:
            return
        version = self.view.os_version_entry.get()
        size_str = self.view.os_size_entry.get()
        if not version:
            messagebox.showerror("Ошибка", "Введите версию")
            return
        try:
            size = int(size_str)
            result = self.computer.update_os(version, size)
            self.view.add_to_log(result)
            self.view.os_version_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Ошибка", "Размер должен быть числом")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def get_available_components(self):
        """Получить список доступных компонентов."""
        return self.computer.get_components_list()

    def install_motherboard(self, motherboard):
        try:
            result = self.computer.install_motherboard(motherboard)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e

    def install_cpu(self, cpu):
        try:
            result = self.computer.install_cpu(cpu)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e

    def add_ram(self, ram):
        try:
            result = self.computer.add_ram(ram)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e

    def remove_ram(self, index):
        try:
            result = self.computer.remove_ram(index)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e

    def install_gpu(self, gpu):
        try:
            result = self.computer.install_video_card(gpu)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e

    def install_hdd(self, hdd):
        try:
            result = self.computer.install_hard_disk(hdd)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e

    def install_psu(self, psu):
        try:
            result = self.computer.install_power_supply(psu)
            if self.view:
                self.view.add_to_log(result)
                self.view.update_display()
            return result
        except Exception as e:
            if self.view:
                messagebox.showerror("Ошибка", str(e))
            raise e


    # === Информация ===
    def get_system_info(self) -> Dict[str, Any]:
        return self.computer.get_system_info()