import pandas as pd
import glob

def file_connector_json():
    files_json = glob.glob("otomoto_*.json")
    if not files_json:
        print("Nie znaleziono plików JSON w bieżącym katalogu.")
        return
    print(f"Znaleziono {len(files_json)} plików JSON. Łączenie danych...")

    data_list = []
    for file in files_json:
        df = pd.read_json(file)
        data_list.append(df)

    complete_df = pd.concat(data_list, ignore_index=True)

    # Czyszczenie duplikatów (poprawiono błąd z inplace=True)
    initial_number = len(complete_df)
    complete_df.drop_duplicates(inplace=True)
    amount_of_duplicates = initial_number - len(complete_df)

    # Zapis do CSV (usunięto zbędny podwójny zapis)
    complete_df.to_csv("complete_data.csv", index=False, encoding='utf-8-sig')

    print(f"Połączono dane z {len(files_json)} plików JSON. Zapisano do complete_data.csv.")
    if amount_of_duplicates > 0:
        print(f"Usunięto {amount_of_duplicates} duplikatów z danych.")
    print("Proces zakończony.")

if __name__ == "__main__":
    file_connector_json()