import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
 
def start_browser():
    """Chrome browser ko open karta hai."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Agar browser window nahi dekhni to neeche wali line uncomment karein:
    # options.add_argument("--headless")
 
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
 
 
def search_product(driver, product_name):
    """Amazon open karke product search karta hai."""
    driver.get("https://www.amazon.com")
 
    # Step 4 (pehle): Search box load hone ka wait
    wait = WebDriverWait(driver, 15)
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
 
    # Step 2: Search box mein product name type karna
    search_box.clear()
    search_box.send_keys(product_name)
 
    # Step 3: Search button click karna (ya Enter dabana)
    search_box.send_keys(Keys.ENTER)
 
    # Step 4: Results page load hone ka wait
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
    )
    time.sleep(2)  # extra safety wait
 
 
def scroll_page(driver, scroll_times=5):
    """Step 5: Page ko scroll karta hai taake zyada products load hon."""
    for i in range(scroll_times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # naye elements load hone ka time dena
 
 
def extract_products(driver):
    """Step 6: Har product ka naam, price, rating extract karta hai."""
    products_data = []
 
    # Amazon har search result ko is container mein rakhta hai
    items = driver.find_elements(By.CSS_SELECTOR, "div.s-result-item[data-component-type='s-search-result']")
 
    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, "h2 span").text
        except:
            name = "N/A"
 
        try:
            price_whole = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
            price_fraction = item.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
            price = f"{price_whole}.{price_fraction}"
        except:
            price = "N/A"
 
        try:
            rating = item.find_element(By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("innerHTML")
        except:
            rating = "N/A"
 
        # Khaali entries skip karna
        if name != "N/A":
            products_data.append({
                "Name": name,
                "Price": price,
                "Rating": rating
            })
 
    return products_data
 
 
def save_to_csv(products_data, filename="amazon_products.csv"):
    """Step 7: Data ko CSV file mein save karta hai."""
    if not products_data:
        print("Koi data nahi mila save karne ke liye.")
        return
 
    keys = products_data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(products_data)
 
    print(f"Data '{filename}' mein save ho gaya. Total products: {len(products_data)}")
 
 
def main():
    product_name = input("Kaunsa product search karna hai? ")
 
    driver = start_browser()
 
    try:
        # Step 1 + 2 + 3 + 4
        search_product(driver, product_name)
 
        # Step 5
        scroll_page(driver, scroll_times=5)
 
        # Step 6
        products_data = extract_products(driver)
 
        # Step 7
        save_to_csv(products_data)
 
    finally:
        driver.quit()  # Browser ko close karna zaroori hai
 
 
if __name__ == "__main__":
    main()