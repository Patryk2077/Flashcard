from tkinter import *
import sqlite3
from pathlib import Path
import os
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style
from create_gui import kreator_interfejsu

current_dir = Path(__file__).resolve(
).parent
os.chdir(current_dir)

root = Tk()
root.title("FlashCard")


class Flashcard():
    def __init__(self, root):
        kreator_interfejsu(root)

    def kreator_tabeli(self, nazwa_tabeli):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()

            # Tworzenie głównej tabeli z wszystkimi zestawami
            cursor.execute("""CREATE TABLE IF NOT EXISTS zestawy_fiszek(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nazwa TEXT NOT NULL)""")

            # Tworzenie poszczególnych zestawów
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nazwa_tabeli}(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                           zestaw_id INTEGER
                          zdanie TEXT NOT NULL,
                          tłumaczenie TEXT NOT NULL,
                           FOREIGN KEY (zestaw_id) REFERENCES zestawy_fiszek(id) )""")

    def dodawanie_rekordów(self, nazwa_tabeli, zdanie, tłumaczenie):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""INSERT INTO {nazwa_tabeli} (zdanie, tłumaczenie) VALUES (?, ?) """, (zdanie, tłumaczenie))


app = Flashcard(root)
app.kreator_tabeli("kurs")
root.mainloop()
