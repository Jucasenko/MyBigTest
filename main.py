import json
import random
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List


# --- ЛОГИКА РАБОТЫ С ДАННЫМИ (Требование №3: Разделение логики и GUI) ---
class DataManager:

    @staticmethod
    def load_history() -> List[Dict[str, str]]:
        """Загрузка истории с обработкой конкретных исключений (Требование №2)."""
        try:
            with open("history.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                # Проверка корректности структуры JSON (Требование №4)
                if isinstance(data, list):
                    return data
                return []
        except FileNotFoundError:
            # Если файла нет — это штатная ситуация при первом запуске
            return []
        except json.JSONDecodeError:
            # Если файл поврежден — выводим сообщение пользователю (Требование №2)
            messagebox.showwarning(
                "Внимание",
                "Файл истории поврежден. Будет автоматически создан новый файл.",
            )
            return []

    @staticmethod
    def save_history(history_list: List[Dict[str, str]]) -> None:
        """Безопасное сохранение истории в файл JSON."""
        try:
            with open("history.json", "w", encoding="utf-8") as f:
                json.dump(history_list, f, ensure_ascii=False, indent=4)
        except IOError:
            messagebox.showerror(
                "Ошибка", "Критическая ошибка: не удалось записать данные на диск."
            )


# --- ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ПРИЛОЖЕНИЯ (GUI) ---
baza_citat: List[Dict[str, str]] = [
    {
        "text": "Учись так, будто тебе предстоит жить вечно.",
        "author": "Махатма Ганди",
        "topic": "Мотивация",
    },
    {
        "text": "Жизнь — это то, что с нами происходит, пока мы строим планы.",
        "author": "Джон Леннон",
        "topic": "Жизнь",
    },
    {
        "text": "Логика может привести вас от пункта А к пункту Б, а воображение — куда угодно.",
        "author": "Альберт Эйнштейн",
        "topic": "Наука",
    },
]

# Инициализируем историю через вызов класса логики
istoria: List[Dict[str, str]] = DataManager.load_history()


def obnovit_spisok_na_ekrane() -> None:
    """Фильтрация истории и обновление элемента Listbox."""
    listbox_history.delete(0, tk.END)
    vibran_author: str = combo_filter_author.get()
    vibran_topic: str = combo_filter_topic.get()

    for elem in istoria:
        author_ok: bool = (
            vibran_author == "Все" or elem["author"] == vibran_author
        )
        topic_ok: bool = vibran_topic == "Все" or elem["topic"] == vibran_topic

        if author_ok and topic_ok:
            stroka: str = (
                f"[{elem['topic']}] {elem['author']}: \"{elem['text']}\""
            )
            listbox_history.insert(tk.END, stroka)


def sgenerirovat() -> None:
    """Выбор случайной цитаты через random и добавление её в историю."""
    sluchaynaya: Dict[str, str] = random.choice(baza_citat)
    label_quote.config(
        text=f'"{sluchaynaya["text"]}"\n\nАвтор: {sluchaynaya["author"]} | Тема: {sluchaynaya["topic"]}'
    )
    istoria.insert(0, sluchaynaya)

    # Вызываем метод сохранения данных из класса DataManager
    DataManager.save_history(istoria)
    obnovit_spisok_na_ekrane()


def dobavit_citatu() -> None:
    """Валидация пустых строк и добавление новой цитаты пользователем."""
    t: str = entry_text.get().strip()
    a: str = entry_author.get().strip()
    top: str = entry_topic.get().strip()

    # Строгая проверка на пустые поля
    if not t or not a or not top:
        messagebox.showerror(
            "Ошибка валидации", "Все поля должны быть обязательно заполнены!"
        )
        return

    novaya: Dict[str, str] = {"text": t, "author": a, "topic": top}
    baza_citat.append(novaya)
    obnovit_filtri()

    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_topic.delete(0, tk.END)
    messagebox.showinfo("Успех", "Новая цитата добавлена в текущую сессию!")


def obnovit_filtri() -> None:
    """Сбор уникальных авторов и тем для выпадающих списков."""
    avtori: List[str] = ["Все"] + list(set([c["author"] for c in baza_citat]))
    temi: List[str] = ["Все"] + list(set([c["topic"] for c in baza_citat]))
    combo_filter_author["values"] = avtori
    combo_filter_topic["values"] = temi


# --- Сборка оконного интерфейса ---
window = tk.Tk()
window.title("Random Quote Generator Pro")
window.geometry("650x650")

label_quote = tk.Label(
    window,
    text="Нажмите кнопку ниже, чтобы получить цитату",
    font=("Arial", 11, "italic"),
    wraplength=550,
    fg="blue",
)
label_quote.pack(pady=20)

btn_generate = tk.Button(
    window, text="Сгенерировать цитату", font=("Arial", 12, "bold"), command=sgenerirovat
)
btn_generate.pack(pady=5)

frame_filter = tk.Frame(window)
frame_filter.pack(pady=10)

tk.Label(frame_filter, text="Фильтр Автора:").grid(row=0, column=0, padx=5)
combo_filter_author = ttk.Combobox(frame_filter, state="readonly", width=15)
combo_filter_author.grid(row=0, column=1, padx=5)
combo_filter_author.set("Все")

tk.Label(frame_filter, text="Фильтр Темы:").grid(row=0, column=2, padx=5)
combo_filter_topic = ttk.Combobox(frame_filter, state="readonly", width=15)
combo_filter_topic.grid(row=0, column=3, padx=5)
combo_filter_topic.set("Все")

btn_apply = tk.Button(
    frame_filter, text="Применить фильтр", command=obnovit_spisok_na_ekrane
)
btn_apply.grid(row=0, column=4, padx=10)

tk.Label(window, text="История просмотров:", font=("Arial", 10, "bold")).pack()
listbox_history = tk.Listbox(window, width=75, height=8)
listbox_history.pack(pady=5)

frame_add = tk.LabelFrame(window, text="Добавить свою цитату в базу")
frame_add.pack(pady=15, fill="x", padx=20)

tk.Label(frame_add, text="Текст цитаты:").grid(row=0, column=0, sticky="w", padx=5)
entry_text = tk.Entry(frame_add, width=50)
entry_text.grid(row=0, column=1, pady=3, padx=5)

tk.Label(frame_add, text="Автор:").grid(row=1, column=0, sticky="w", padx=5)
entry_author = tk.Entry(frame_add, width=50)
entry_author.grid(row=1, column=1, pady=3, padx=5)

tk.Label(frame_add, text="Тема:").grid(row=2, column=0, sticky="w", padx=5)
entry_topic = tk.Entry(frame_add, width=50)
entry_topic.grid(row=2, column=1, pady=3, padx=5)

btn_add = tk.Button(frame_add, text="Сохранить в базу", command=dobavit_citatu)
btn_add.grid(row=3, column=0, columnspan=2, pady=10)

obnovit_filtri()
obnovit_spisok_na_ekrane()
window.mainloop()
