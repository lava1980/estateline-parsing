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
import sys
import time

from config import *
from utils import *


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level = logging.INFO,
                    filename = 'estate.log'
                    )

base_url = 'http://www.estateline.ru/projects/'

geckodriver = '/usr/local/bin/geckodriver'
options = webdriver.FirefoxOptions()
options.headless == True

driver = webdriver.Firefox(executable_path=geckodriver, options=options)

    

def auth():
    # raise Exception('Тестовое исключение')
    logging.info('Старт авторизации')
    email, password = AUTH_DATA
    driver.get(base_url)
    driver.find_element_by_xpath('//div[@id="topAuth"]/div/div/a').click()
    driver.find_element_by_id('u_email').send_keys(email)
    driver.find_element_by_id('u_password').send_keys(password)
    driver.find_element_by_xpath('//div[@class="bg"]/a/span').click()
    
    driver.find_element_by_xpath('//td[@id="center"]/ul/li/a/span').click()
    driver.find_element_by_xpath(f'//ul[@class="dropbox"]/li[{REGION}]/div/a').click()


def get_category_html(category, counter):
    url = base_url + category + '/?stPage=' + str(counter)
    driver.get(url)
    return driver.page_source


def get_page_data(url):
    driver.get(url)
    html = driver.page_source

    # html = open(os.getcwd() + '/page.html', 'r')    
    soup = bs4.BeautifulSoup(html, features='lxml')

    obj_name = soup.find(
        'div', class_='halfed').find_all('li')[3].find('span', class_='dd').get_text()  
    obj_name = clean_text(obj_name) 

    block_list = soup.find_all(class_=re.compile("dl-in-card-16"))
    company_name_list = soup.find_all('h2', class_=re.compile("card-woLi"))
    
    if len(company_name_list) == 0:
        raise Exception('Нет доступа к странице ' + url)

    if len(block_list) != len(company_name_list):
        logging.info('Длина списка блоков = ' + str(len(block_list)) + '. Длина списка названий = ' + str(len(company_name_list)))
        raise Exception('Не совпадает число названий компаний с числом блоков')

    print('Число названий ' + str(len(company_name_list)))
    data_list = []

    for block in block_list:
        index = block_list.index(block)        
        company_name = clean_text(
            company_name_list[index].find_all('a')[-1].get_text()
            )
        form = clean_text(
            company_name_list[index].find_all('span')[-1].get_text()
            )
        block_data_list = get_block_data(block)
        block_data_list.insert(0, company_name)
        block_data_list.insert(1, form) 
        block_data_list.insert(0, obj_name)
        data_list.append(block_data_list)             
        
    print(data_list)    
    return data_list

 
def main():
    auth()        
    for i in range(1, PAGES_PER_DAY//15 + 1):
        cat_html = get_category_html('residential', i)    
        links_list = get_cat_page_links(cat_html)
        for link in links_list:
            page_data = get_page_data(link)
            write_data_to_excel(page_data)
            



if __name__ == "__main__":
    try:
        main()
        # auth()
        # get_page_data('http://www.estateline.ru/project/39870/')
    except Exception as e:
        send_telegram_message('Возникло исключение: ' + str(e))