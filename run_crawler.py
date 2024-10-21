# run_crawler.py
from scraper.lazada_scraper import LazadaScraper
from scraper.data_extractor import extract_products
import json
import os

def save_data(data, keyword):
    os.makedirs("data", exist_ok=True)
    # Sanitize the keyword to create a safe filename
    keyword_safe = keyword.replace(" ", "_").replace("%20", "_")
    filename = f"shopee_data_{keyword_safe}.json"
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    # Path to the browser driver
    DRIVER_PATH = 'drivers/chromedriver-win64/chromedriver.exe'
    
    # Initialize the scraper
    scraper = LazadaScraper(DRIVER_PATH)
    
    # Load the Lazada page
    keyword = input("Enter a product to search: ")
    scraper.load_page("https://www.lazada.vn/catalog/?q=" + keyword)
    
    # Scroll through the page to load all products
    scraper.scroll_page()
    
    # Extract product data
    products = extract_products(scraper.driver)
    
    # Save data to a file
    save_data(products, keyword)
    
    # Close the scraper
    scraper.close()

if __name__ == "__main__":
    main()
