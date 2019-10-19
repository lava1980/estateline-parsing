import bs4
import openpyxl
import os
import re


def get_page_data():
    # driver.get(url)
    # html = driver.page_source

    html = open(os.getcwd() + '/page.html', 'r')    
    soup = bs4.BeautifulSoup(html, features='lxml')

    obj_name = soup.find(
        'div', class_='halfed').find_all('li')[3].find('span', class_='dd').get_text()  
    obj_name = clean_text(obj_name) 

    block_list = soup.find_all(class_=re.compile("dl-in-card"))[2:]
    company_name_list = soup.find_all('h2', class_=re.compile("card-woLi"))
    if len(block_list) != len(company_name_list):
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


def clean_text(text):
    text = text.strip()
    if '\xa0' in text:
        text = text.replace('\xa0', ' ')
    return text


def get_block_data(block):    
    fold_list = [
        'Местоположение', 'Адрес', 'Телефон', 'Эл. почта', 'Сайт', 'ИНН', 'Описание']
    items_list = block.find_all('li')
    block_data = []
    for fold in fold_list:        
        for item in items_list:
            try:
                fold_name = clean_text(
                    item.find('span', class_='dt').get_text()
                    )
                fold_value = clean_text(
                    item.find('span', class_='dd').get_text()
                    )
            except AttributeError:
                continue
            
            if fold == fold_name:
                block_data.append(fold_value)
                break
            # Если прошлись по всем строкам и не нашли, присваиваем значение по умолчанию
            if items_list.index(item) == (len(items_list) - 1):
                block_data.append('Не найдено поле ' + fold)

    return block_data


def write_html_file(html):
    with open('page.html', 'w') as f:
        f.write(html)

            
def write_row_to_excel(data):    
    wb = openpyxl.Workbook()    
    wb.create_sheet(title = 'База объектов', index = 0)    
    sheet = wb['База объектов']
    
    town, adres, phone, email, site, inn, description = get_block_data(data)
    
        
    sheet.append([town, adres, phone, email, site, inn, description])
    wb.save('objects.xlsx')
         
            



# block = bs4.BeautifulSoup(open('block.html', 'r'), features='lxml')
# get_block_data(block)
# write_row_to_excel(block)


if __name__ == "__main__":
    get_page_data()
