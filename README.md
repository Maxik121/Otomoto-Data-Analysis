# Otomoto Data Analysis

Projekt analityczny mający na celu zebranie ogłoszeń z serwisu Otomoto, przetworzenie danych i zbudowanie prostego modelu regresji liniowej do predykcji cen samochodów.

## Zawartość repozytorium

- `test.py` — skrypt do pobierania ogłoszeń z Otomoto (prosty scraper oparty na requests + BeautifulSoup). Plik konfigurowany jest przez adres URL oraz zakres stron do pobrania.
- `Data/agregator.py` — narzędzie łączące wiele plików JSON (wygenerowanych przez scraper) w jeden plik CSV `complete_data.csv`.
- `Data/` — katalog z danymi i skryptami pomocniczymi:
  - `complete_data.csv` — surowe, połączone ogłoszenia (bez imputacji pojemności silnika).
  - `cars_data.csv` — przetworzony i oczyszczony zestaw danych gotowy do dalszej analizy i modelowania (z uzupełnioną pojemnością silnika i przeliczoną walutą).
  - `agregator.py` — skrypt łączący pliki JSON w `complete_data.csv`.
- `EDA_data proccessing.ipynb` — notebook z eksploracją danych (EDA) oraz procesem uzupełniania braków, konwersją walut, wykresami i przygotowaniem `cars_data.csv`.
- `predictive_model.ipynb` — notebook z budową modelu regresji liniowej do predykcji ceny samochodu oraz analizą zmiennych kandydujących na regresory.
- `README.md` — (ten plik) opis projektu i instrukcje uruchomienia.

## Cel projektu

1. Zautomatyzować zbieranie ogłoszeń samochodowych z serwisu Otomoto w zadanym obszarze (np. Kraków).
2. Oczyścić i wzbogacić dane (np. ekstrakcja pojemności silnika z pola modelu, uzupełnianie braków, konwersja walut).
3. Przeprowadzić analizę eksploracyjną (EDA) i przygotować dane pod modelowanie.
4. Zbudować prosty model regresji liniowej przewidujący cenę samochodu na podstawie cech takich jak marka, przebieg, rocznik czy pojemność silnika.

## Wymagania

- Python 3.8+ (notebooky działały na 3.13 w środowisku autora)
- Zalecane biblioteki (można zainstalować przez pip):
  - pandas
  - numpy
  - requests
  - beautifulsoup4
  - seaborn
  - matplotlib
  - scikit-learn
  - statsmodels

Przykładowa komenda instalacji:

```bash
pip install pandas numpy requests beautifulsoup4 seaborn matplotlib scikit-learn statsmodels
```

## Jak uruchomić

1. Scraping danych

- Dostosuj URL w `test.py` (zmienna `url`) do swojej wyszukiwarki Otomoto (np. lokalizacja, filtry). Ustaw liczbę stron do pobrania (STRONA_STARTOWA/STRONA_KONCOWA).
- Uruchom:

```bash
python test.py
```

Plik wynikowy będzie zapisywany w katalogu `Data` jako `otomoto_strony_<start>_do_<end>_<timestamp>.json`.

Uwaga: używany scraper jest prosty — zachowaj ostrożność i sprawdź regulamin serwisu Otomoto. W kodzie zastosowano rotację User-Agent oraz losowe opóźnienia między żądaniami, ale przy intensywnym pobieraniu warto stosować dodatkowe zabezpieczenia i respektować zasady strony.

2. Agregacja plików JSON

- Po zebraniu wielu plików JSON uruchom `Data/agregator.py` (w katalogu, gdzie znajdują się pliki JSON) aby scalić je w `Data/complete_data.csv`:

```bash
python Data/agregator.py
```

3. Przetwarzanie i EDA

- Notebook `EDA_data proccessing.ipynb` zawiera kroki oczyszczania danych, ekstrakcji `Pojemność silnika`, uzupełniania braków (hierarchiczne uzupełnianie medianą po modelu/marki), konwersję walut oraz wykresy opisowe. Otwórz notebook w JupyterLab/Notebook i uruchom komórki.

4. Model predykcyjny

- Notebook `predictive_model.ipynb` to przykładowe podejście do budowy regresji liniowej na przygotowanym zbiorze `Data/cars_data.csv`. Zawiera importy, przygotowanie zmiennych i podstawowe dopasowanie modelu.

## Struktura danych i kolumny

Główne kolumny w przetworzonym pliku `cars_data.csv`:

- Marka — marka samochodu
- Model — pole tekstowe z nazwą modelu (często zawiera informacje o pojemności)
- Cena — cena ogłoszenia (w PLN)
- Waluta — oryginalna waluta (po przeliczeniu wszystkie rekordy w PLN)
- Paliwo — typ napędu (benzyna, diesel, hybryda, elektryczny itp.)
- Przebieg — przebieg w kilometrach
- Rocznik — rok produkcji
- Skrzynia biegów — typ skrzyni (Manualna/Automatyczna)
- Pojemność silnika — wartość numeryczna (w litrach), wyekstrahowana z pola Model i uzupełniona
- Pojemność_znana — binarna flaga informująca czy pojemność była bezpośrednio dostępna w tekście

## Pomysły na rozwinięcie projektu

- Rozszerzenie parsowania szczegółowych parametrów z ogłoszeń (moc silnika, kolor, wyposażenie, liczba właścicieli itp.).
- Użycie bardziej zaawansowanych modeli (RandomForest, XGBoost) i porównanie wyników z regresją liniową.
- Walidacja modelu i przygotowanie pipeline'u (scaler, kodowanie kategorii, selekcja cech).
- Stworzenie API/serwisu umożliwiającego predykcję ceny na podstawie formularza (np. Flask/FastAPI).
- Automatyzacja zbierania danych jako job (z zachowaniem zasad strony i limitów).

## Uwagi prawne i etyczne

- Zbieranie danych ze stron zewnętrznych może podlegać regulaminom serwisów oraz przepisom prawnym. Przed uruchamianiem scalera w szerokiej skali sprawdź regulamin Otomoto oraz obowiązujące przepisy dotyczące scrapingu.
- Nie udostępniaj poufnych danych ani nie wykorzystuj danych w sposób naruszający prawa innych podmiotów.

## Kontakt

Masz pytania lub chcesz współpracować? Otwórz issue w repozytorium lub skontaktuj się ze mną przez GitHub: @Maxik121

## Licencja

Brak jawnie określonej licencji w repozytorium. Jeśli chcesz, dodaj plik `LICENSE` lub doprecyzuj zasady użycia — domyślnie repozytorium jest objęte prawami autorskimi właściciela.
