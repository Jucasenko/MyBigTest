import json
import random
import tkinter as tk
from tkinter import messagebox, ttk

# 1. Базовый список цитат (Текст, Автор, Тема)
baza_citat = [
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
    {
        "text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.",
        "author": "Уинстон Черчилль",
        "topic": "Мотивация",
    },
]

# Список для хранения истории просмотров
istoria = []


# Функция загрузки истории из файла JSON (если файла нет, создается пустой)
def load_history():
    global istoria
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            istoria = json.load(f)
            obnovit_spisok_na_ekrane()
    except:
        istoria = []


# Функция сохранения истории в JSON
def save_history():
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(istoria, f, ensure_ascii=False, indent=4)


# Функция обновления списка истории на экране с учетом фильтров
def obnovit_spisok_na_ekrane():
    # Очищаем старый список на экране
    listbox_history.delete(0, tk.END)

    vibran_author = combo_filter_author.get()
    vibran_topic = combo_filter_topic.get()

    # Идем по всей истории и проверяем фильтры
    for elem in istoria:
        # Проверяем автора (если выбрано "Все" или совпадает автор)
        author_ok = vibran_author == "Все" or elem["author"] == vibran_author
        # Проверяем тему (если выбрано "Все" или совпадает тема)
        topic_ok = vibran_topic == "Все" or elem["topic"] == vibran_topic

        if author_ok and topic_ok:
            # Красиво добавляем строчку в список на экране
            stroka = f"[{elem['topic']}] {elem['author']}: \"{elem['text']}\""
            listbox_history.insert(tk.END, stroka)


# 2. Кнопка «Сгенерировать цитату»
def sgenerirovat():
    # Выбираем случайную цитату из базы
    sluchaynaya = random.choice(baza_citat)

    # Показываем её в главном текстовом поле
    label_quote.config(
        text=f'"{sluchaynaya["text"]}"\n\nАвтор: {sluchaynaya["author"]} | Тема: {sluchaynaya["topic"]}'
    )

    # Добавляем в начало списка истории
    istoria.insert(0, sluchaynaya)

    # Сохраняем в файл и обновляем экран
    save_history()
    obnovit_spisok_na_ekrane()


# 6. Кнопка добавления новой цитаты с проверкой пустых строк
def dobavit_citatu():
    t = entry_text.get()
    a = entry_author.get()
    top = entry_topic.get()

    # Проверка на пустые строки
    if t == "" or a == "" or top == "":
        messagebox.showerror("Ошибка", "Заполните все поля для новой цитаты!")
        return

    # Создаем новую цитату и добавляем в базу
    novaya = {"text": t, "author": a, "topic": top}
    baza_citat.append(novaya)

    # Обновляем фильтры, чтобы там появились новые авторы/темы
    obnovit_filtri()

    # Очищаем поля ввода
    entry_text.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_topic.delete(0, tk.END)

    messagebox.showinfo("Успех", "Цитата успешно добавлена в базу!")


# Функция автоматического обновления выпадающих списков фильтрации
def obnovit_filtri():
    # Собираем всех уникальных авторов и темы из базы данных
    avtori = ["Все"] + list(set([c["author"] for c in baza_citat]))
    temi = ["Все"] + list(set([c["topic"] for c in baza_citat]))

    combo_filter_author["values"] = avtori
    combo_filter_topic["values"] = temi


# --- СОЗДАНИЕ ИНТЕРФЕЙСА ОКНА ---
window = tk.Tk()
window.title("Random Quote Generator")
window.geometry("650x650")

# Главное поле для показа сгенерированной цитаты
label_quote = tk.Label(
    window,
    text="Нажмите кнопку ниже, чтобы получить цитату",
    font=("Arial", 11, "italic"),
    wraplength=550,
    fg="blue",
)
label_quote.pack(pady=20)

# Кнопка генерации
btn_generate = tk.Button(
    window, text="Сгенерировать цитату", font=("Arial", 12, "bold"), command=sgenerirovat
)
btn_generate.pack(pady=5)

# --- БЛОК ФИЛЬТРАЦИИ И ИСТОРИИ ---
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

# Кнопка применения фильтров
btn_apply = tk.Button(
    frame_filter, text="Применить фильтр", command=obnovit_spisok_na_ekrane
)
btn_apply.grid(row=0, column=4, padx=10)

# Список истории на экране (Listbox)
tk.Label(window, text="История просмотров:", font=("Arial", 10, "bold")).pack()
listbox_history = tk.Listbox(window, width=75, height=8)
listbox_history.pack(pady=5)

# --- БЛОК ДОБАВЛЕНИЯ СВОЕЙ ЦИТАТЫ ---
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

# Инициализируем фильтры при старте, загружаем историю и запускаем окно
obnovit_filtri()
load_history()
window.mainloop()
