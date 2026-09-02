import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime

# Lista różnych User-Agentów do rotacji
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
]

def scrape_otomoto(base_url, start_page=1, end_page=40):
    all_cars = []
    session = requests.Session()
    
    # Konfiguracja nagłówków dla sesji
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"otomoto_strony_{start_page}_do_{end_page}_{timestamp}.json"

    for page_number in range(start_page, end_page + 1):
        if "?" in base_url:
            current_url = f"{base_url}&page={page_number}"
        else:
            current_url = f"{base_url}?page={page_number}"
            
        print(f"\n[Strona {page_number}/{end_page}] Pobieranie: {current_url}")
        
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        
        response = session.get(current_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Błąd podczas pobierania strony. Kod statusu: {response.status_code}")
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        json_ld_tag = soup.find('script', id='listing-json-ld')
        if json_ld_tag:
            try:
                data = json.loads(json_ld_tag.string)
                offers = data.get('mainEntity', {}).get('itemListElement', [])
                
                if not offers:
                    print("Brak ofert na tej stronie. Przerywam pobieranie.")
                    break
                
                years_html = [node.text.strip() for node in soup.find_all(attrs={'data-parameter': 'year'})]
                gearboxes_html = [node.text.strip() for node in soup.find_all(attrs={'data-parameter': 'gearbox'})]
                
                for i, offer in enumerate(offers):
                    item = offer.get('itemOffered', {})
                    price_spec = offer.get('priceSpecification', {})
                    
                    rocznik = years_html[i] if i < len(years_html) else "Brak"
                    skrzynia = gearboxes_html[i] if i < len(gearboxes_html) else "Brak"

                    # Tworzenie słownika z informacjami o samochodzie
                    car_info = {
                        "Marka": item.get('brand'),
                        "Model": item.get('name'),
                        "Cena": price_spec.get('price'),
                        "Waluta": price_spec.get('priceCurrency'),
                        "Paliwo": item.get('fuelType'),
                        "Przebieg": item.get('mileageFromOdometer', {}).get('value'),
                        "Rocznik": rocznik,
                        "Skrzynia biegów": skrzynia
                    }
                    all_cars.append(car_info)
                    
            except json.JSONDecodeError:
                print("Błąd parsowania danych strukturalnych JSON-LD.")
        else:
            print("Nie znaleziono tagu z danymi strukturalnymi na tej stronie.")
            break
            
        # Zapisanie danych do pliku JSON po każdej stronie
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(all_cars, f, ensure_ascii=False, indent=4)
        print(f"Dane zapisane! W pliku {output_filename} znajduje się obecnie {len(all_cars)} ogłoszeń.")
        
        # Zabezpieczenie kodu
        if page_number < end_page:
            sleep_time = random.uniform(5.0, 13.0)
            print(f"Oczekiwanie {sleep_time:.2f} sekund przed kolejnym żądaniem...")
            time.sleep(sleep_time)

    return all_cars, output_filename

if __name__ == '__main__':
    url = "https://www.otomoto.pl/osobowe/krakow?search%5Blat%5D=50.07567&search%5Blon%5D=19.93084&search%5Badvanced_search_expanded%5D=true"

    # Ustawienie zakresu paczki danych
    STRONA_STARTOWA = 180
    STRONA_KONCOWA = 200

    print(f"Rozpoczęcie pobierania danych (od strony {STRONA_STARTOWA} do {STRONA_KONCOWA})...")
    scraped_data, plik_wynikowy = scrape_otomoto(url, start_page=STRONA_STARTOWA, end_page=STRONA_KONCOWA)
    
    print(f"\nProces zakończony. Pobrano łącznie {len(scraped_data)} ofert.")
    print(f"Wszystkie dane czekają na Ciebie w pliku: {plik_wynikowy}")