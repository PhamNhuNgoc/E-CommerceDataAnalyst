from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import DRIVER_PATH

def setup_driver(driver_path: str = DRIVER_PATH):
    chrome_options = Options()
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    return driver
