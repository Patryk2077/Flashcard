from tkinter import *
from tkinter import ttk
from ttkbootstrap import Style


def kreator_interfejsu(self, root):
    """Funkcja tworzy interfejs aplikacji"""
    root.geometry("600x400")

    # Zmiene interfejsu GUI
    nazwa_zestawu_var = StringVar()
    zdanie_po_polsku_var = StringVar()
    zdanie_po_angielsku_var = StringVar()

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
        dodawanie_zdań, state="readonly", width=40, values=self.pobierz_wszystkie_zestawy())
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
        wybór_zestawu, state="readonly", width=40, values=self.pobierz_wszystkie_zestawy())
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
