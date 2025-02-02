from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from logger import logger
import os

def getDriver(driver_path):
    if not os.path.exists(driver_path):
        logger.error(f"Driver not found at path: {driver_path}")
        raise FileNotFoundError(f"Driver not found at path: {driver_path}")
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    return driver