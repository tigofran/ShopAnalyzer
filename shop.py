from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from prettytable import PrettyTable

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
print('Encontrei {0} artigos!'.format(len(cnt_list)))

t= PrettyTable(['Titulo', 'Marca', 'Quantidade', 'Preco1', 'Preco2'])

for item in cnt_list[:10]:
    prod_title = item.find_element_by_class_name('title').text
    prod_brand = item.find_element_by_class_name('type').text
    prod_quantity = item.find_element_by_class_name('subTitle').text
    prod_price_main = item.find_element_by_class_name('priceFirstRow').text
    prod_price_second = item.find_element_by_class_name('priceSecondRow').text

    """ print('titulo: %s' % prod_title)
    print('marca: %s' %prod_brand)
    print('quantidade: %s' %prod_quantity)
    print('preco principal: |%s|' %prod_price_main)
    print('preco secundario: |%s|' %prod_price_second) """



    #print('titulo: {0} | marca: {1} | quantidade: {2} | preco_1: {3} | preco_2: {4}'.format(prod_title, prod_brand, prod_quantity, prod_price_main, prod_price_second))
    t.add_row([prod_title, prod_brand, prod_quantity, prod_price_main, prod_price_second])
print(t)




