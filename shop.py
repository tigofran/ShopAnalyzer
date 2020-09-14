from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from prettytable import PrettyTable
import re

print('Termo a pesquisar: ', end='')
keyword = input()
cnt_url= "https://www.continente.pt/pt-pt/public/Pages/searchresults.aspx?k=" + keyword #+ "#/?pl=xx"
pd_url= "https://mercadao.pt/store/pingo-doce/search?queries=" + keyword
auc_url= "https://www.auchan.pt/Frontoffice/search/" + keyword

options = webdriver.ChromeOptions()
options.add_argument("headless") #comentar esta linha para o browser aparecer
options.add_argument("--log-level=3")  #apenas mostra avisos fatais na consola
options.add_experimental_option('excludeSwitches', ['enable-logging']) #elimina o aviso devtools
bro = webdriver.Chrome('D:\Tiago\OneDrive - Universidade de Lisboa\Documentos\chromedriver.exe', options=options)

#continente
cnt_response = bro.get(cnt_url)
cnt_list = bro.find_elements_by_class_name('productItem')
print('Encontrei {0} artigos no continente.'.format(len(cnt_list)))

t_cnt= PrettyTable(['Titulo', 'Marca', 'Quantidade', 'Preco1', 'Preco2'])

for item in cnt_list[:10]:
    prod_title = item.find_element_by_class_name('title').text
    prod_brand = item.find_element_by_class_name('type').text
    prod_quantity = item.find_element_by_class_name('subTitle').text
    prod_price_main = item.find_element_by_class_name('priceFirstRow').text
    prod_price_second = item.find_element_by_class_name('priceSecondRow').text

    #print('titulo: {0} | marca: {1} | quantidade: {2} | preco_1: {3} | preco_2: {4}'.format(prod_title, prod_brand, prod_quantity, prod_price_main, prod_price_second))
    
    t_cnt.add_row([prod_title, prod_brand, prod_quantity, prod_price_main, prod_price_second])
print(t_cnt)

#pingo doce
pd_response = bro.get(pd_url)
pd_list = bro.find_elements_by_tag_name('pdo-product-item')
print('Encontrei {0} artigos no pingo doce.'.format(len(pd_list)))

t_pd = PrettyTable(['Titulo','Quantidade','Preco1','Preco2'])

for item in pd_list[:10]:
    prod_title = item.find_element_by_tag_name('h3').text
    prod_quantity = item.find_element_by_tag_name('pdo-product-price-per-unit').text.split('|')[0]
    prod_price_main = item.find_element_by_tag_name('pdo-product-price-tag').find_element_by_tag_name('span').text
    prod_price_second = item.find_element_by_tag_name('pdo-product-price-per-unit').text.split('|')[1]

    #print('titulo: {0} |  quantidade: {2} | preco_1: {3} | preco_2: {4}'.format(prod_title, prod_quantity, prod_price_main, prod_price_second))
    
    t_pd.add_row([prod_title, prod_quantity, prod_price_main, prod_price_second])
print(t_pd)

#auchan
auc_response = bro.get(auc_url)
auc_list = bro.find_elements_by_class_name('product-item-border')
print('Encontrei {0} artigos no auchan.'.format(len(auc_list)))

t_auc = PrettyTable(['Titulo','Quantidade','Preco1','Preco2'])

for item in auc_list[:10]:
    prod_desc = item.find_element_by_tag_name('h3').text
    if re.match('^[0-9]+ ?[A-Za-z]+$', prod_desc.split(' ')[-2] + prod_desc.split(' ')[-1]) is not None:
        prod_title = ' '.join(prod_desc.split(' ')[:-2])
        prod_quantity = ''.join(prod_desc.split(' ')[-2:])
    else:
        prod_title = ' '.join(prod_desc.split(' ')[:-1])
        prod_quantity = ''.join(prod_desc.split(' ')[-1:])
    prod_price_main = item.find_element_by_class_name('product-item-price ').text
    prod_price_second = item.find_element_by_class_name('product-item-actions-column').text

    #print('titulo: {0} |  quantidade: {1} | preco_1: {2} | preco_2: {3}'.format(prod_title, prod_quantity, prod_price_main, prod_price_second))
    
    t_auc.add_row([prod_title, prod_quantity, prod_price_main, prod_price_second])
print(t_auc)