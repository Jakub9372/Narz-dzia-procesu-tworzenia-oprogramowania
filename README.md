# FitLicznik Pro — Twój Osobisty Kalkulator Kalorii

## Autor
- **Imię i Nazwisko:** Jakub Tyszko
- **Numer albumu:** 13169

---

## Co posiada aplikacja
* **Trwałość i persistencyjność danych:** Użycie pliku `kalorie_dane.json` gwarantuje, że po ponownym uruchomieniu aplikacji dane użytkownika (wpisane posiłki oraz zmodyfikowany cel kaloryczny) zostaną automatycznie przywrócone.
* **Filtrowanie rekordów:** Możliwość segregowania wpisów według kategorii (*Śniadanie*, *Obiad*, *Kolacja*, *Przekąska*), co znacznie poprawia czytelność przy wielu wpisach.
* **System powiadomień wizualnych:** Pasek postępu (`Progressbar`) oraz dynamiczna zmiana kolorów podsumowania (zielony, żółty, czerwony) informują o stopniu realizacji założeń dietetycznych.
* **Pełna odporność na błędy:** Walidacja typów danych zabezpiecza program przed crashowaniem w wyniku wpisania liter zamiast cyfr lub ujemnych wartości.
* **Kompletna dokumentacja:** Kod źródłowy posiada pełne opisy klas i metod za pomocą standardu docstring oraz komentarzy strukturalnych.

---

## Struktura plików w repozytorium
* `app.py` - Główny program wykonywalny zawierający logikę aplikacji i warstwę wizualną.
* `kalorie_dane.json` - Lokalna tekstowa baza danych w formacie JSON (generowana przy pierwszym uruchomieniu).
* `README.md` - Niniejsza dokumentacja techniczna projektu stworzona w formacie Markdown.

---

## Instrukcja instalacji i uruchomienia

### Wymagania techniczne
Aplikacja bazuje wyłącznie na bibliotekach standardowych standardu **Python 3.x**.

### Procedura uruchomienia
1. Sklonuj repozytorium na lokalne urządzenie:
   ```bash
   git clone [TUTAJ_WKLEISZ_LINK_DO_TEGO_REPOZYTORIUM_PO_JEGO_UTWORZENIU]
