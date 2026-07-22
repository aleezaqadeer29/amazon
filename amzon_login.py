import time
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def start_browser():
    """Chrome browser setup in Headless Mode for CI/CD Pipeline."""
    options = webdriver.ChromeOptions()
    
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def scrape_data(driver):
    """Website se quotes aur authors extract karta hai."""
    print("Navigating to target website...")
    driver.get("https://quotes.toscrape.com")
    time.sleep(2)

    scraped_data = []
    quote_elements = driver.find_elements(By.CSS_SELECTOR, "div.quote")

    for item in quote_elements:
        try:
            text = item.find_element(By.CSS_SELECTOR, "span.text").text
        except:
            text = "N/A"

        try:
            author = item.find_element(By.CSS_SELECTOR, "small.author").text
        except:
            author = "N/A"

        if text != "N/A":
            scraped_data.append({
                "Quote": text,
                "Author": author
            })

    return scraped_data


def save_to_csv(data, filename="amazon_products.csv"):
    """Data ko CSV file mein save karta hai (Pipeline Artifact output ke liye)."""
    if not data:
        print("No data found to save.")
        return

    keys = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data successfully saved to '{filename}'. Total records: {len(data)}")


def main():
    print("Starting Automated Scraper Pipeline Test...")
    driver = start_browser()

    try:
        data = scrape_data(driver)
        save_to_csv(data)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()