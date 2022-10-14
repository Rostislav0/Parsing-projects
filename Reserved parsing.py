import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://www.reserved.com/ru/ru/sale/men/bestsellers-ru'

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
           'accept': '*/*'}

FILE = 'reserved.csv'
def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = soup.find_all('figure')
    all_info = []
    for product in products:

        all_info.append({
            "name_of_product": product.find('figcaption', class_="es-product-name").get_text(),
            "image_of_product": product.find('img').get('data-src'),
            "price_of_product": ''.join(product.find('p', class_="es-discount-price").get_text().split()),
            "url_of_product": product.find('a', class_="es-product-photo").get('href')




        })

    return all_info


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Name', 'Preview', 'Price', 'URL'])
        for item in items:
            writer.writerow([item["name_of_product"], item["image_of_product"], item["price_of_product"], item["url_of_product"]])



def parse():
    html = get_html(URL)
    if html.status_code == 200:

        save_file(get_content(html.text), FILE)
        os.startfile(FILE)
    else:
        print("Error")

parse()