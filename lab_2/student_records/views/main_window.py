import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Optional
from models.student import Student
from controllers.student_controller import StudentController
from views.add_dialog import AddStudentDialog
from views.search_dialog import SearchDialog
from views.delete_dialog import DeleteDialog


class PaginatedTable:
    """Класс для управления постраничным выводом таблицы"""

    def __init__(self, parent, columns: List[tuple], controller: StudentController,
                 on_selection_change: Optional[callable] = None):
        self.parent = parent
        self.columns = columns  # (field, title, width)
        self.controller = controller
        self.on_selection_change = on_selection_change

        # Параметры пагинации
        self.current_page = 1
        self.page_size = 10
        self.page_sizes = [5, 10, 20, 50, 100]
        self.total_records = 0
        self.total_pages = 1
        self.all_data: List[Student] = []
        self.displayed_data: List[Student] = []

        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        """Создание элементов интерфейса"""
        # Основной фрейм
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Фрейм для таблицы
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Создаем Treeview
        self.tree = ttk.Treeview(table_frame, columns=[col[0] for col in self.columns],
                                 show='headings', selectmode='extended')

        # Настройка колонок
        for col_id, col_title, col_width in self.columns:
            self.tree.heading(col_id, text=col_title)
            self.tree.column(col_id, width=col_width, minwidth=50)

        # Скроллбары
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Размещение
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Фрейм для элементов управления пагинацией
        pagination_frame = ttk.Frame(self.main_frame)
        pagination_frame.pack(fill=tk.X, pady=5)

        # Информация о записях
        self.info_label = ttk.Label(pagination_frame, text="Записей: 0")
        self.info_label.pack(side=tk.LEFT, padx=5)

        # Выбор размера страницы
        ttk.Label(pagination_frame, text="Показывать:").pack(side=tk.LEFT, padx=5)
        self.page_size_combo = ttk.Combobox(pagination_frame, values=self.page_sizes,
                                            width=5, state='readonly')
        self.page_size_combo.set(self.page_size)
        self.page_size_combo.pack(side=tk.LEFT, padx=5)
        ttk.Label(pagination_frame, text="записей").pack(side=tk.LEFT)

        # Кнопки навигации
        nav_frame = ttk.Frame(pagination_frame)
        nav_frame.pack(side=tk.RIGHT)

        self.first_btn = ttk.Button(nav_frame, text="|<", width=3, command=self._first_page)
        self.first_btn.pack(side=tk.LEFT, padx=2)

        self.prev_btn = ttk.Button(nav_frame, text="<", width=3, command=self._prev_page)
        self.prev_btn.pack(side=tk.LEFT, padx=2)

        self.page_label = ttk.Label(nav_frame, text="Стр. 1/1")
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.next_btn = ttk.Button(nav_frame, text=">", width=3, command=self._next_page)
        self.next_btn.pack(side=tk.LEFT, padx=2)

        self.last_btn = ttk.Button(nav_frame, text=">|", width=3, command=self._last_page)
        self.last_btn.pack(side=tk.LEFT, padx=2)

        # Статусная строка
        self.status_label = ttk.Label(self.main_frame, text="Готово")
        self.status_label.pack(fill=tk.X, pady=2)

    def _bind_events(self):
        """Привязка событий"""
        self.page_size_combo.bind('<<ComboboxSelected>>', self._on_page_size_change)
        self.tree.bind('<<TreeviewSelect>>', self._on_select)

    def _on_select(self, event):
        """Обработка выбора записи"""
        if self.on_selection_change:
            selected = self.get_selected_items()
            self.on_selection_change(len(selected) > 0)

    def _on_page_size_change(self, event=None):
        """Изменение размера страницы"""
        new_size = int(self.page_size_combo.get())
        if new_size != self.page_size:
            self.page_size = new_size
            self.current_page = 1
            self.refresh()

    def _first_page(self):
        """Первая страница"""
        if self.current_page > 1:
            self.current_page = 1
            self._display_current_page()

    def _prev_page(self):
        """Предыдущая страница"""
        if self.current_page > 1:
            self.current_page -= 1
            self._display_current_page()

    def _next_page(self):
        """Следующая страница"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._display_current_page()

    def _last_page(self):
        """Последняя страница"""
        if self.current_page < self.total_pages:
            self.current_page = self.total_pages
            self._display_current_page()

    def _update_pagination_controls(self):
        """Обновление элементов управления пагинацией"""
        self.info_label.config(text=f"Записей: {self.total_records}")
        self.page_label.config(text=f"Стр. {self.current_page}/{self.total_pages}")

        # Активация/деактивация кнопок
        self.first_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)
        self.last_btn.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)

    def _display_current_page(self):
        """Отображение текущей страницы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.displayed_data:
            return

        # Вычисление индексов для текущей страницы
        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.displayed_data))

        # Заполнение таблицы
        for student in self.displayed_data[start_idx:end_idx]:
            values = [
                student.full_name,
                student.course,
                student.group,
                student.total_works,
                student.completed_works,
                student.programming_language
            ]
            self.tree.insert('', tk.END, values=values)

        self._update_pagination_controls()
        self.status_label.config(text=f"Показаны записи {start_idx + 1}-{end_idx} из {len(self.displayed_data)}")

    def set_data(self, data: List[Student]):
        """Установка данных для отображения"""
        self.all_data = data.copy()
        self.displayed_data = data.copy()
        self.total_records = len(data)
        self.total_pages = max(1, (self.total_records + self.page_size - 1) // self.page_size)
        self.current_page = min(self.current_page, self.total_pages)
        self._display_current_page()

    def refresh(self):
        """Обновление отображения"""
        self.set_data(self.all_data)

    def get_selected_items(self) -> List[int]:
        """Получение индексов выбранных элементов"""
        selection = self.tree.selection()
        if not selection:
            return []

        indices = []
        for item in selection:
            idx = self.tree.index(item)
            indices.append((self.current_page - 1) * self.page_size + idx)

        return indices

    def clear_selection(self):
        """Снятие выделения"""
        self.tree.selection_remove(self.tree.selection())

    def set_status(self, text: str):
        """Установка текста статуса"""
        self.status_label.config(text=text)


class MainWindow:
    """Главное окно приложения"""

    def __init__(self, root):
        self.root = root
        self.root.title("Учет студентов - Лабораторная работа №2")
        self.root.geometry("1000x600")

        self.controller = StudentController()
        self.controller.add_observer(self.on_model_changed)

        self._setup_menu()
        self._setup_toolbar()
        self._setup_main_area()
        self._setup_status_bar()

        # Загружаем пример данных
        self._load_sample_data()

    def _setup_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить из XML", command=self.load_from_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить в XML", command=self.save_to_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")

        # Меню Правка
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Добавить запись", command=self.add_record, accelerator="Ctrl+N")
        edit_menu.add_command(label="Поиск", command=self.search_records, accelerator="Ctrl+F")
        edit_menu.add_command(label="Удалить", command=self.delete_records, accelerator="Ctrl+D")

        # Меню Вид
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Обновить", command=self.refresh_view, accelerator="F5")

        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)

        # Привязка горячих клавиш
        self.root.bind('<Control-n>', lambda e: self.add_record())
        self.root.bind('<Control-f>', lambda e: self.search_records())
        self.root.bind('<Control-d>', lambda e: self.delete_records())
        self.root.bind('<Control-o>', lambda e: self.load_from_file())
        self.root.bind('<Control-s>', lambda e: self.save_to_file())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<F5>', lambda e: self.refresh_view())

    def _setup_toolbar(self):
        """Создание панели инструментов"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # Кнопки
        ttk.Button(toolbar, text="Добавить", command=self.add_record).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Поиск", command=self.search_records).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Удалить", command=self.delete_records).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="Загрузить", command=self.load_from_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Сохранить", command=self.save_to_file).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="Обновить", command=self.refresh_view).pack(side=tk.LEFT, padx=2)

    def _setup_main_area(self):
        """Создание основной области"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заголовок
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)

        ttk.Label(title_frame, text="Список студентов",
                  font=('Arial', 14, 'bold')).pack(side=tk.LEFT)

        self.record_count_label = ttk.Label(title_frame, text="")
        self.record_count_label.pack(side=tk.RIGHT)

        # Таблица с пагинацией
        columns = [
            ('full_name', 'ФИО студента', 250),
            ('course', 'Курс', 60),
            ('group', 'Группа', 100),
            ('total_works', 'Всего работ', 100),
            ('completed_works', 'Выполнено', 100),
            ('programming_language', 'Язык', 120)
        ]

        self.table = PaginatedTable(main_frame, columns, self.controller,
                                    self.on_selection_change)

    def _setup_status_bar(self):
        """Создание строки состояния"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(self.status_bar, text="Готово", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.file_label = ttk.Label(self.status_bar, text="", relief=tk.SUNKEN)
        self.file_label.pack(side=tk.RIGHT)

    def on_selection_change(self, has_selection: bool):
        """Обработка изменения выделения"""
        # Можно добавить логику при выделении записей
        pass

    def on_model_changed(self):
        """Обработка изменений в модели"""
        self.refresh_view()
        self.status_label.config(text="Данные обновлены")

    def refresh_view(self):
        """Обновление отображения"""
        students = self.controller.get_all_students()
        self.table.set_data(students)
        self.record_count_label.config(text=f"Всего записей: {len(students)}")

        # Обновление информации о файле
        current_file = self.controller.get_current_file()
        if current_file:
            self.file_label.config(text=f"Файл: {current_file}")
        else:
            self.file_label.config(text="")

    def add_record(self):
        """Добавление новой записи"""
        dialog = AddStudentDialog(self.root, self.controller)
        self.root.wait_window(dialog)

        if dialog.result:
            if self.controller.add_student(dialog.result):
                self.status_label.config(text="Запись успешно добавлена")
                self.refresh_view()
            else:
                messagebox.showerror("Ошибка", "Не удалось добавить запись")

    def search_records(self):
        """Поиск записей"""
        dialog = SearchDialog(self.root, self.controller)
        self.root.wait_window(dialog)

    def delete_records(self):
        """Удаление записей"""
        dialog = DeleteDialog(self.root, self.controller)
        self.root.wait_window(dialog)

        if dialog.deleted_count is not None:
            if dialog.deleted_count > 0:
                messagebox.showinfo("Удаление",
                                    f"Удалено записей: {dialog.deleted_count}")
                self.refresh_view()
            else:
                messagebox.showinfo("Удаление",
                                    "Записей для удаления не найдено")

    def load_from_file(self):
        """Загрузка данных из XML файла"""
        filepath = filedialog.askopenfilename(
            title="Выберите XML файл для загрузки",
            filetypes=[("XML файлы", "*.xml"), ("Все файлы", "*.*")]
        )

        if not filepath:
            return

        success, message = self.controller.load_from_file(filepath)

        if success:
            messagebox.showinfo("Загрузка", message)
            self.status_label.config(text=f"Загружено из {filepath}")
            self.refresh_view()
        else:
            messagebox.showerror("Ошибка загрузки", message)

    def save_to_file(self):
        """Сохранение данных в XML файл"""
        filepath = filedialog.asksaveasfilename(
            title="Сохранить как XML",
            defaultextension=".xml",
            filetypes=[("XML файлы", "*.xml"), ("Все файлы", "*.*")]
        )

        if not filepath:
            return

        if self.controller.save_to_file(filepath):
            messagebox.showinfo("Сохранение", "Данные успешно сохранены")
            self.status_label.config(text=f"Сохранено в {filepath}")
            self.file_label.config(text=f"Файл: {filepath}")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить данные")

    def show_about(self):
        """Отображение информации о программе"""
        about_text = """Лабораторная работа №2"""

        messagebox.showinfo("О программе", about_text)

    def _load_sample_data(self):
        """Загрузка примеров данных для демонстрации"""
        sample_students = [
            {"full_name": "Иванов Иван Иванович", "course": 2, "group": "421701",
             "total_works": 15, "completed_works": 12, "programming_language": "Python"},
            {"full_name": "Петров Петр Петрович", "course": 2, "group": "421702",
             "total_works": 12, "completed_works": 10, "programming_language": "Java"},
            {"full_name": "Сидорова Анна Михайловна", "course": 2, "group": "421703",
             "total_works": 20, "completed_works": 18, "programming_language": "C++"},
            {"full_name": "Козлов Дмитрий Сергеевич", "course": 1, "group": "521701",
             "total_works": 10, "completed_works": 8, "programming_language": "Python"},
            {"full_name": "Смирнова Елена Александровна", "course": 1, "group": "521702",
             "total_works": 15, "completed_works": 15, "programming_language": "JavaScript"},
            {"full_name": "Васильев Алексей Николаевич", "course": 1, "group": "521703",
             "total_works": 25, "completed_works": 20, "programming_language": "C#"},
            {"full_name": "Михайлова Ольга Викторовна", "course": 1, "group": "521704",
             "total_works": 12, "completed_works": 9, "programming_language": "PHP"},
            {"full_name": "Федоров Артем Игоревич", "course": 2, "group": "421701",
             "total_works": 20, "completed_works": 17, "programming_language": "Ruby"},
            {"full_name": "Николаева Татьяна Павловна", "course": 2, "group": "421702",
             "total_works": 15, "completed_works": 14, "programming_language": "Python"},
            {"full_name": "Александров Максим Денисович", "course": 2, "group": "421703",
             "total_works": 10, "completed_works": 7, "programming_language": "Java"},
        ]

        # Дублируем записи для создания большего количества
        for i in range(1):
            for student in sample_students[:10]:
                new_student = student.copy()
                new_student["full_name"] = f"{student['full_name']} {i + 1}"
                self.controller.add_student(new_student)

        self.refresh_view()