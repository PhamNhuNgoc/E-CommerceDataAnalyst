# shopee_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

class LazadaScraper:
    def __init__(self, driver_path):
        chrome_options = Options()
        chrome_options.add_argument("--disable-gpu")
        time.sleep(2)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
        # self.driver = webdriver.Chrome(service=Service(driver_path))
        self.wait = WebDriverWait(self.driver, 10)
        logging.basicConfig(filename='logs/crawler.log', level=logging.INFO)
        
    def chrome_options(self):
        options = webdriver.ChromeOptions()
        return options

    def load_page(self, url):
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Bm3ON')))
    
    def scroll_page(self):
        SCROLL_PAUSE_TIME = 2
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def close(self):
        self.driver.quit()
