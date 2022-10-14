import time
from selenium import webdriver
from bs4 import BeautifulSoup


def put_in_sql(a):

    insert = '''
    insert into sales(t_name, p_name, url, price)
    values (%s, %s, %s, %s)
    '''

    b = []

    for i in a:
        for c in i:
            for v in i[c]:
                for nt in v:
                    b.append(
                        (
                            c, nt, v[nt][0], v[nt][1]
                        )
                    )

    from mysql.connector import connect, Error
    try:
        with connect(
                host="localhost",
                user="root",
                password="",
                database="b_py"
        ) as connection:
            with connection.cursor() as cursor:
                cursor.executemany(insert, b)
                connection.commit()
    except Error as e:
        print(e)



def all_of_catalog():
    start = 'https://www.bershka.com/by/%D0%BC%D1%83%D0%B6%D1%87%D0%B8%D0%BD%D1%8B'
    URLS = [
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%BA%D1%83%D1%80%D1%82%D0%BA%D0%B8-%D0%B8-%D0%BF%D0%B0%D0%BB%D1%8C%D1%82%D0%BE-c1010193546.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D1%82%D0%BE%D0%BB%D1%81%D1%82%D0%BE%D0%B2%D0%BA%D0%B8-c1010193244.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D1%81%D0%B2%D0%B8%D1%82%D0%B5%D1%80%D1%8B-%D0%B8-%D0%BA%D0%B0%D1%80%D0%B4%D0%B8%D0%B3%D0%B0%D0%BD%D1%8B-c1010193243.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%B6%D0%B8%D0%BB%D0%B5%D1%82%D1%8B-c1010514002.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D1%84%D1%83%D1%82%D0%B1%D0%BE%D0%BB%D0%BA%D0%B8-c1010193239.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D1%80%D1%83%D0%B1%D0%B0%D1%88%D0%BA%D0%B8-c1010193240.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%B1%D1%80%D1%8E%D0%BA%D0%B8-c1010193241.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D0%B4%D0%B6%D0%B8%D0%BD%D1%81%D1%8B-c1010193238.html?discount=1',
        '/%D0%BE%D0%B4%D0%B5%D0%B6%D0%B4%D0%B0/%D1%88%D0%BE%D1%80%D1%82%D1%8B-c1010193242.html?discount=1',
        '/%D0%BE%D0%B1%D1%83%D0%B2%D1%8C-c1010193202.html?discount=1',
        '/%D0%B0%D0%BA%D1%81%D0%B5%D1%81%D1%81%D1%83%D0%B0%D1%80%D1%8B-c1010193172.html?discount=1'
        ]
    TYPES = ['Куртки и пальто', 'Толстовки', 'Свитеры и кардиганы', 'Жилеты', 'Футболки',
             'Рубашки', 'Брюки', 'Джинсы', 'Шорты', 'Обувь', 'Аксессуары']

    result = []
    ONCE = list(zip(TYPES, URLS))

    for t, u in ONCE:
        result.append({
            t: get_source_html(url=start + u)
        })

    put_in_sql(result)


def get_sales(structure):
    # with open("123.html", "w", encoding='utf-8') as file:
    #     file.write(driver.page_source)
    soup = BeautifulSoup(structure, 'lxml')
    items = soup.find_all('div', class_='category-product-card')

    sales = []
    for item in items:
        if item.find('img', class_='image-item'):
            sales.append({
                # 'name': item.find('div', class_='product-text product-text__without-label').get_text(),
                # 'price': ''.join(item.find('span', class_='current-price-elem red-price').get_text().split())
                # 'div', class_='product-text product-text__without-label'
                item.find('img', class_='image-item').get('alt'): [
                    'https://www.bershka.com' + item.find('a', class_='grid-card-link').get('href'),
                    ''.join(item.find('span', class_='current-price-elem red-price').get_text().split()[0])
                ]
            })
    return sales


def get_source_html(url):
    driver = webdriver.Chrome()

    driver.get(url=url)
    time.sleep(0.3)
    SCROLL_PAUSE_TIME = 0.3

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(0.3)
    return get_sales(driver.page_source)


def main():
    all_of_catalog()


if __name__ == '__main__':
    main()
