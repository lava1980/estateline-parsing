import bs4
import os
import re


def get_page_data():
    # driver.get(url)
    # html = driver.page_source

    html = open(os.getcwd() + '/page.html', 'r')    
    soup = bs4.BeautifulSoup(html, features='lxml')
    obj_name = soup.find('div', class_='halfed').find_all('li')[3].find('span', class_='dd').get_text()
    block_list = soup.find_all(class_=re.compile("dl-in-card"))[2:]
    company_name_list = soup.find_all('h2', class_=re.compile("card-woLi"))
    if len(block_list) != len(company_name_list):
        raise Exception('Не совпадает число названий компаний с числом блоков')

    print('Число названий ' + str(len(company_name_list)))

    for block in block_list:
        index = block_list.index(block)
        
        company_name = company_name_list[index].find_all('a')[-1].get_text()
        form = company_name_list[index].find_all('span')[-1].get_text()
        
        
        print(company_name, form)


    

    #print(block_list[0])    
    print(obj_name)






def get_block_data(block):    
    items_list = block.find_all('li')
    for item in items_list:
        pass
        # Пройтись по значениям и сделать проверку, или есть поле. Например, или есть поле имейл.



block = bs4.BeautifulSoup(open('block.html', 'r'), features='lxml')
get_block_data(block)



#get_page_data()