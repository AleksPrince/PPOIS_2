import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from controllers.student_controller import StudentController
from models.student import Student


class DeleteDialog(tk.Toplevel):
    """Диалог удаления записей"""

    def __init__(self, parent, controller: StudentController):
        super().__init__(parent)
        self.controller = controller
        self.deleted_count = None
        self.preview_results: List[Student] = []

        self.title("Удаление записей")
        self.geometry("700x600")
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

        # Предупреждение
        warning_frame = ttk.Frame(main_frame)
        warning_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(warning_frame,
                  text="⚠️ ВНИМАНИЕ! Удаление записей невозможно отменить!",
                  foreground="red",
                  font=('Arial', 12, 'bold')).pack()

        # Фрейм с критериями удаления
        criteria_frame = ttk.LabelFrame(main_frame, text="Критерии удаления")
        criteria_frame.pack(fill=tk.X, padx=5, pady=5)

        self._create_delete_fields(criteria_frame)

        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=10)

        ttk.Button(control_frame, text="Предварительный просмотр",
                   command=self._preview_delete).pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Сбросить критерии",
                   command=self._reset_criteria).pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text="Удалить найденные",
                   command=self._confirm_delete).pack(side=tk.RIGHT, padx=5)

        ttk.Button(control_frame, text="Отмена",
                   command=self.destroy).pack(side=tk.RIGHT, padx=5)

        # Фрейм с результатами предпросмотра
        preview_frame = ttk.LabelFrame(main_frame, text="Предпросмотр записей для удаления")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Таблица для предпросмотра
        self._create_preview_table(preview_frame)

        # Информационная строка
        self.info_label = ttk.Label(main_frame, text="")
        self.info_label.pack(fill=tk.X, padx=5, pady=5)

    def _create_delete_fields(self, parent):
        """Создание полей для ввода критериев удаления"""
        # Используем сетку для размещения
        parent.columnconfigure(1, weight=1)
        parent.columnconfigure(3, weight=1)

        row = 0

        # По ФИО или группе
        ttk.Label(parent, text="ФИО (содержит):").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
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
        row += 1

        # Диапазоны
        range_frame = ttk.Frame(parent)
        range_frame.grid(row=row, column=0, columnspan=4, sticky=tk.W, padx=5, pady=5)

        ttk.Label(range_frame, text="Диапазон всего работ:").pack(side=tk.LEFT)

        self.min_total_works_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.min_total_works_var, width=5).pack(side=tk.LEFT, padx=2)

        ttk.Label(range_frame, text="-").pack(side=tk.LEFT)

        self.max_total_works_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.max_total_works_var, width=5).pack(side=tk.LEFT, padx=2)

        ttk.Label(range_frame, text="  Выполнено:").pack(side=tk.LEFT, padx=(10, 2))

        self.min_completed_works_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.min_completed_works_var, width=5).pack(side=tk.LEFT, padx=2)

        ttk.Label(range_frame, text="-").pack(side=tk.LEFT)

        self.max_completed_works_var = tk.StringVar()
        ttk.Entry(range_frame, textvariable=self.max_completed_works_var, width=5).pack(side=tk.LEFT, padx=2)

    def _create_preview_table(self, parent):
        """Создание таблицы для предпросмотра"""
        # Создаем Treeview
        columns = ('full_name', 'course', 'group', 'total_works', 'completed_works', 'programming_language')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)

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
        vsb = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(parent, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Размещение
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

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
        self._reset_criteria()

    def _get_criteria(self) -> dict:
        """Сбор критериев из полей ввода"""
        criteria = {}

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

        if self.min_completed_works_var.get().strip():
            criteria['min_completed_works'] = self.min_completed_works_var.get().strip()

        if self.max_completed_works_var.get().strip():
            criteria['max_completed_works'] = self.max_completed_works_var.get().strip()

        return criteria

    def _preview_delete(self):
        """Предварительный просмотр записей для удаления"""
        criteria = self._get_criteria()

        if not criteria:
            messagebox.showwarning("Предупреждение",
                                   "Не указаны критерии для удаления.\nБудут показаны все записи.")

        # Выполняем поиск
        self.preview_results = self.controller.search_students(criteria)

        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполняем таблицу
        for student in self.preview_results:
            values = [
                student.full_name,
                student.course,
                student.group,
                student.total_works,
                student.completed_works,
                student.programming_language
            ]
            self.tree.insert('', tk.END, values=values)

        # Обновляем информацию
        count = len(self.preview_results)
        if count == 0:
            self.info_label.config(text="Записей для удаления не найдено", foreground="blue")
        else:
            self.info_label.config(text=f"Найдено записей для удаления: {count}",
                                   foreground="red" if count > 0 else "blue")

    def _reset_criteria(self):
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
        self.min_completed_works_var.set('')
        self.max_completed_works_var.set('')

        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.preview_results = []
        self.info_label.config(text="")

    def _confirm_delete(self):
        """Подтверждение удаления"""
        if not self.preview_results:
            messagebox.showwarning("Предупреждение",
                                   "Сначала выполните предварительный просмотр записей для удаления.")
            return

        count = len(self.preview_results)

        if count == 0:
            messagebox.showinfo("Удаление", "Нет записей для удаления.")
            return

        # Запрашиваем подтверждение
        result = messagebox.askyesno(
            "Подтверждение удаления",
            f"Вы действительно хотите удалить {count} записей?\n\n"
            "Это действие невозможно отменить!",
            icon='warning'
        )

        if result:
            # Выполняем удаление
            criteria = self._get_criteria()
            self.deleted_count = self.controller.delete_students(criteria)

            # Закрываем диалог
            self.destroy()