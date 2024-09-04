import csv
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Konfiguracja opcji przeglądarki
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uruchom w trybie bez interfejsu graficznego

# Inicjalizacja przeglądarki
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Funkcja do pobierania danych o numerze
def get_number_info(number):
    url = f"https://infonumer.pl/numer/{number}"
    driver.get(url)
    
    # Czekaj, aż numer telefonu będzie dostępny
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.ha1")))

    try:
        # Pobieranie numeru telefonu
        phone_number = driver.find_element(By.CSS_SELECTOR, "h1.ha1").text

        # Pobieranie reputacji
        reputation_element = driver.find_element(By.CSS_SELECTOR, "p.mt20")
        reputation_text = reputation_element.text
        reputation_start = reputation_text.find("Reputacja jest") + len("Reputacja jest")
        reputation = reputation_text[reputation_start:].strip().split()[0]

        return phone_number, reputation

    except Exception as e:
        print(f"Błąd podczas pobierania danych: {e}")
        return None, None

# Funkcja do generowania losowych numerów telefonów
def generate_random_numbers(n):
    numbers = []
    for _ in range(n):
        number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        numbers.append(number)
    return numbers

# Lista 300 losowych numerów do przetworzenia plus dodatkowy numer
numbers = generate_random_numbers(300) + ["503210897"]

# Otwórz plik CSV do zapisu
with open('numer_info.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Numer', 'Reputacja']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Zapisz nagłówki do pliku CSV
    writer.writeheader()

    # Przetwarzanie numerów
    for number in numbers:
        print(f"\nPrzetwarzanie numeru: {number}")
        phone_number, reputation = get_number_info(number)
        if phone_number and reputation:
            # Zapisz dane do pliku CSV
            writer.writerow({'Numer': phone_number, 'Reputacja': reputation})

# Zamknięcie przeglądarki
driver.quit()
