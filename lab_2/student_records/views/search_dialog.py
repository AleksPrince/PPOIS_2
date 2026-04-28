import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Dict, Any
from models.student import Student
from controllers.student_controller import StudentController


class SearchResultsTable:
    """Таблица результатов поиска с пагинацией"""

    def __init__(self, parent, controller: StudentController):
        self.parent = parent
        self.controller = controller
        self.current_page = 1
        self.page_size = 10
        self.page_sizes = [5, 10, 20, 50]
        self.total_records = 0
        self.total_pages = 1
        self.all_results: List[Student] = []

        self._setup_ui()

    def _setup_ui(self):
        """Создание интерфейса таблицы"""
        # Основной фрейм
        self.main_frame = ttk.LabelFrame(self.parent, text="Результаты поиска")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Фрейм для таблицы
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Treeview
        columns = ('full_name', 'course', 'group', 'total_works',
                   'completed_works', 'programming_language')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)

        # Заголовки
        self.tree.heading('full_name', text='ФИО')
        self.tree.heading('course', text='Курс')
        self.tree.heading('group', text='Группа')
        self.tree.heading('total_works', text='Всего работ')
        self.tree.heading('completed_works', text='Выполнено')
        self.tree.heading('programming_language', text='Язык')

        # Ширина колонок
        self.tree.column('full_name', width=200)
        self.tree.column('course', width=50)
        self.tree.column('group', width=80)
        self.tree.column('total_works', width=80)
        self.tree.column('completed_works', width=80)
        self.tree.column('programming_language', width=100)

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

        # Пагинация
        pagination_frame = ttk.Frame(self.main_frame)
        pagination_frame.pack(fill=tk.X, padx=5, pady=5)

        # Информация
        self.info_label = ttk.Label(pagination_frame, text="Найдено: 0")
        self.info_label.pack(side=tk.LEFT)

        # Навигация
        nav_frame = ttk.Frame(pagination_frame)
        nav_frame.pack(side=tk.RIGHT)

        self.first_btn = ttk.Button(nav_frame, text="|<", width=3, command=self._first_page)
        self.first_btn.pack(side=tk.LEFT, padx=2)

        self.prev_btn = ttk.Button(nav_frame, text="<", width=3, command=self._prev_page)
        self.prev_btn.pack(side=tk.LEFT, padx=2)

        self.page_label = ttk.Label(nav_frame, text="Стр. 1/1")
        self.page_label.pack(side=tk.LEFT, padx=5)

        self.next_btn = ttk.Button(nav_frame, text=">", width=3, command=self._next_page)
        self.next_btn.pack(side=tk.LEFT, padx=2)

        self.last_btn = ttk.Button(nav_frame, text=">|", width=3, command=self._last_page)
        self.last_btn.pack(side=tk.LEFT, padx=2)

        # Размер страницы
        ttk.Label(pagination_frame, text="Показывать:").pack(side=tk.RIGHT, padx=5)
        self.page_size_combo = ttk.Combobox(pagination_frame, values=self.page_sizes,
                                            width=5, state='readonly')
        self.page_size_combo.set(self.page_size)
        self.page_size_combo.pack(side=tk.RIGHT)
        self.page_size_combo.bind('<<ComboboxSelected>>', self._on_page_size_change)

    def _update_navigation(self):
        """Обновление навигации"""
        self.info_label.config(text=f"Найдено: {self.total_records}")
        self.page_label.config(text=f"Стр. {self.current_page}/{self.total_pages}")

        self.first_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.prev_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)
        self.last_btn.config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)

    def _display_current_page(self):
        """Отображение текущей страницы"""
        # Очистка
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not self.all_results:
            return

        start_idx = (self.current_page - 1) * self.page_size
        end_idx = min(start_idx + self.page_size, len(self.all_results))

        for student in self.all_results[start_idx:end_idx]:
            values = [
                student.full_name,
                student.course,
                student.group,
                student.total_works,
                student.completed_works,
                student.programming_language
            ]
            self.tree.insert('', tk.END, values=values)

        self._update_navigation()

    def _first_page(self):
        if self.current_page > 1:
            self.current_page = 1
            self._display_current_page()

    def _prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self._display_current_page()

    def _next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._display_current_page()

    def _last_page(self):
        if self.current_page < self.total_pages:
            self.current_page = self.total_pages
            self._display_current_page()

    def _on_page_size_change(self, event=None):
        new_size = int(self.page_size_combo.get())
        if new_size != self.page_size:
            self.page_size = new_size
            self.total_pages = max(1, (self.total_records + self.page_size - 1) // self.page_size)
            self.current_page = min(self.current_page, self.total_pages)
            self._display_current_page()

    def set_results(self, results: List[Student]):
        """Установка результатов поиска"""
        self.all_results = results
        self.total_records = len(results)
        self.total_pages = max(1, (self.total_records + self.page_size - 1) // self.page_size)
        self.current_page = 1
        self._display_current_page()


class SearchDialog(tk.Toplevel):
    """Диалог поиска записей"""

    def __init__(self, parent, controller: StudentController):
        super().__init__(parent)
        self.controller = controller
        self.search_criteria = {}

        self.title("Поиск записей")
        self.geometry("800x600")
        self.transient(parent)
        self.grab_set()

        # Центрируем окно
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self._setup_ui()
        self._load_unique_values()

    def _setup_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм с критериями поиска
        criteria_frame = ttk.LabelFrame(main_frame, text="Критерии поиска")
        criteria_frame.pack(fill=tk.X, padx=5, pady=5)

        # Создаем поля поиска
        self._create_search_fields(criteria_frame)

        # Кнопки поиска
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(button_frame, text="Найти", command=self._perform_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сбросить", command=self._reset_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Закрыть", command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Таблица результатов
        self.results_table = SearchResultsTable(main_frame, self.controller)

    def _create_search_fields(self, parent):
        """Создание полей для ввода критериев поиска"""
        # Используем сетку для размещения
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)

        # Поля поиска
        row = 0

        # По ФИО или группе
        ttk.Label(parent, text="ФИО:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.full_name_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.full_name_var, width=25).grid(row=row, column=1, sticky=tk.W, padx=5,
                                                                          pady=5)

        ttk.Label(parent, text="Группа:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.group_combo = ttk.Combobox(parent, values=[], width=15, state='readonly')
        self.group_combo.grid(row=row, column=3, sticky=tk.W, padx=5, pady=5)
        row += 1

        # По курсу или языку программирования
        ttk.Label(parent, text="Курс:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.course_combo = ttk.Combobox(parent, values=[], width=10, state='readonly')
        self.course_combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(parent, text="Язык программирования:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.lang_combo = ttk.Combobox(parent, values=[], width=15, state='readonly')
        self.lang_combo.grid(row=row, column=3, sticky=tk.W, padx=5, pady=5)
        row += 1

        # По количеству работ
        ttk.Label(parent, text="Всего работ:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.total_works_combo = ttk.Combobox(parent, values=[], width=10, state='readonly')
        self.total_works_combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(parent, text="Выполнено работ:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)
        self.completed_works_combo = ttk.Combobox(parent, values=[], width=10, state='readonly')
        self.completed_works_combo.grid(row=row, column=3, sticky=tk.W, padx=5, pady=5)
        row += 1

        # По невыполненным работам
        ttk.Label(parent, text="Невыполненных работ:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.incomplete_works_combo = ttk.Combobox(parent, values=[], width=10, state='readonly')
        self.incomplete_works_combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        # Диапазоны
        ttk.Label(parent, text="Диапазоны:").grid(row=row, column=2, sticky=tk.W, padx=5, pady=5)

        range_frame = ttk.Frame(parent)
        range_frame.grid(row=row, column=3, sticky=tk.W, padx=5, pady=5)

        ttk.Label(range_frame, text="Всего работ от:").pack(side=tk.LEFT)
        self.min_total_works_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.min_total_works_var, width=5).pack(side=tk.LEFT, padx=2)

        ttk.Label(range_frame, text="до:").pack(side=tk.LEFT)
        self.max_total_works_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.max_total_works_var, width=5).pack(side=tk.LEFT, padx=2)
        row += 1

        # Пустая строка
        ttk.Label(parent, text="").grid(row=row, column=0, pady=5)

    def _load_unique_values(self):
        """Загрузка уникальных значений для выпадающих списков"""
        # Загружаем значения
        groups = set()
        courses = set()
        languages = set()
        total_works = set()
        completed_works = set()

        for student in self.controller.get_all_students():
            groups.add(student.group)
            courses.add(str(student.course))
            languages.add(student.programming_language)
            total_works.add(str(student.total_works))
            completed_works.add(str(student.completed_works))

        # Устанавливаем значения
        self.group_combo['values'] = [''] + sorted(list(groups))
        self.course_combo['values'] = [''] + sorted(list(courses))
        self.lang_combo['values'] = [''] + sorted(list(languages))
        self.total_works_combo['values'] = [''] + sorted(list(total_works))
        self.completed_works_combo['values'] = [''] + sorted(list(completed_works))

        # Для невыполненных работ вычисляем возможные значения
        incomplete_values = set()
        for student in self.controller.get_all_students():
            incomplete_values.add(str(student.incomplete_works))
        self.incomplete_works_combo['values'] = [''] + sorted(list(incomplete_values))

        # Сбрасываем выбор
        self.group_combo.set('')
        self.course_combo.set('')
        self.lang_combo.set('')
        self.total_works_combo.set('')
        self.completed_works_combo.set('')
        self.incomplete_works_combo.set('')

    def _perform_search(self):
        """Выполнение поиска"""
        criteria = {}

        # Собираем критерии
        if self.full_name_var.get().strip():
            criteria['full_name'] = self.full_name_var.get().strip()

        if self.group_combo.get():
            criteria['group'] = self.group_combo.get()

        if self.course_combo.get():
            criteria['course'] = self.course_combo.get()

        if self.lang_combo.get():
            criteria['programming_language'] = self.lang_combo.get()

        if self.total_works_combo.get():
            criteria['total_works'] = self.total_works_combo.get()

        if self.completed_works_combo.get():
            criteria['completed_works'] = self.completed_works_combo.get()

        if self.incomplete_works_combo.get():
            criteria['incomplete_works'] = self.incomplete_works_combo.get()

        # Диапазоны
        if self.min_total_works_var.get().strip():
            criteria['min_total_works'] = self.min_total_works_var.get().strip()

        if self.max_total_works_var.get().strip():
            criteria['max_total_works'] = self.max_total_works_var.get().strip()

        # Выполняем поиск
        results = self.controller.search_students(criteria)
        self.results_table.set_results(results)

        # Обновляем статус
        if not results:
            messagebox.showinfo("Поиск", "Записей, соответствующих критериям, не найдено")

    def _reset_search(self):
        """Сброс критериев поиска"""
        self.full_name_var.set('')
        self.group_combo.set('')
        self.course_combo.set('')
        self.lang_combo.set('')
        self.total_works_combo.set('')
        self.completed_works_combo.set('')
        self.incomplete_works_combo.set('')
        self.min_total_works_var.set('')
        self.max_total_works_var.set('')

        # Очищаем результаты
        self.results_table.set_results([])