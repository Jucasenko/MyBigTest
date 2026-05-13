import json
import random
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List


# --- ЛОГИКА РАБОТЫ С ДАННЫМИ (Вынесено в отдельный класс) ---
class TaskDataManager:

    @staticmethod
    def load_history() -> List[Dict[str, str]]:
        """Загрузка истории с обработкой конкретных исключений."""
        try:
            with open("task_history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except FileNotFoundError:
            # Отсутствие файла при первом запуске — штатная ситуация
            return []
        except json.JSONDecodeError:
            # Обработка поврежденного JSON
            messagebox.showwarning(
                "Внимание",
                "Файл истории задач поврежден. Будет создан новый файл.",
            )
            return []

    @staticmethod
    def save_history(history_list: List[Dict[str, str]]) -> None:
        """Безопасное сохранение истории в файл JSON."""
        try:
            with open("task_history.json", "w", encoding="utf-8") as f:
                json.dump(history_list, f, ensure_ascii=False, indent=4)
        except IOError:
            messagebox.showerror(
                "Ошибка", "Критическая ошибка: не удалось записать данные на диск."
            )


# --- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ПРИЛОЖЕНИЯ (GUI) ---
baza_zadach: List[Dict[str, str]] = [
    {"text": "Прочитать научную статью", "topic": "Учёба"},
    {"text": "Сделать утреннюю зарядку", "topic": "Спорт"},
    {"text": "Разобрать файлы на рабочем столе", "topic": "Работа"},
    {"text": "Повторить синтаксис списков в Python", "topic": "Учёба"},
    {"text": "Пробежать 2 километра на стадионе", "topic": "Спорт"},
]

# Загружаем историю из файла при старте
istoria: List[Dict[str, str]] = TaskDataManager.load_history()


def obnovit_spisok_na_ekrane() -> None:
    """Фильтрация истории по типу задачи и обновление Listbox."""
    listbox_history.delete(0, tk.END)
    vibran_topic: str = combo_filter_topic.get()

    for elem in istoria:
        # Проверка фильтра (если выбрано 'Все' или тип совпадает)
        topic_ok: bool = vibran_topic == "Все" or elem["topic"] == vibran_topic

        if topic_ok:
            stroka: str = f"[{elem['topic']}] — {elem['text']}"
            listbox_history.insert(tk.END, stroka)


def sgenerirovat() -> None:
    """Выбор случайной задачи через random и добавление её в историю."""
    sluchaynaya: Dict[str, str] = random.choice(baza_zadach)
    label_task.config(
        text=f'Задача: "{sluchaynaya["text"]}"\nКатегория: {sluchaynaya["topic"]}'
    )

    istoria.insert(0, sluchaynaya)
    TaskDataManager.save_history(istoria)
    obnovit_spisok_na_ekrane()


def dobavit_zadachu() -> None:
    """Валидация непустых строк и добавление новой задачи."""
    t: str = entry_text.get().strip()
    top: str = entry_topic.get().strip()

    # Проверка корректности ввода (Требование №6)
    if not t or not top:
        messagebox.showerror(
            "Ошибка валидации", "Поля 'Что нужно сделать' и 'Тип' не должны быть пустыми!"
        )
        return

    novaya: Dict[str, str] = {"text": t, "topic": top}
    baza_zadach.append(novaya)
    obnovit_filtri()

    entry_text.delete(0, tk.END)
    entry_topic.delete(0, tk.END)
    messagebox.showinfo("Успех", "Новая задача успешно добавлена в пул!")


def obnovit_filtri() -> None:
    """Обновление выпадающего списка фильтрации типов задач."""
    temi: List[str] = ["Все"] + list(set([z["topic"] for z in baza_zadach]))
    combo_filter_topic["values"] = temi


# --- Сборка интерфейса GUI ---
window = tk.Tk()
window.title("Random Task Generator")
window.geometry("600x550")

label_task = tk.Label(
    window,
    text="Нажмите кнопку ниже, чтобы спланировать действие",
    font=("Arial", 11, "italic"),
    wraplength=500,
    fg="darkgreen",
)
label_task.pack(pady=20)

btn_generate = tk.Button(
    window, text="Сгенерировать задачу", font=("Arial", 12, "bold"), command=sgenerirovat
)
btn_generate.pack(pady=5)

# Фильтрация
frame_filter = tk.Frame(window)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Фильтр по типу задачи:").grid(row=0, column=0, padx=5)
combo_filter_topic = ttk.Combobox(frame_filter, state="readonly", width=20)
combo_filter_topic.grid(row=0, column=1, padx=5)
combo_filter_topic.set("Все")

btn_apply = tk.Button(
    frame_filter, text="Применить фильтр", command=obnovit_spisok_na_ekrane
)
btn_apply.grid(row=0, column=2, padx=10)

# Список истории
tk.Label(window, text="История сгенерированных задач:", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
listbox_history = tk.Listbox(window, width=65, height=8)
listbox_history.pack(pady=5, padx=20)

# Форма добавления
frame_add = tk.LabelFrame(window, text=" Создать свою задачу ")
frame_add.pack(pady=15, fill="x", padx=20)

tk.Label(frame_add, text="Что нужно сделать:").grid(row=0, column=0, sticky="w", padx=5)
entry_text = tk.Entry(frame_add, width=45)
entry_text.grid(row=0, column=1, pady=5, padx=5)

tk.Label(frame_add, text="Тип (учёба/спорт/работа):").grid(row=1, column=0, sticky="w", padx=5)
entry_topic = tk.Entry(frame_add, width=45)
entry_topic.grid(row=1, column=1, pady=5, padx=5)

btn_add = tk.Button(frame_add, text="Добавить в пул задач", command=dobavit_zadachu)
btn_add.grid(row=2, column=0, columnspan=2, pady=10)

obnovit_filtri()
obnovit_spisok_na_ekrane()
window.mainloop()
