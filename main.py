from tkinter import *
import sqlite3
from pathlib import Path
import os
from tkinter import ttk
from tkinter import messagebox
from ttkbootstrap import Style


current_dir = Path(__file__).resolve(
).parent
os.chdir(current_dir)

root = Tk()
root.title("FlashCard")

# Zmiene interfejsu GUI
nazwa_zestawu_var = StringVar()
zdanie_po_polsku_var = StringVar()
zdanie_po_angielsku_var = StringVar()


class Flashcard():
    def __init__(self, root):
        self.kreator_interfejsu(root)
        self.wybrany_zestaw = None

    def kreator_interfejsu(self, root):
        """Funkcja tworzy interfejs aplikacji"""
        root.geometry("600x400")

        # Zmiene interfejsu GUI
        # nazwa_zestawu_var = StringVar()
        # zdanie_po_polsku_var = StringVar()
        # zdanie_po_angielsku_var = StringVar()

        # Stylizowanie interfejsu gui
        style = Style(theme="superhero")
        style.configure("TLabel", font=('TkDefaultFont', 18))
        style.configure("TButton", font=('TkDefaultFont', 16), width=10)

        # Tworzenie widzetu do zarządzania kartami
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

    # =====================================
    # Karta Tryb Nauki
    # =====================================

        # Utwórz kartę "Tryb nauki" i jej zawartość
        tryb_nauki = ttk.Frame(notebook)
        notebook.add(tryb_nauki, text="Tryb Nauki")

        # Etykieta "Przetłumacz zdanie"
        ttk.Label(tryb_nauki, text="przykłądowe zdanie").pack(padx=10, pady=10)

        # Pole do wpisywania tłumaczenia
        pole_tłumaczenie = ttk.Entry(tryb_nauki, width=40)
        pole_tłumaczenie.pack(padx=5, pady=20)

        # Przycisk "poprzedni"
        ttk.Button(tryb_nauki, text="Poprzedni", command=None).pack(
            padx=20, pady=5, side="left")

        # Przycisk do odwracania karty
        ttk.Button(tryb_nauki, text="Pokaż", command=None).pack(
            padx=40, pady=5, side="left")

        # Przycisk "następny"
        ttk.Button(tryb_nauki, text="Następny", command=None).pack(
            padx=20, pady=5, side="right")

    # ============================
    # Karta Dodawanie Zdań
    # ============================

        # Tworzenie karty "Dodawanie Zdań" i jej zawartość
        dodawanie_zdań = ttk.Frame(notebook)
        notebook.add(dodawanie_zdań, text="Dodawanie Zdań")

        # Etykieta opisująca wybór zestawu
        ttk.Label(dodawanie_zdań, text="Wybierz zestaw").pack(padx=5, pady=5)

        # Combobox do wybierania istniejących zestawów kart
        zestaw_combobox = ttk.Combobox(
            dodawanie_zdań, state="readonly", width=40, values=self.pobieranie_wszystkich_zestawów())
        zestaw_combobox.pack(padx=5, pady=5)
        zestaw_combobox.bind("<<ComboboxSelected>>",
                             self.zapisz_wybrany_zestaw)

        # Pole do wprowadzania zdania po polsku
        ttk.Label(dodawanie_zdań, text="zdanie po polsku").pack(
            padx=5, pady=10)
        ttk.Entry(dodawanie_zdań, textvariable=zdanie_po_polsku_var,
                  width=45).pack(padx=5, pady=5)

        # Pole do wprowadzania zdania po angielsku
        ttk.Label(dodawanie_zdań, text="definicja po angielsku").pack(
            padx=5, pady=10)
        ttk.Entry(dodawanie_zdań, textvariable=zdanie_po_angielsku_var,
                  width=45).pack(padx=5, pady=5)

        # Przycisk "zapisz"
        ttk.Button(dodawanie_zdań, text="Zapisz",
                   command=lambda: self.dodawanie_rekordów(self.wybrany_zestaw, zdanie_po_polsku_var, zdanie_po_angielsku_var)).pack(padx=5, pady=10)

    # =================================
    # Karta Wybór Zestawu
    # =================================
        # Tworzenie karty "Nowy Zestaw" i jej zawartość
        wybór_zestawu = ttk.Frame(notebook)
        notebook.add(wybór_zestawu, text="Wybór Zestawu")

        # Etykieta opisująca wybór zestawu
        ttk.Label(wybór_zestawu, text="Wybierz zestaw").pack(padx=5, pady=5)

        # Combobox do wybierania istniejących zestawów kart
        zestaw_combobox = ttk.Combobox(
            wybór_zestawu, state="readonly", width=40, values=self.pobieranie_wszystkich_zestawów())
        zestaw_combobox.pack(padx=5, pady=5)
        zestaw_combobox.bind("<<ComboboxSelected>>",
                             self.zapisz_wybrany_zestaw)

        # Etykieta opisująca tworzenie nowego zestawu
        ttk.Label(wybór_zestawu, text="Nazwa nowego zestawu").pack(
            padx=5, pady=10)
        ttk.Entry(wybór_zestawu, textvariable=nazwa_zestawu_var, width=45).pack(
            padx=5, pady=5)

        # Przycisk "utwórz zestaw"
        ttk.Button(wybór_zestawu, text="Zapisz",
                   command=lambda: self.kreator_tabeli(
                       nazwa_zestawu_var.get())).pack(padx=5, pady=5)

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
                        zestaw_id INTEGER,
                        zdanie TEXT,
                        tłumaczenie TEXT,
                        FOREIGN KEY (zestaw_id) REFERENCES zestawy_fiszek(id) )""")

    def dodawanie_rekordów(self, nazwa_tabeli, zdanie, tłumaczenie):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()
            zdanie_value = zdanie.get()
            tłumaczenie_value = tłumaczenie.get()
            cursor.execute(
                f"""INSERT INTO {nazwa_tabeli} (zdanie, tłumaczenie) VALUES (?, ?) """, (zdanie_value, tłumaczenie_value))

    # Funkcja pobierania nazw wszystkich zestawów kart flash z bazy danych
    def pobieranie_wszystkich_zestawów(self):
        with sqlite3.connect("flashcard.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id,nazwa FROM zestawy_fiszek")
            rows = cursor.fetchall()
            zestawy = [row[1] for row in rows]
        return zestawy

    # Zapisuje wybrazy zestaw do nauki
    def zapisz_wybrany_zestaw(self, event):
        combobox = event.widget
        self.wybrany_zestaw = str(combobox.get())


app = Flashcard(root)
app.kreator_tabeli("szkoła")
root.mainloop()
