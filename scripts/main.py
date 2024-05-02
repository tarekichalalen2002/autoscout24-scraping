import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager,ChromeType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd

columns = ["model_name", "extended_name", "price", "price_judgement", "kilometers", "transmission", "release_date", "fuel", "power", "owner", "owner_adress"]
df = pd.DataFrame(columns=columns)


# Chrome driver path 
path = "C:\\Users\\windows\\Desktop\\chromedriver-win64\\chromedriver.exe"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/537.36"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(f"user-agent={user_agent}")
service = ChromeService(executable_path=path)
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()
companies_urls = [
    "https://www.autoscout24.fr/voiture/audi/",
    "https://www.autoscout24.fr/voiture/bmw/",
    "https://www.autoscout24.fr/voiture/citroen/",
    "https://www.autoscout24.fr/voiture/dacia/",
    "https://www.autoscout24.fr/voiture/ferrari/",
    "https://www.autoscout24.fr/voiture/ford/",
    "https://www.autoscout24.fr/voiture/morgan/",
    "https://www.autoscout24.fr/voiture/peugeot/",
    "https://www.autoscout24.fr/voiture/porsche/",
    "https://www.autoscout24.fr/voiture/renault/",
    "https://www.autoscout24.fr/voiture/tesla/",
    "https://www.autoscout24.fr/voiture/toyota/"
]
for url_company in companies_urls:
    driver.get(url_company)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter tout')]")))
        driver.find_element(By.XPATH, "//button[contains(text(), 'Accepter tout')]").click()
        time.sleep(1)
    except:
        pass
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Afficher tout')]")))
        driver.find_element(By.XPATH, "//button[contains(text(), 'Afficher tout')]").click()
    except:
        pass
    
    time.sleep(1)

    models = driver.find_elements(By.XPATH, "//div[contains(@class, 'TopModels_model__zd0sT')]")
    if models:
        model = models[0]
        for i in range(0,len(models)):
            driver.execute_script("arguments[0].click();", model)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(0.5)

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Afficher toutes les annonces')]")))
            driver.find_element(By.XPATH, "//span[contains(text(), 'Afficher toutes les annonces')]").click()

            time.sleep(1)


            offers = driver.find_elements(By.XPATH, "//article[contains(@class, 'cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7')]")
            for offer in offers:
                model_name=""
                extended_name=""
                price=""
                price_judgement=""
                kilometers = ""
                transmission = ""
                release_date = ""
                fuel = ""
                power = ""
                try:
                    model_name = offer.find_element(By.XPATH, ".//h2").text.split("\n")[0]
                except:
                    pass
                
                try:
                    extended_name = offer.find_element(By.XPATH, ".//span[contains(@class, 'ListItem_version__5EWfi')]").text
                except:
                    pass
                
                try:
                    price = offer.find_element(By.XPATH, ".//p[contains(@class, 'Price_price__APlgs PriceAndSeals_current_price__ykUpx')]").text
                except:
                    pass
                
                try:
                    price_judgement = offer.find_element(By.XPATH, ".//div[contains(@class, 'scr-price-label PriceAndSeals_price_info__hXkBr')]/p").text
                except:
                    pass
                
                try:
                    kilometers = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-mileage_road')]").text
                except:
                    pass
                
                try:
                    transmission = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-transmission')]").text
                except:
                    pass
                
                try:
                    release_date = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-calendar')]").text
                except:
                    pass
            
                try:
                    fuel = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-gas_pump')]").text
                except:
                    pass
                
                try:
                    power = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-speedometer')]").text
                except:
                    pass
                new_row = {
                    "model_name": model_name, 
                    "extended_name": extended_name,
                    "price": price,
                    "price_judgement": price_judgement,
                    "kilometers": kilometers,
                    "transmission": transmission,
                    "release_date": release_date,
                    "fuel": fuel,
                    "power": power,
                }
                new_row_df = pd.DataFrame([new_row])
                df = pd.concat([df, new_row_df], ignore_index=True)
            suivant_button = None
            try:
                suivant_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Aller à la page suivante')]")))
            except:
                pass
            if suivant_button:
                while suivant_button.is_enabled():
                    suivant_button.click()
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                    time.sleep(0.5)
                    offers = driver.find_elements(By.XPATH, "//article[contains(@class, 'cldt-summary-full-item listing-impressions-tracking list-page-item ListItem_article__qyYw7')]")
                    for offer in offers:
                        model_name=""
                        extended_name=""
                        price=""
                        price_judgement=""
                        kilometers = ""
                        transmission = ""
                        release_date = ""
                        fuel = ""
                        power = ""
                        try:
                            model_name = offer.find_element(By.XPATH, ".//h2").text.split("\n")[0]
                        except:
                            pass
                        
                        try:
                            extended_name = offer.find_element(By.XPATH, ".//span[contains(@class, 'ListItem_version__5EWfi')]").text
                        except:
                            pass
                        
                        try:
                            price = offer.find_element(By.XPATH, ".//p[contains(@class, 'Price_price__APlgs PriceAndSeals_current_price__ykUpx')]").text
                        except:
                            pass
                        
                        try:
                            price_judgement = offer.find_element(By.XPATH, ".//div[contains(@class, 'scr-price-label PriceAndSeals_price_info__hXkBr')]/p").text
                        except:
                            pass
                        
                        try:
                            kilometers = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-mileage_road')]").text
                        except:
                            pass
                        
                        try:
                            transmission = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-transmission')]").text
                        except:
                            pass
                        
                        try:
                            release_date = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-calendar')]").text
                        except:
                            pass
                    
                        try:
                            fuel = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-gas_pump')]").text
                        except:
                            pass
                        
                        try:
                            power = offer.find_element(By.XPATH, ".//span[contains(@data-testid, 'VehicleDetails-speedometer')]").text
                        except:
                            pass
                        new_row = {
                            "model_name": model_name, 
                            "extended_name": extended_name,
                            "price": price,
                            "price_judgement": price_judgement,
                            "kilometers": kilometers,
                            "transmission": transmission,
                            "release_date": release_date,
                            "fuel": fuel,
                            "power": power,
                        }
                        new_row_df = pd.DataFrame([new_row])
                        df = pd.concat([df, new_row_df], ignore_index=True)
                    suivant_button = None
                    try:
                        suivant_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Aller à la page suivante')]")))
                    except:
                        pass
                    if not suivant_button:
                        break
            driver.get(url_company)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(1)
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accepter tout')]")))
                driver.find_element(By.XPATH, "//button[contains(text(), 'Accepter tout')]").click()
                time.sleep(1)
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Afficher tout')]")))
                driver.find_element(By.XPATH, "//button[contains(text(), 'Afficher tout')]").click()
            except:
                pass
            model = driver.find_elements(By.XPATH, "//div[contains(@class, 'TopModels_model__zd0sT')]")[i]
            time.sleep(1)

            df.to_csv(f"{url_company[35:len(url_company)-1]}-{i}.csv")
            columns = ["model_name", "extended_name", "price", "price_judgement", "kilometers", "transmission", "release_date", "fuel", "power", "owner", "owner_adress"]
            df = pd.DataFrame(columns=columns)