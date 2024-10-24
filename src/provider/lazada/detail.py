import os
import json
import time
import pandas as pd
from selenium.webdriver.common.by import By
from provider.lazada.schema import LAZADA_PRODUCTS_SCHEMA_MAPPING
from setup_driver import setup_driver
from sqlalchemy.orm import Session
from database.connection import get_db
from database.schema import Product

def scrape_products(driver, keyword: str) -> list[dict]:
    """
    Scrape Lazada page and extract product information.
    """
    # Load the Lazada page
    driver.get(f"https://www.lazada.vn/catalog/?q={keyword}")
    time.sleep(10)

    # Scroll through the page
    scroll_page(driver)

    # Extract product data
    products = driver.find_elements(By.CLASS_NAME, 'Bm3ON')
    product_list = []
    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, 'RfADt').text
            price = product.find_element(By.CLASS_NAME, 'aBrP0').text
            link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product_list.append({'name': name, 'price': price, 'link': link})
        except Exception as e:
            print(f"Error extracting product: {e}")
    return product_list


def scroll_page(driver):
    """
    Scrolls through the Lazada page to load more products.
    """
    SCROLL_PAUSE_TIME = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def process_data(driver, products: list[dict]) -> pd.DataFrame:
    """
    Process the scraped product data, adding any additional information.
    """
    processed_data = []
    for item in products:
        driver.get(item['link'])
        try:
            item['average_score'] = driver.find_element(By.CLASS_NAME, 'average_score').text
            processed_data.append(item)
        except Exception as e:
            print(f"Error processing product page: {e}")

    df = pd.DataFrame(processed_data)
    df = df.rename(columns=LAZADA_PRODUCTS_SCHEMA_MAPPING)
    return df


def load_data_to_db(df: pd.DataFrame, db: Session):
    """
    Load the processed data into the database.
    """
    for _, row in df.iterrows():
        product = Product(
            name=row['product_name'],
            price=row['product_price'],
            link=row['product_url'],
            average_score=row.get('average_rating', None)
        )
        db.add(product)
    db.commit()
    print("Data successfully loaded into the database.")



def run_scraper():
    DRIVER_PATH = 'drivers/chromedriver-win64/chromedriver.exe'
    
    # Setup WebDriver
    driver = setup_driver(DRIVER_PATH)

    # Step 1: Scrape the product data
    keyword = input("Enter a product to search: ")
    products = scrape_products(driver, keyword)

    # Step 2: Process the scraped data
    processed_df = process_data(driver, products)

    # Step 3: Load the processed data into the database
    db = get_db()
    load_data_to_db(processed_df, db)

    # Close the WebDriver
    driver.quit()
