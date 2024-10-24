# data_extractor.py
from selenium.webdriver.common.by import By

def extract_products(driver) -> list[dict]:
    product_list = []
    products = driver.find_elements(By.CLASS_NAME, 'Bm3ON')

    for product in products:
        try:
            name = product.find_element(By.CLASS_NAME, 'RfADt').text
            price = product.find_element(By.CLASS_NAME, 'aBrP0').text
            link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            product_list.append({
                'name': name,
                'price': price,
                'link': link
            })
        except Exception as e:
            print(f"Error extracting product: {e}")
    
    return product_list