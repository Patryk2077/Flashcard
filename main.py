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
        kreator_interfejsu(self, root)
        self.wybrany_zestaw = None

    def kreator_tabeli(self, nazwa_tabeli):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()

            # Tworzenie głównej tabeli z wszystkimi zestawami
            cursor.execute("""CREATE TABLE IF NOT EXISTS zestawy_fiszek(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           nazwa TEXT NOT NULL)""")

            # Sprawdzenie, czy zestaw o tej nazwie już istnieje w zestawy_fiszek
            cursor.execute(
                "SELECT nazwa FROM zestawy_fiszek WHERE nazwa = ?", (nazwa_tabeli,))
            wynik = cursor.fetchone()

            # Jeśli nie ma takiego wpisu, dodaj nową nazwę zestawu do tabeli zestawy_fiszek
            if wynik is None:
                cursor.execute(
                    "INSERT INTO zestawy_fiszek (nazwa) VALUES (?)", (nazwa_tabeli,))

            # Tworzenie poszczególnych zestawów
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nazwa_tabeli}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        zdanie TEXT,
                        tłumaczenie TEXT,
                        status INTEGER )""")

    def dodawanie_rekordów(self, nazwa_tabeli, zdanie, tłumaczenie, status=0):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()
            zdanie_value = zdanie.get()
            tłumaczenie_value = tłumaczenie.get()
            cursor.execute(
                f"""INSERT INTO {nazwa_tabeli} (zdanie, tłumaczenie, status) VALUES (?, ?, ?) """, (zdanie_value, tłumaczenie_value, status))

    # Funkcja pobierania nazw wszystkich zestawów kart flash z bazy danych
    def pobierz_wszystkie_zestawy(self):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id,nazwa FROM zestawy_fiszek")
            rows = cursor.fetchall()
            zestawy = [row[1] for row in rows]
        return zestawy

    # Zapisuje wybrany zestaw do nauki
    def zapisz_wybrany_zestaw(self, event):
        combobox = event.widget
        self.wybrany_zestaw = combobox.get()

    # Pobieranie zdania z tabeli
    def pobierz_zdania(self):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT zdanie, tłumaczenie FROM szkoła")
            wyniki = cursor.fetchall()
            karty = [(wynik[0], wynik[1]) for wynik in wyniki]
            return karty


app = Flashcard(root)
wynik = app.pobierz_zdania()
print(wynik)
root.mainloop()
