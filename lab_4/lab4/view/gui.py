"""
Графический интерфейс пользователя на tkinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, Any, Optional


class ComputerGUI:
    """Графический интерфейс пользователя."""

    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Модель компьютера")
        self.root.geometry("1100x650")

        self.controller.register_view(self)
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        """Создание всех виджетов."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.create_control_tab()
        self.create_components_tab()
        self.create_peripherals_tab()
        self.create_software_tab()
        self.create_storage_tab()
        self.create_log_tab()

    def create_control_tab(self):
        """Вкладка управления."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Управление")

        info_frame = ttk.LabelFrame(frame, text="Информация")
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.name_label = ttk.Label(info_frame, text="")
        self.name_label.pack(anchor=tk.W, padx=10, pady=2)

        self.status_label = ttk.Label(info_frame, text="")
        self.status_label.pack(anchor=tk.W, padx=10, pady=2)

        self.os_label = ttk.Label(info_frame, text="")
        self.os_label.pack(anchor=tk.W, padx=10, pady=2)

        power_frame = ttk.LabelFrame(frame, text="Питание")
        power_frame.pack(fill=tk.X, padx=10, pady=5)

        btn_frame = ttk.Frame(power_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Включить", command=self.controller.power_on).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Выключить", command=self.controller.power_off).pack(side=tk.LEFT, padx=5)

        os_frame = ttk.LabelFrame(frame, text="Обновление ОС")
        os_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(os_frame, text="Новая версия:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.os_version_entry = ttk.Entry(os_frame, width=30)
        self.os_version_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(os_frame, text="Размер (ГБ):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.os_size_entry = ttk.Entry(os_frame, width=30)
        self.os_size_entry.insert(0, "5")
        self.os_size_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(os_frame, text="Обновить ОС", command=self.controller.update_os).grid(row=2, column=0, columnspan=2,
                                                                                         pady=10)

    def create_components_tab(self):
        """Вкладка компонентов."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Компоненты")

        # Материнская плата
        mb_frame = ttk.LabelFrame(frame, text="Материнская плата")
        mb_frame.pack(fill=tk.X, padx=10, pady=5)
        self.mb_label = ttk.Label(mb_frame, text="")
        self.mb_label.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(mb_frame, text="Заменить", command=self.show_motherboard_selector).pack(side=tk.RIGHT, padx=10)

        # Процессор
        cpu_frame = ttk.LabelFrame(frame, text="Процессор")
        cpu_frame.pack(fill=tk.X, padx=10, pady=5)
        self.cpu_label = ttk.Label(cpu_frame, text="")
        self.cpu_label.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(cpu_frame, text="Заменить", command=self.show_cpu_selector).pack(side=tk.RIGHT, padx=10)

        # Оперативная память
        ram_frame = ttk.LabelFrame(frame, text="Оперативная память")
        ram_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.ram_tree = ttk.Treeview(ram_frame, columns=("name", "manufacturer", "type", "size"), show="headings",
                                     height=4)
        self.ram_tree.heading("name", text="Название")
        self.ram_tree.heading("manufacturer", text="Производитель")
        self.ram_tree.heading("type", text="Тип")
        self.ram_tree.heading("size", text="Размер (ГБ)")
        self.ram_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ram_buttons = ttk.Frame(ram_frame)
        ram_buttons.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(ram_buttons, text="Добавить модуль", command=self.show_ram_selector).pack(side=tk.LEFT, padx=2)
        ttk.Button(ram_buttons, text="Удалить выбранный", command=self.remove_ram).pack(side=tk.LEFT, padx=2)

        # Видеокарта
        gpu_frame = ttk.LabelFrame(frame, text="Видеокарта")
        gpu_frame.pack(fill=tk.X, padx=10, pady=5)
        self.gpu_label = ttk.Label(gpu_frame, text="")
        self.gpu_label.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(gpu_frame, text="Заменить", command=self.show_gpu_selector).pack(side=tk.RIGHT, padx=10)

        # Жесткий диск
        hdd_frame = ttk.LabelFrame(frame, text="Жесткий диск")
        hdd_frame.pack(fill=tk.X, padx=10, pady=5)
        self.hdd_label = ttk.Label(hdd_frame, text="")
        self.hdd_label.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(hdd_frame, text="Заменить", command=self.show_hdd_selector).pack(side=tk.RIGHT, padx=10)

        # Блок питания
        psu_frame = ttk.LabelFrame(frame, text="Блок питания")
        psu_frame.pack(fill=tk.X, padx=10, pady=5)
        self.psu_label = ttk.Label(psu_frame, text="")
        self.psu_label.pack(side=tk.LEFT, padx=10, pady=5)
        ttk.Button(psu_frame, text="Заменить", command=self.show_psu_selector).pack(side=tk.RIGHT, padx=10)

    def create_peripherals_tab(self):
        """Вкладка периферии."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Периферия")

        mon_frame = ttk.LabelFrame(frame, text="Монитор")
        mon_frame.pack(fill=tk.X, padx=10, pady=5)
        self.monitor_label = ttk.Label(mon_frame, text="Не подключен")
        self.monitor_label.pack(side=tk.LEFT, padx=10, pady=10)
        btn_frame1 = ttk.Frame(mon_frame)
        btn_frame1.pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(btn_frame1, text="Подключить", command=lambda: self._connect("monitor")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame1, text="Отключить", command=lambda: self._disconnect("monitor")).pack(side=tk.LEFT, padx=2)

        kb_frame = ttk.LabelFrame(frame, text="Клавиатура")
        kb_frame.pack(fill=tk.X, padx=10, pady=5)
        self.keyboard_label = ttk.Label(kb_frame, text="Не подключена")
        self.keyboard_label.pack(side=tk.LEFT, padx=10, pady=10)
        btn_frame2 = ttk.Frame(kb_frame)
        btn_frame2.pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(btn_frame2, text="Подключить", command=lambda: self._connect("keyboard")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame2, text="Отключить", command=lambda: self._disconnect("keyboard")).pack(side=tk.LEFT,
                                                                                                    padx=2)

        mouse_frame = ttk.LabelFrame(frame, text="Мышь")
        mouse_frame.pack(fill=tk.X, padx=10, pady=5)
        self.mouse_label = ttk.Label(mouse_frame, text="Не подключена")
        self.mouse_label.pack(side=tk.LEFT, padx=10, pady=10)
        btn_frame3 = ttk.Frame(mouse_frame)
        btn_frame3.pack(side=tk.RIGHT, padx=10, pady=10)
        ttk.Button(btn_frame3, text="Подключить", command=lambda: self._connect("mouse")).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame3, text="Отключить", command=lambda: self._disconnect("mouse")).pack(side=tk.LEFT, padx=2)

    def _connect(self, device_type: str):
        try:
            result = self.controller.connect_peripheral(device_type)
            self.add_to_log(result)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def _disconnect(self, device_type: str):
        try:
            result = self.controller.disconnect_peripheral(device_type)
            self.add_to_log(result)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def create_software_tab(self):
        """Вкладка программ."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Программы")

        install_frame = ttk.LabelFrame(frame, text="Установка ПО")
        install_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(install_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.soft_name = ttk.Entry(install_frame, width=20)
        self.soft_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(install_frame, text="Версия:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.soft_version = ttk.Entry(install_frame, width=15)
        self.soft_version.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(install_frame, text="Размер (ГБ):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.soft_size = ttk.Entry(install_frame, width=20)
        self.soft_size.grid(row=1, column=1, padx=5, pady=5)

        self.is_os_var = tk.BooleanVar()
        ttk.Checkbutton(install_frame, text="Это ОС", variable=self.is_os_var).grid(row=1, column=2, columnspan=2,
                                                                                    padx=5, pady=5)

        ttk.Button(install_frame, text="Установить", command=self.controller.install_software).grid(row=2, column=0,
                                                                                                    columnspan=4,
                                                                                                    pady=10)

        list_frame = ttk.LabelFrame(frame, text="Установленное ПО")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.soft_tree = ttk.Treeview(list_frame, columns=("name", "version", "size", "is_os", "date"), show="headings",
                                      height=8)
        self.soft_tree.heading("name", text="Название")
        self.soft_tree.heading("version", text="Версия")
        self.soft_tree.heading("size", text="Размер (ГБ)")
        self.soft_tree.heading("is_os", text="ОС")
        self.soft_tree.heading("date", text="Дата")
        self.soft_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(list_frame, text="Удалить", command=self.controller.uninstall_software).pack(pady=5)

    def create_storage_tab(self):
        """Вкладка хранилища."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Хранилище")

        info_frame = ttk.LabelFrame(frame, text="Информация о диске")
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.disk_label = ttk.Label(info_frame, text="")
        self.disk_label.pack(pady=5)

        self.disk_progress = ttk.Progressbar(info_frame, length=400, mode='determinate')
        self.disk_progress.pack(pady=5)

        self.disk_usage_label = ttk.Label(info_frame, text="")
        self.disk_usage_label.pack(pady=2)

        file_frame = ttk.LabelFrame(frame, text="Сохранение файлов")
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(file_frame, text="Имя файла:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.filename_entry = ttk.Entry(file_frame, width=25)
        self.filename_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(file_frame, text="Тип:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.file_type_combo = ttk.Combobox(file_frame, values=["document", "image", "video", "music"], width=15)
        self.file_type_combo.set("document")
        self.file_type_combo.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(file_frame, text="Размер (ГБ):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.filesize_entry = ttk.Entry(file_frame, width=25)
        self.filesize_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(file_frame, text="Сохранить", command=self.controller.save_file).grid(row=2, column=0, columnspan=4,
                                                                                         pady=10)

        files_list_frame = ttk.LabelFrame(frame, text="Файлы на диске")
        files_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.files_tree = ttk.Treeview(files_list_frame, columns=("name", "type", "size", "date"), show="headings",
                                       height=8)
        self.files_tree.heading("name", text="Имя")
        self.files_tree.heading("type", text="Тип")
        self.files_tree.heading("size", text="Размер (ГБ)")
        self.files_tree.heading("date", text="Дата")
        self.files_tree.column("name", width=200)
        self.files_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Button(files_list_frame, text="Удалить", command=self.controller.delete_file).pack(pady=5)

    def create_log_tab(self):
        """Вкладка логов."""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Лог")

        self.log_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Button(frame, text="Очистить", command=self.clear_log).pack(pady=5)

    def update_display(self, info: Dict[str, Any] = None):
        """Обновить отображение."""
        if info is None:
            info = self.controller.get_system_info()

        self.name_label.config(text=f"Имя: {info['name']}")
        self.status_label.config(text=f"Статус: {info['status'].upper()}")
        self.os_label.config(text=f"ОС: {info['os']}")

        # Материнская плата
        if info['components']['motherboard']:
            mb = info['components']['motherboard']
            self.mb_label.config(text=f"{mb['manufacturer']} {mb['name']} | {mb['chipset']}")
        else:
            self.mb_label.config(text="Не установлена")

        # Процессор
        if info['components']['cpu']:
            cpu = info['components']['cpu']
            self.cpu_label.config(
                text=f"{cpu['manufacturer']} {cpu['name']} | {cpu['cores']} ядер | {cpu['frequency']} ГГц")
        else:
            self.cpu_label.config(text="Не установлен")

        # ОЗУ
        for item in self.ram_tree.get_children():
            self.ram_tree.delete(item)
        for ram in info['components']['ram']:
            self.ram_tree.insert("", tk.END,
                                 values=(ram['name'], ram['manufacturer'], ram.get('type', 'N/A'), ram['size']))

        # Видеокарта
        if info['components']['video_card']:
            gpu = info['components']['video_card']
            self.gpu_label.config(text=f"{gpu['manufacturer']} {gpu['name']} | {gpu['memory_size']}ГБ")
        else:
            self.gpu_label.config(text="Не установлена")

        # Жесткий диск
        if info['components']['hard_disk']:
            hdd = info['components']['hard_disk']
            self.hdd_label.config(text=f"{hdd['manufacturer']} {hdd['name']} | {hdd['capacity']}ГБ")
        else:
            self.hdd_label.config(text="Не установлен")

        # Блок питания
        if info['components']['power_supply']:
            psu = info['components']['power_supply']
            self.psu_label.config(text=f"{psu['manufacturer']} {psu['name']} | {psu['wattage']}Вт")
        else:
            self.psu_label.config(text="Не установлен")

        # Периферия
        self.monitor_label.config(text="Подключен" if info['peripherals']['monitor'] else "Не подключен")
        self.keyboard_label.config(text="Подключена" if info['peripherals']['keyboard'] else "Не подключена")
        self.mouse_label.config(text="Подключена" if info['peripherals']['mouse'] else "Не подключена")

        # Хранилище
        storage = info['storage']
        if 'error' not in storage:
            total = storage['total']
            used = storage['used']
            percent = storage.get('usage_percent', 0)
            self.disk_label.config(text=f"Жесткий диск: {total} ГБ")
            self.disk_progress['value'] = percent
            self.disk_usage_label.config(text=f"Использовано: {used} ГБ из {total} ГБ ({percent:.1f}%)")

        # ПО
        for item in self.soft_tree.get_children():
            self.soft_tree.delete(item)
        for sw in self.controller.list_installed_software():
            self.soft_tree.insert("", tk.END,
                                  values=(sw['name'], sw['version'], sw['size'], "Да" if sw['is_os'] else "Нет",
                                          sw['installation_date']))

        # Файлы
        for item in self.files_tree.get_children():
            self.files_tree.delete(item)
        for file in self.controller.list_files():
            self.files_tree.insert("", tk.END, values=(file['name'], file['type'], file['size'], file['created_at']))

    def add_to_log(self, message: str):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def update(self, event: str, data: Any):
        self.add_to_log(f"Событие: {event}")
        self.update_display()

    def show_motherboard_selector(self):
        """Выбор материнской платы."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор материнской платы")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите материнскую плату:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(dialog, width=60, height=15)
        listbox.pack(padx=20, pady=10)

        components = self.controller.get_available_components()
        for mb in components['motherboard']:
            listbox.insert(tk.END, f"{mb.manufacturer} {mb.name} | {mb.chipset.value} | {mb.socket.value}")

        def select():
            selection = listbox.curselection()
            if selection:
                mb = components['motherboard'][selection[0]]
                try:
                    result = self.controller.install_motherboard(mb)
                    self.add_to_log(result)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Выбрать", command=select).pack(pady=10)

    def show_cpu_selector(self):
        """Выбор процессора."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор процессора")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите процессор:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(dialog, width=60, height=15)
        listbox.pack(padx=20, pady=10)

        components = self.controller.get_available_components()
        for cpu in components['cpu']:
            listbox.insert(tk.END, f"{cpu.manufacturer} {cpu.name} | {cpu.cores} ядер | {cpu.frequency} ГГц")

        def select():
            selection = listbox.curselection()
            if selection:
                cpu = components['cpu'][selection[0]]
                try:
                    result = self.controller.install_cpu(cpu)
                    self.add_to_log(result)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Выбрать", command=select).pack(pady=10)

    def show_ram_selector(self):
        """Выбор модуля ОЗУ."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор оперативной памяти")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите модуль памяти:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(dialog, width=60, height=15)
        listbox.pack(padx=20, pady=10)

        components = self.controller.get_available_components()
        for ram in components['ram']:
            listbox.insert(tk.END, f"{ram.manufacturer} {ram.name} | {ram.ram_type.value} | {ram.size}ГБ")

        def select():
            selection = listbox.curselection()
            if selection:
                ram = components['ram'][selection[0]]
                try:
                    result = self.controller.add_ram(ram)
                    self.add_to_log(result)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Добавить", command=select).pack(pady=10)

    def remove_ram(self):
        """Удалить выбранный модуль ОЗУ."""
        selected = self.ram_tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите модуль памяти")
            return
        index = self.ram_tree.index(selected[0])
        try:
            result = self.controller.remove_ram(index)
            self.add_to_log(result)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def show_gpu_selector(self):
        """Выбор видеокарты."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор видеокарты")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите видеокарту:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(dialog, width=60, height=15)
        listbox.pack(padx=20, pady=10)

        components = self.controller.get_available_components()
        for gpu in components['gpu']:
            listbox.insert(tk.END, f"{gpu.manufacturer} {gpu.name} | {gpu.memory_size}ГБ {gpu.memory_type}")

        def select():
            selection = listbox.curselection()
            if selection:
                gpu = components['gpu'][selection[0]]
                try:
                    result = self.controller.install_gpu(gpu)
                    self.add_to_log(result)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Выбрать", command=select).pack(pady=10)

    def show_hdd_selector(self):
        """Выбор жесткого диска."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор жесткого диска")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите жесткий диск:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(dialog, width=60, height=15)
        listbox.pack(padx=20, pady=10)

        components = self.controller.get_available_components()
        for hdd in components['hdd']:
            listbox.insert(tk.END, f"{hdd.manufacturer} {hdd.name} | {hdd.capacity}ГБ")

        def select():
            selection = listbox.curselection()
            if selection:
                hdd = components['hdd'][selection[0]]
                try:
                    result = self.controller.install_hdd(hdd)
                    self.add_to_log(result)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Выбрать", command=select).pack(pady=10)

    def show_psu_selector(self):
        """Выбор блока питания."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор блока питания")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Выберите блок питания:", font=("Arial", 12, "bold")).pack(pady=10)

        listbox = tk.Listbox(dialog, width=60, height=15)
        listbox.pack(padx=20, pady=10)

        components = self.controller.get_available_components()
        for psu in components['psu']:
            listbox.insert(tk.END, f"{psu.manufacturer} {psu.name} | {psu.wattage}Вт | {psu.efficiency}")

        def select():
            selection = listbox.curselection()
            if selection:
                psu = components['psu'][selection[0]]
                try:
                    result = self.controller.install_psu(psu)
                    self.add_to_log(result)
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Ошибка", str(e))

        ttk.Button(dialog, text="Выбрать", command=select).pack(pady=10)

    def run(self):
        self.root.mainloop()