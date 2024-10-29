import os
import sys
from sqlite3 import IntegrityError
import time
import json
import pandas as pd
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session

# Path Append
sys.path.append(os.path.abspath(os.curdir))


from endpoint import crud
from endpoint.model import ProductModel
from src.provider.lazada.schema import LAZADA_PRODUCTS_SCHEMA_MAPPING, LAZADA_REVIEWS_SCHEMA_MAPPING
from src.setup_driver import setup_driver
from src.database.connector import SessionLocal
from src.database.schema import Product

def get_products(driver, keyword: str) -> pd.DataFrame:
    """
    Scrape Lazada page and extract product information.
    """
    driver.get(f"https://www.lazada.vn/catalog/?ajax=true&isFirstRequest=true&page=1&q={keyword}")
    time.sleep(30)

    json_element = driver.find_element(By.TAG_NAME, "pre")
    json_data = json.loads(json_element.text).get('mods').get('listItems')

    filtered_data_list = []
    for item in json_data: 
        filtered_data = {
            new_key: item[old_key]
            for old_key, new_key in LAZADA_PRODUCTS_SCHEMA_MAPPING.items()
            if old_key in item
        }
        filtered_data_list.append(filtered_data)
    
    return pd.DataFrame(filtered_data_list)


# def scrape_products(driver, keyword: str) -> list[dict]:
#     """
#     Scrape Lazada page and extract product information.
#     """
#     # Load the Lazada page
#     driver.get(f"https://www.lazada.vn/catalog/?q={keyword}")
#     time.sleep(10)

#     # Scroll through the page
#     scroll_page(driver)

#     # Extract product data
#     products = driver.find_elements(By.CLASS_NAME, 'Bm3ON')
#     product_list = []
#     for product in products:
#         try:
#             name = product.find_element(By.CLASS_NAME, 'RfADt').text
#             price = product.find_element(By.CLASS_NAME, 'aBrP0').text
#             link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
#             product_list.append({'name': name, 'price': price, 'link': link})
#         except Exception as e:
#             print(f"Error extracting product: {e}")
#     return product_list


# def scroll_page(driver):
#     """
#     Scrolls through the Lazada page to load more products.
#     """
#     SCROLL_PAUSE_TIME = 2
#     last_height = driver.execute_script("return document.body.scrollHeight")

#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(SCROLL_PAUSE_TIME)
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height


# def process_data(driver, products: list[dict]) -> pd.DataFrame:
#     """
#     Process the scraped product data, adding any additional information.
#     """
#     processed_data = []
#     for item in products:
#         driver.get(item['link'])
#         time.sleep(20)
#         try:
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             item['average_score'] = soup.find('span', class_='score-average').text
#             processed_data.append(item)
#         except Exception as e:
#             print(f"Error processing product page: {e}")

#     df = pd.DataFrame(processed_data)
#     df = df.rename(columns=LAZADA_PRODUCTS_SCHEMA_MAPPING)
#     return df

def get_reviews(driver, product_id: int) -> pd.DataFrame:
    """
    Scrape Lazada page and extract product reviews.
    """
    driver.get(f"https://my.lazada.vn/pdp/review/getReviewList?itemId={product_id}")
    time.sleep(10)

    json_element = driver.find_element(By.TAG_NAME, "pre")
    json_data = json.loads(json_element.text).get('model').get('items')

    review_list = []
    for review in json_data:
        filtered_data = {
            new_key: review[old_key]
            for old_key, new_key in LAZADA_REVIEWS_SCHEMA_MAPPING.items()
            if old_key in review
        }
        review_list.append(filtered_data)
    return pd.DataFrame(review_list)

def load_data_to_db(df: pd.DataFrame, db: Session):
    """
    Load the processed data into the database, only if the product doesn't already exist.
    """

    df = df.where(pd.notnull(df), None)
    for _, row in df.iterrows():
    
        product_data = row.to_dict()
        validated_data = ProductModel(**product_data)
        
        crud.upsert_item(db, validated_data)


def run_scraper():
    DRIVER_PATH = 'drivers/chromedriver-win64/chromedriver.exe'
    
    # Setup WebDriver
    driver = setup_driver(DRIVER_PATH)

    # Step 1: Scrape the product data
    keyword = input("Enter a product to search: ")
    products = get_products(driver, keyword)

    # Step 3: Load the processed data into the database
    db = SessionLocal()
    load_data_to_db(products, db)

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    run_scraper()
