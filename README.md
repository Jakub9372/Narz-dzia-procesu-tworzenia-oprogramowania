# Menedżer Wydatków Domowych (Expense Tracker Pro)

Aplikacja okienkowa (GUI) napisana w języku Python przy użyciu biblioteki `tkinter`. Służy do monitorowania codziennych finansów, kategoryzowania kosztów oraz automatycznego wyliczania statystyk budżetowych.

## Autor
- **Imię i Nazwisko:** Jakub Tyszko
- **Numer albumu:** 13169

---

## Funkcje aplikacji
* **Trwałość danych :** Wydatki automatycznie zapisują się w pliku strukturalnym `wydatki_dane.json`, co pozwala zachować historię po zamknięciu programu.
* **Dynamiczne Filtrowanie:** Możliwość podglądu wydatków tylko z jednej wybranej kategorii wraz z automatyczną aktualizacją sumy dla danego filtra.
* **Pełna Walidacja Danych:** Odporność programu na puste pola formularzy oraz wprowadzanie błędnych znaków (np. liter zamiast kwot finansowych).

---

## Struktura repozytorium
* `app.py` - Główny kod źródłowy aplikacji z kompletnym interfejsem GUI oraz pełną dokumentacją kodu (docstringi, komentarze).
* `wydatki_dane.json` - Plik z bazą danych (tworzony automatycznie przy pierwszym uruchomieniu).
* `README.md` - Niniejszy plik dokumentacji technicznej i instrukcji w formacie Markdown.

---

## Instrukcja uruchomienia aplikacji

### Wymagania wstępne
Do uruchomienia aplikacji wymagane jest posiadanie zainstalowanego środowiska **Python w wersji 3.x**. Biblioteka graficzna `tkinter`.

### Krok po kroku
1. Pobierz zawartość tego repozytorium na swój dysk twardy lub sklonuj je poleceniem:
   ```bash
   git clone [LINK_DO_TWOJEGO_REPOZYTORIUM]
