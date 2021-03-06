from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable
import re
import os
import sys
from flask import Flask, render_template, request, redirect

#print('Termo a pesquisar: ', end='')

options = webdriver.ChromeOptions()
options.add_argument("headless") #comentar esta linha para o browser aparecer
options.add_argument("--log-level=3")  #apenas mostra avisos fatais na consola
options.add_experimental_option('excludeSwitches', ['enable-logging']) #elimina o aviso devtools
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('user-agent=josesantos1987')


chrome_bin = os.environ.get('GOOGLE_CHROME_BIN', None)
chromedriver_path = os.environ.get('CHROMEDRIVER_PATH',None)
options.binary_location = chrome_bin


bro = webdriver.Chrome(chromedriver_path, options=options)
#continente
def prices_continente(keyword):
    cnt_url= "https://www.continente.pt/pt-pt/public/Pages/searchresults.aspx?k=" + keyword
    cnt_response = bro.get(cnt_url)
    bro.find_element_by_xpath("/html").click()
    cnt_list = bro.find_elements_by_class_name('productItem')
    print('Encontrei {0} artigos no continente.'.format(len(cnt_list)), flush=True)

    t_cnt= PrettyTable(['Titulo', 'Marca', 'Quantidade', 'Preco1', 'Preco2'])

    for item in cnt_list:
        prod_title = item.find_element_by_class_name('title').text
        prod_brand = item.find_element_by_class_name('type').text
        prod_quantity = item.find_element_by_class_name('subTitle').text
        prod_price_main = item.find_element_by_class_name('priceFirstRow').text
        prod_price_second = item.find_element_by_class_name('priceSecondRow').text

        #print('titulo: {0} | marca: {1} | quantidade: {2} | preco_1: {3} | preco_2: {4}'.format(prod_title, prod_brand, prod_quantity, prod_price_main, prod_price_second))
        
        t_cnt.add_row([prod_title, prod_brand, prod_quantity, prod_price_main, prod_price_second])
    return t_cnt

#pingo doce
def prices_pingodoce(keyword):  
    pd_url= "https://mercadao.pt/store/pingo-doce/search?queries=" + keyword  
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
    return t_pd


#auchan
def prices_auchan(keyword):
    auc_url= "https://www.auchan.pt/Frontoffice/search/" + keyword
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
    return t_auc


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/process", methods = ["GET", "POST"])
def process_site():
    if len(request.form['pesquisa']) == 0:
        return redirect('/')
    if request.form["loja"] == "Continente":
        nexturl = '/c/'
    elif request.form["loja"] == "Pingo Doce":
        nexturl = '/p/'
    else:
        nexturl = '/a/'
    nexturl += request.form['pesquisa']
    return redirect(nexturl)

    
    
@app.route("/c/<keyword>")
def get_continente(keyword):
    return prices_continente(keyword).get_html_string()
@app.route("/p/<keyword>")
def get_pingodoce(keyword):
    return prices_pingodoce(keyword).get_html_string()
@app.route("/a/<keyword>")
def get_auchan(keyword):
    return prices_auchan(keyword).get_html_string()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port = "5000",threaded=True)
