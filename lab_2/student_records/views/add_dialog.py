import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from controllers.student_controller import StudentController


class AddStudentDialog(tk.Toplevel):
    """Диалог добавления нового студента"""

    def __init__(self, parent, controller: StudentController):
        super().__init__(parent)
        self.controller = controller
        self.result: Optional[dict] = None

        self.title("Добавление студента")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # Центрируем окно
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        self._setup_ui()
        self._bind_events()

    def _setup_ui(self):
        """Создание интерфейса диалога"""
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Поля ввода
        fields = [
            ("ФИО студента:", "full_name"),
            ("Курс:", "course"),
            ("Группа:", "group"),
            ("Общее число работ:", "total_works"),
            ("Количество выполненных работ:", "completed_works"),
            ("Язык программирования:", "programming_language")
        ]

        self.entries = {}

        for i, (label, field) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=5)

            if field in ['course', 'total_works', 'completed_works']:
                # Для числовых полей используем Spinbox
                var = tk.StringVar()
                if field == 'course':
                    entry = ttk.Spinbox(main_frame, from_=1, to=6, textvariable=var, width=30)
                else:
                    entry = ttk.Spinbox(main_frame, from_=0, to=100, textvariable=var, width=30)
                self.entries[field] = var
                entry.grid(row=i, column=1, sticky=tk.W, pady=5, padx=5)
            else:
                # Текстовые поля
                var = tk.StringVar()
                entry = ttk.Entry(main_frame, textvariable=var, width=30)
                self.entries[field] = var
                entry.grid(row=i, column=1, sticky=tk.W, pady=5, padx=5)

        # Подсказка
        ttk.Label(main_frame, text="Все поля обязательны для заполнения",
                  foreground="gray").grid(row=len(fields), column=0, columnspan=2, pady=10)

        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Добавить", command=self._on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.destroy).pack(side=tk.LEFT, padx=5)

        # Настройка весов для растяжения
        main_frame.columnconfigure(1, weight=1)

    def _bind_events(self):
        """Привязка событий"""
        self.bind('<Return>', lambda e: self._on_ok())
        self.bind('<Escape>', lambda e: self.destroy())

    def _on_ok(self):
        """Обработка нажатия OK"""
        # Сбор данных
        data = {}
        errors = []

        # Проверка заполненности
        for field, var in self.entries.items():
            value = var.get().strip()
            if not value:
                errors.append(f"Поле '{field}' обязательно для заполнения")
            else:
                data[field] = value

        if errors:
            messagebox.showerror("Ошибка", "\n".join(errors))
            return

        # Преобразование типов
        try:
            data['course'] = int(data['course'])
            data['total_works'] = int(data['total_works'])
            data['completed_works'] = int(data['completed_works'])
        except ValueError:
            messagebox.showerror("Ошибка", "Курс и количество работ должны быть числами")
            return

        # Дополнительная валидация
        if data['completed_works'] > data['total_works']:
            messagebox.showerror("Ошибка",
                                 "Количество выполненных работ не может превышать общее число")
            return

        self.result = data
        self.destroy()