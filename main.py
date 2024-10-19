import tkinter as tk
import sqlite3
from pathlib import Path
import os
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style

# ustawienie katalogu roboczego na bierzący folder
current_dir = Path(__file__).resolve(
).parent
os.chdir(current_dir)

# Połączenie z bazą danych SQLite i tworzenie tabel, jeśli nie istnieją
connection = sqlite3.connect("flashcard.db")
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        set_id INTEGER,
        polish TEXT,
        english TEXT,
        UNIQUE(set_id, polish),
        FOREIGN KEY (set_id) REFERENCES sets(id) ON DELETE CASCADE
    )
''')
connection.commit()

# Funkcja pomocnicza do pobrania dostępnych zestawów


def get_sets():
    cursor.execute("Select * FROM sets")
    return cursor.fetchall()


# ============================
# Główne okno aplikacji
# ============================
root = tk.Tk()
root.title("FlashCard")
root.geometry("600x400")

# Stylizowanie interfejsu gui
style = Style(theme="superhero")
style.configure("TLabel", font=('TkDefaultFont', 18))
style.configure("TButton", font=('TkDefaultFont', 16), width=12)


# Tworzenie widzetu do zarządzania kartami
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# =====================================
# Karta Nauka
# =====================================

learning_frame = ttk.Frame(notebook)
notebook.add(learning_frame, text="Nauka")

selected_set_id = tk.IntVar()
current_card_index = 0
cards = []


def load_cards(set_id):
    "Funkcja pobierająca fiszki z wybranego zestawu"
    global cards, current_card_index
    cursor.execute("SELECT polish, english FROM cards WHERE id=?", (set_id))
    cards = cursor.fetchall()
    current_card_index = 0
    if cards:
        show_card(current_card_index)
    else:
        messagebox.showinfo("Info", "Brak fiszek w wybranym zestawie.")


def show_card(index):
    if cards:
        polish_label.config(tekst=cards[index][0])
        answer_entry.delete(0, tk.END)
        answer_label.config(tekst="")


def show_answer():
    if cards:
        answer_label.config(text=cards[current_card_index][1])


def previous_card():
    global current_card_index
    if current_card_index > 0:
        current_card_index -= 1
        show_card(current_card_index)


def next_card():
    global current_card_index
    if current_card_index < len(cards) - 1:
        current_card_index += 1
        show_card(current_card_index)


# Interfejs do nauki
set_selection = ttk.Combobox(learning_frame, state="readonly", width=40)
set_selection.pack(pady=10)


def update_set_selection():
    sets = get_sets()
    set_selection['values'] = [f"{s[1]} (ID: {s[0]})" for s in sets]
    set_selection.bind("<<ComboboxSelected>>", lambda: load_cards(
        int(set_selection.get().split(": ")[1])))


polish_label = ttk.Label(learning_frame, text="")
polish_label.pack(pady=10)

answer_entry = ttk.Entry(learning_frame, width=40)
answer_entry.pack()

answer_label = ttk.Label(learning_frame, text="", foreground="green")
answer_label.pack(pady=10)

button_frame = ttk.Frame(learning_frame)
button_frame.pack(pady=10)

previous_button = ttk.Button(
    button_frame, text="Poprzedni", command=previous_card)
previous_button.grid(row=0, column=0, padx=5)

show_answer_button = ttk.Button(
    button_frame, text="Pokaż", command=show_answer)
show_answer_button.grid(row=0, column=1, padx=5)

next_button = ttk.Button(button_frame, text="Następny", command=next_card)
next_button.grid(row=0, column=2, padx=5)

update_set_selection()

# ============================
# Karta Dodawanie Zdań
# ============================

add_card_frame = ttk.Frame(notebook)
notebook.add(add_card_frame, text="Dodawanie nowych kart")

new_card_set = ttk.Combobox(add_card_frame, state="readonly", width=40)
new_card_set.pack(pady=10)

update_set_selection()  # Aktualizacja listy zestawów

polish_entry = ttk.Entry(add_card_frame, width=40)
polish_entry.pack(pady=5)
polish_entry.insert(0, "Tekst po polsku")

english_entry = ttk.Entry(add_card_frame, width=40)
english_entry.pack(pady=5)
english_entry.insert(0, "Tekst po angielsku")


def add_card():
    set_id = int(new_card_set.get().split(": ")[1])
    polish = polish_entry.get().strip()
    english = english_entry.get().strip()

    if not polish or not english:
        messagebox.showwarning("Błąd", "Wprowadź obie strony fiszki.")
        return
    try:
        cursor.execute("INSERT INTO cards (set_id, polish, english) VALUES (?, ?, ?)",
                       (set_id, polish, english))
        connection.commit()
        messagebox.showinfo("Sukces", "Dodano nową fiszkę.")
        polish_entry.delete(0, tk.END)
        english_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showwarning(
            "Błąd", "Taka fiszka już istnieje w tym zestawie.")


add_card_button = ttk.Button(add_card_frame, text="Zapisz", command=add_card)
add_card_button.pack(pady=10)

# =================================
# Karta Dodawanie zestawu
# =================================
manage_sets_frame = ttk.Frame(notebook)
notebook.add(manage_sets_frame, text="Dodawanie zestawów kart")

set_name_entry = ttk.Entry(manage_sets_frame, width=40)
set_name_entry.pack(pady=5)
set_name_entry.insert(0, "Nazwa zestawu")


def add_set():
    set_name = set_name_entry.get().strip()
    if not set_name:
        messagebox.showwarning("Błąd", "Wprowadź nazwę zestawu.")
        return

    try:
        cursor.execute("INSERT INTO sets (name) VALUES (?)", (set_name,))
        connection.commit()
        update_set_selection()
        messagebox.showinfo("Sukces", "Dodano nowy zestaw.")
        set_name_entry.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showwarning("Błąd", "Zestaw o takiej nazwie już istnieje.")


add_set_button = ttk.Button(
    manage_sets_frame, text="Dodaj zestaw", command=add_set)
add_set_button.pack(pady=10)


def delete_set():
    set_name = set_name_entry.get().strip()
    if not set_name:
        messagebox.showwarning("Błąd", "Wprowadź nazwę zestawu do usunięcia.")
        return

    cursor.execute("DELETE FROM sets WHERE name=?", (set_name,))
    connection.commit()
    update_set_selection()
    messagebox.showinfo("Sukces", "Usunięto zestaw.")


delete_set_button = ttk.Button(
    manage_sets_frame, text="Usuń zestaw", command=delete_set)
delete_set_button.pack(pady=10)

# Uruchomienie aplikacji
root.mainloop()
