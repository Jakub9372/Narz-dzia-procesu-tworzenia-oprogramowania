import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class AdvancedCalorieCounter:
    """Główna klasa aplikacji FitLicznik Pro.

    Odpowiada za zarządzanie interfejsem użytkownika, walidację danych,
    obliczanie bilansu kalorycznego oraz trwałe zapisywanie posiłków.
    """

    def __init__(self, root):
        """Inicjalizuje okno, ładuje bazę danych i tworzy elementy GUI."""
        self.root = root
        self.root.title("FitLicznik Pro — Licznik Kalorii")
        self.root.geometry("550x700")
        self.root.resizable(False, False)

        # Plik do trwałego przechowywania danych posiłków i celu
        self.DATA_FILE = "kalorie_dane.json"

        # Domyślne wartości zmiennych
        self.suma_kalorii = 0
        self.cel_kalorii = 2000
        self.lista_posilkow = []
        self.kategorie = [
            "Wszystkie",
            "Śniadanie",
            "Obiad",
            "Kolacja",
            "Przekąska",
        ]

        # Wczytanie danych z pliku przed uruchomieniem okna
        self.wczytaj_dane()

        # --- TŁO APLIKACJI (Canvas w wersji Dark Mode) ---
        self.canvas_tlo = tk.Canvas(
            root, width=550, height=700, bg="#0F172A", bd=0, highlightthickness=0
        )
        self.canvas_tlo.pack(fill="both", expand=True)

        # Dekoracyjne kształty w tle (ciemniejsze, dopasowane odcienie)
        self.canvas_tlo.create_oval(
            -50, -50, 200, 200, fill="#1E293B", outline=""
        )
        self.canvas_tlo.create_oval(
            380, 520, 600, 740, fill="#334155", outline=""
        )

        # Główna karta interfejsu (ciemny panel centralny)
        self.okno_glowne = tk.Frame(
            root,
            bg="#1E293B",
            bd=0,
            highlightbackground="#334155",
            highlightthickness=1,
        )
        self.canvas_tlo.create_window(
            275, 350, window=self.okno_glowne, width=480, height=640
        )

        # --- ELEMENTY INTERFEJSU (GUI) ---
        self.lbl_tytul = tk.Label(
            self.okno_glowne,
            text=" FitLicznik Kalorii Pro",
            font=("Arial", 16, "bold"),
            bg="#1E293B",
            fg="#F8FAFC",
        )
        self.lbl_tytul.pack(pady=15)

        # Sekcja zarządzania dziennym celem kalorycznym
        self.frame_cel = tk.Frame(self.okno_glowne, bg="#1E293B")
        self.frame_cel.pack(pady=5)

        tk.Label(
            self.frame_cel,
            text="Twój dzienny cel (kcal):",
            font=("Arial", 10),
            bg="#1E293B",
            fg="#94A3B8",
        ).pack(side="left", padx=5)

        self.entry_cel = tk.Entry(
            self.frame_cel,
            width=8,
            font=("Arial", 10),
            justify="center",
            bg="#0F172A",
            fg="white",
            insertbackground="white",
            bd=1,
            relief="solid",
        )
        self.entry_cel.insert(0, str(self.cel_kalorii))
        self.entry_cel.pack(side="left", padx=5)

        self.btn_ustaw_cel = tk.Button(
            self.frame_cel,
            text="Ustaw",
            command=self.aktualizuj_cel,
            bg="#475569",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=8,
        )
        self.btn_ustaw_cel.pack(side="left", padx=5)

        # Formularz dodawania posiłków
        self.frame_input = tk.LabelFrame(
            self.okno_glowne,
            text=" Dodaj posiłek ",
            font=("Arial", 10, "bold"),
            bg="#263449",
            fg="#F8FAFC",
            bd=1,
            relief="solid",
        )
        self.frame_input.pack(pady=10, fill="x", padx=20, ipady=5)

        tk.Label(
            self.frame_input, text="Nazwa posiłku:", bg="#263449", fg="#E2E8F0"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_nazwa = tk.Entry(
            self.frame_input,
            width=18,
            font=("Arial", 10),
            bg="#0F172A",
            fg="white",
            insertbackground="white",
            bd=1,
            relief="solid",
        )
        self.entry_nazwa.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(
            self.frame_input, text="Kalorie (kcal):", bg="#263449", fg="#E2E8F0"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_kalorie = tk.Entry(
            self.frame_input,
            width=18,
            font=("Arial", 10),
            bg="#0F172A",
            fg="white",
            insertbackground="white",
            bd=1,
            relief="solid",
        )
        self.entry_kalorie.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(
            self.frame_input, text="Kategoria:", bg="#263449", fg="#E2E8F0"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.combo_kat = ttk.Combobox(
            self.frame_input,
            values=self.kategorie[1:],
            width=16,
            font=("Arial", 10),
            state="readonly",
        )
        self.combo_kat.set("Śniadanie")
        self.combo_kat.grid(row=2, column=1, padx=10, pady=5)

        self.btn_dodaj = tk.Button(
            self.frame_input,
            text="➕\nDodaj",
            command=self.dodaj_posilek,
            bg="#10B981",
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            width=6,
        )
        self.btn_dodaj.grid(row=0, column=2, rowspan=3, padx=10, pady=5, sticky="ns")

        # Sekcja filtrowania listy
        self.frame_filtr = tk.Frame(self.okno_glowne, bg="#1E293B")
        self.frame_filtr.pack(fill="x", padx=20, pady=5)

        tk.Label(
            self.frame_filtr, text="Filtruj listę:", bg="#1E293B", fg="#94A3B8"
        ).pack(side="left", padx=5)
        self.combo_filtr = ttk.Combobox(
            self.frame_filtr,
            values=self.kategorie,
            width=14,
            font=("Arial", 10),
            state="readonly",
        )
        self.combo_filtr.set("Wszystkie")
        self.combo_filtr.pack(side="left", padx=5)
        self.combo_filtr.bind("<<ComboboxSelected>>", lambda e: self.odswiez_liste())

        # Lista posiłków z suwakiem przewijania
        self.frame_list = tk.Frame(self.okno_glowne, bg="#1E293B")
        self.frame_list.pack(fill="both", expand=True, padx=20, pady=5)

        self.listbox_posilki = tk.Listbox(
            self.frame_list,
            font=("Arial", 10),
            bd=1,
            relief="solid",
            bg="#0F172A",
            fg="#E2E8F0",
            selectbackground="#10B981",
            selectforeground="white",
            highlightthickness=0,
        )
        self.listbox_posilki.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(
            self.frame_list, orient="vertical", command=self.listbox_posilki.yview
        )
        self.scrollbar.pack(side="right", fill="y")
        self.listbox_posilki.config(yscrollcommand=self.scrollbar.set)

        # Przyciski zarządzania bazą danych
        self.frame_btns = tk.Frame(self.okno_glowne, bg="#1E293B")
        self.frame_btns.pack(pady=5)

        self.btn_usun = tk.Button(
            self.frame_btns,
            text="❌ Usuń zaznaczone",
            command=self.usun_posilek,
            bg="#EF4444",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=10,
        )
        self.btn_usun.pack(side="left", padx=5)

        self.btn_wyczysc = tk.Button(
            self.frame_btns,
            text="🔄 Wyczyszcz dzień",
            command=self.wyczysc_wszystko,
            bg="#64748B",
            fg="white",
            font=("Arial", 9, "bold"),
            relief="flat",
            padx=10,
        )
        self.btn_wyczysc.pack(side="left", padx=5)

        # Wizualny pasek postępu kalorii
        self.progress = ttk.Progressbar(
            self.okno_glowne, orient="horizontal", length=440, mode="determinate"
        )
        self.progress.pack(pady=5)

        # Podsumowanie liczbowe i procentowe
        self.lbl_suma = tk.Label(
            self.okno_glowne,
            text="Suma: 0 / 2000 kcal (0%)",
            font=("Arial", 13, "bold"),
            bg="#1E293B",
            fg="#10B981",
        )
        self.lbl_suma.pack(pady=15)

        # Pierwsze odświeżenie interfejsu
        self.odswiez_liste()

    def aktualizuj_cel(self):
        """Aktualizuje dzienny limit kalorii po walidacji pola tekstowego."""
        try:
            nowy_cel = int(self.entry_cel.get())
            if nowy_cel <= 0:
                raise ValueError
            self.cel_kalorii = nowy_cel
            self.zapisz_dane()
            self.odswiez_liste()
        except ValueError:
            messagebox.showerror(
                "Błąd wartości", "Cel musi być liczbą całkowitą większą od zera!"
            )

    def dodaj_posilek(self):
        """Pobiera dane, przeprowadza walidację i dopisuje posiłek do listy."""
        nazwa = self.entry_nazwa.get().strip()
        kalorie_txt = self.entry_kalorie.get().strip()
        kategoria = self.combo_kat.get()

        if not nazwa or not kalorie_txt:
            messagebox.showwarning(
                "Puste pola", "Musisz podać nazwę posiłku oraz liczbę kalorii!"
            )
            return

        try:
            kalorie = int(kalorie_txt)
            if kalorie < 0:
                raise ValueError

            # Stworzenie struktury słownika dla nowego wpisu
            nowy_wpis = {
                "nazwa": nazwa,
                "kalorie": kalorie,
                "kategoria": kategoria,
            }
            self.lista_posilkow.append(nowy_wpis)

            # Zapis do JSON i aktualizacja widoków
            self.zapisz_dane()
            self.odswiez_liste()

            # Czyszczenie pól wejściowych
            self.entry_nazwa.delete(0, tk.END)
            self.entry_kalorie.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Błąd danych",
                "Wprowadź prawidłową liczbę całkowitą dla kalorii!",
            )

    def usun_posilek(self):
        """Usuwa wybrany element z listy, odnajdując go w bazie danych JSON."""
        zaznaczony = self.listbox_posilki.curselection()

        if not zaznaczony:
            messagebox.showwarning(
                "Brak wyboru", "Zaznacz pozycję z listy, którą chcesz usunąć."
            )
            return

        tekst_elementu = self.listbox_posilki.get(zaznaczony[0])

        # Szukanie odpowiedniego rekordu w pamięci aplikacji
        for posilek in self.lista_posilkow:
            szablon = f" [{posilek['kategoria']}] {posilek['nazwa']} — {posilek['kalorie']} kcal"
            if szablon == tekst_elementu:
                self.lista_posilkow.remove(posilek)
                break

        self.zapisz_dane()
        self.odswiez_liste()

    def wyczysc_wszystko(self):
        """Resetuje całkowitą listę zjedzonych posiłków w danym dniu."""
        potwierdzenie = messagebox.askyesno(
            "Reset bazy", "Czy na pewno chcesz wyczyścić listę posiłków?"
        )
        if potwierdzenie:
            self.lista_posilkow = []
            self.zapisz_dane()
            self.odswiez_liste()

    def odswiez_liste(self):
        """Aktualizuje elementy Listbox, oblicza sumy i zarządza kolorami ostrzeżeń."""
        self.listbox_posilki.delete(0, tk.END)
        filtr = self.combo_filtr.get()
        self.suma_kalorii = 0

        # Sumowanie całkowite (niezależne od nałożonego filtra widoku)
        for p in self.lista_posilkow:
            self.suma_kalorii += p["kalorie"]

        # Filtrowanie wyświetlania pozycji w Listbox
        for p in self.lista_posilkow:
            if filtr == "Wszystkie" or p["kategoria"] == filtr:
                self.listbox_posilki.insert(
                    tk.END,
                    f" [{p['kategoria']}] {p['nazwa']} — {p['kalorie']} kcal",
                )

        # Wyliczenia procentowe do paska postępu
        procent = (
            int((self.suma_kalorii / self.cel_kalorii) * 100)
            if self.cel_kalorii > 0
            else 0
        )
        self.progress["maximum"] = self.cel_kalorii
        self.progress["value"] = min(self.suma_kalorii, self.cel_kalorii)

        # Dynamiczna aktualizacja tekstu podsumowania
        self.lbl_suma.config(
            text=f"Suma: {self.suma_kalorii} / {self.cel_kalorii} kcal ({procent}%)"
        )

        # Inteligentne zarządzanie kolorami tekstu ostrzeżeń w trybie ciemnym
        if procent < 80:
            self.lbl_suma.config(fg="#10B981")  # Jasnozielony - bezpiecznie
        elif procent <= 100:
            self.lbl_suma.config(fg="#F59E0B")  # Ciepły pomarańcz - blisko limitu
        else:
            self.lbl_suma.config(fg="#F87171")  # Wyrazisty czerwony - przekroczone

    def zapisz_dane(self):
        """Zapisuje aktualne cele i listę posiłków do pliku strukturalnego JSON."""
        paczka_danych = {
            "cel_kalorii": self.cel_kalorii,
            "lista_posilkow": self.lista_posilkow,
        }
        try:
            with open(self.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(paczka_danych, f, ensure_ascii=False, indent=4)
        except IOError:
            messagebox.showerror(
                "Błąd zapisu", "Nie udało się zapisać danych."
            )

    def wczytaj_dane(self):
        """Ładuje dane z pliku JSON. W przypadku braku pliku, uruchamia czystą bazę."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r", encoding="utf-8") as f:
                    paczka = json.load(f)
                    self.cel_kalorii = paczka.get("cel_kalorii", 2000)
                    self.lista_posilkow = paczka.get("lista_posilkow", [])
            except (json.JSONDecodeError, KeyError):
                self.lista_posilkow = []
                self.cel_kalorii = 2000


if __name__ == "__main__":
    # Inicjalizacja i start pętli okna głównego systemu operacyjnego
    root = tk.Tk()
    app = AdvancedCalorieCounter(root)
    root.mainloop()