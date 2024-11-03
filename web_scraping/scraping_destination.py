import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

url = "https://www.google.com/search?q=du+l%E1%BB%8Bch+h%E1%BB%93+ch%C3%AD+minh&sca_esv=c7f8bf539794a7f6&rlz=1C1CHBF_enVN1128VN1128&sxsrf=ADLYWIIRBHeFm6lg510Um1jTokxvX12mKQ:1729089918801&udm=15&sa=X&ved=2ahUKEwjt-5PzkZOJAxVJrlYBHS3RJUgQxN8JegQIZxAz&biw=1536&bih=703&dpr=1.25"

# Selenium configuration
chrome_options = Options()
chrome_options.add_argument("start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url)

wait = WebDriverWait(driver, 10)

destinations_data = []

while True:
    try:
        expand_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(),"Điểm tham quan khác")]'))
        )
        expand_button.click()
        print("clicked on 'Điểm tham quan khác'.")

        time.sleep(3)
        # get list of destination
        destinations = driver.find_elements(by=By.XPATH,
                                            value='//div[contains(@class,"ZsAbe") and contains(@class,"EXH1Ce")]')

        for destination in destinations:
            try:
                # get destination's name
                destination_name = destination.find_element(by=By.CSS_SELECTOR, value='span.Yt787').text if destination.find_elements(by=By.CSS_SELECTOR, value='span.Yt787') else "N/A"

                # get destination's rating
                destination_rating = destination.find_element(by=By.CSS_SELECTOR, value='span.yi40Hd.YrbPuc').text if destination.find_elements(by=By.CSS_SELECTOR, value='span.yi40Hd.YrbPuc') else "N/A"

                # get destination's type
                destination_type = destination.find_element(by=By.CSS_SELECTOR, value='div.ZJjBBf.cyspcb.DH9lqb').text if destination.find_elements(by=By.CSS_SELECTOR, value='div.ZJjBBf.cyspcb.DH9lqb') else "N/A"

                # get destination's price
                destination_price = destination.find_element(by=By.CSS_SELECTOR, value='div.rDUZLd.JNI6Yb').text if destination.find_elements(by=By.CSS_SELECTOR, value='div.rDUZLd.JNI6Yb') else "N/A"

                destinations_data.append({
                    "name": destination_name,
                    "rating": destination_rating,
                    "type": destination_type,
                    "price": destination_price
                })

                print("Destination:", destination_name)
                print("Rating:", destination_rating)
                print("Destination type:", destination_type)
                print("Price:", destination_price)
                print("--------------------")
            except Exception as e:
                print(f"Error processing destination: {e}")

            print(f"Number of Destination: {len(destinations_data)}")
    except Exception as e:
        print(f"No more 'Điểm tham quan khác' button to press or Error: {e}")
        break


os.makedirs('../data', exist_ok=True)

with open('../data/destinations.json', 'w', encoding='utf-8') as json_file:
    json.dump(destinations_data, json_file, ensure_ascii=False, indent=4)


driver.quit()
