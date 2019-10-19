from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import bs4
import logging
import openpyxl 
import os
import re
import time

from config import *
from utils import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'estate.log'
                    )

base_url = 'http://www.estateline.ru/projects/'

options = webdriver.FirefoxOptions()
options.headless == False

driver = webdriver.Firefox(options=options)

def auth():
    logging.info('Старт авторизации')
    email, password = AUTH_DATA
    driver.get(base_url + REGION_LIST[0])
    driver.find_element_by_xpath('//div[@id="topAuth"]/div/div/a').click()
    driver.find_element_by_id('u_email').send_keys(email)
    driver.find_element_by_id('u_password').send_keys(password)
    driver.find_element_by_xpath('//div[@class="bg"]/a/span').click()

def get_category(category):
    url = base_url + category
    driver.get(url)
    

def get_category_html(url):
    driver.current_window_handle
    return driver.page_source

    












def main():
    # auth()
    # get_category('residential')
    get_page_data()
    






if __name__ == "__main__":
    main()
