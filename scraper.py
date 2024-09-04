import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc  # Biblioteka do omijania zabezpieczeń Cloudflare

# Konfiguracja opcji przeglądarki
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uruchom w trybie bez interfejsu graficznego, jeśli potrzebne

# Inicjalizacja przeglądarki z undetected_chromedriver
driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Funkcja do pobierania danych o numerze z nowej strony
def get_number_info(number):
    url = f"https://www.nieznany-numer.pl/numer/{number}"
    driver.get(url)
    
    # Czekaj, aż numer telefonu będzie dostępny lub strona się załaduje
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        
        # Pobieranie numeru telefonu
        phone_number = driver.find_element(By.CSS_SELECTOR, "h1").text
        
        # Pobieranie statusu
        status_element = driver.find_element(By.CSS_SELECTOR, ".status-class-selector")  # <-- Tu podajemy właściwy selektor dla statusu
        status = status_element.text.strip()

        # Pobieranie komentarzy
        comments_elements = driver.find_elements(By.CSS_SELECTOR, ".comments-class-selector")  # <-- Tu podajemy właściwy selektor dla komentarzy
        comments = [comment.text.strip() for comment in comments_elements]

        return phone_number, status, comments

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return None, None, None

# Numer telefonu do przetworzenia
number = "500965578"

# Otwórz plik CSV do zapisu
with open('numer_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Numer', 'Status', 'Komentarze']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Zapisz nagłówki do pliku CSV
    writer.writeheader()

    # Przetwarzanie numeru
    print(f"\nPrzetwarzanie numeru: {number}")
    phone_number, status, comments = get_number_info(number)
    if phone_number and status and comments:
        # Zapisz dane do pliku CSV
        writer.writerow({'Numer': phone_number, 'Status': status, 'Komentarze': "; ".join(comments)})

# Zamknięcie przeglądarki
driver.quit()
