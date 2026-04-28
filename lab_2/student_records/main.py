#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#cd D:\AK\Лабораторные\2 курс\ППОИС\4 семестр\student_records
#coverage report -m


"""
Лабораторная работа №2
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Добавляем путь к проекту в sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from views.main_window import MainWindow


def center_window(window):
    """Центрирование окна на экране"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


def main():
    """Главная функция запуска приложения"""
    try:
        # Создаем корневое окно
        root = tk.Tk()

        # Устанавливаем заголовок
        root.title("Система учета студентов - Лабораторная работа №2 (Вариант 14)")

        # Устанавливаем минимальный размер окна
        root.minsize(1000, 700)

        # Устанавливаем иконку (если есть)
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'resources', 'icon.ico')
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        except:
            pass  # Игнорируем ошибки с иконкой

        # Создаем главное окно приложения
        app = MainWindow(root)

        # Центрируем окно на экране
        center_window(root)

        # Запускаем главный цикл обработки событий
        root.mainloop()

    except Exception as e:
        # В случае критической ошибки показываем сообщение
        messagebox.showerror("Критическая ошибка",
                             f"Произошла критическая ошибка при запуске приложения:\n\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()