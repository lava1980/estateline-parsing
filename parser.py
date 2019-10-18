from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import time
from config import *
import bs4
import openpyxl 
import logging

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

    
def write_html_file(html):
    with open('page.html', 'w') as f:
        f.write(html)




def get_page_data():
    # driver.get(url)
    # html = driver.page_source

    html = open(os.getcwd() + '/page.html', 'r')
    
    soup = bs4.BeautifulSoup(html, features='lxml')
    name = soup.find('div', class_='halfed').find_all('li')[3].get_text()
    print(name)








def main():
    # auth()
    # get_category('residential')
    get_page_data()
    






if __name__ == "__main__":
    main()
