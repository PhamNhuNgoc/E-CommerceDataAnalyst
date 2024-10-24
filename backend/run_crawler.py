# run_crawler.py
from scraper.lazada_scraper import LazadaScraper
from scraper.data_extractor import extract_products
from scraper.schema import LAZADA_PRODUCTS_SCHEMA_MAPPING
from typing import Annotated
from sqlalchemy.orm import Session
# from pydantic import BaseModel, Field
# from fastapi import FastAPI, Depends, HTTPException, Path

import json
import os
import pandas as pd
from selenium.webdriver.common.by import By


def save_data(data, keyword):
    os.makedirs("data", exist_ok=True)
    # Sanitize the keyword to create a safe filename
    keyword_safe = keyword.replace(" ", "_").replace("%20", "_")
    filename = f"lazada_data_{keyword_safe}.json"
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def process_data(data) -> pd.DataFrame:
    DRIVER_PATH = 'drivers/chromedriver-win64/chromedriver.exe'
    scraper = LazadaScraper(DRIVER_PATH)

    list_data: list[dict] = []

    for item in data:
        scraper.load_page(item['link'])
        item['average_score'] = scraper.find_element(By.CLASS_NAME, 'average_score').text
        list_data.append(item)

    return pd.DataFrame(data).rename(LAZADA_PRODUCTS_SCHEMA_MAPPING)

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

    # Process the data
    print(process_data(products))
    
    # # Save data to a file
    # save_data(products, keyword)
    
    # Close the scraper
    scraper.close()

if __name__ == "__main__":
    main()
