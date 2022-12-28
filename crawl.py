from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

wd = webdriver.Chrome()
wd.get('https://shopee.vn/search?keyword=laptop')
sleep(5)

product_list = list()
SCROLL_PAUSE_TIME = 0.5
# Get scroll height
last_height = wd.execute_script("return window.scrollY")
while True:
    soup = BeautifulSoup(wd.page_source, "html.parser")
    product_list.extend([product for product in soup.find_all('div', 
                                                    attrs={'class': 'col-xs-2-4 shopee-search-item-result__item'})])
    # Scroll down to bottom
    wd.execute_script("window.scrollTo(0, window.scrollY + 300)")

    # Wait to load page
    sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = wd.execute_script("return window.scrollY")
    if new_height == last_height:
        break
    last_height = new_height

product_list = set(product_list)

with open('result.html', 'w', encoding='utf-8') as f:
    for product in product_list:
        f.write(product.prettify())
        f.write('#'*80)

data_collections = dict()
for i, product in enumerate(product_list):
    product_dict = {'upper_price': 'NA',
                    'lower_price': 'NA',
                    'description': 'NA',
                    'link': 'NA'}
    try:
        product_link = product.find('a', attrs={'data-sqe': 'link'}).get('href')
        product_id = product_link.split('sp_atk=')[-1]
        if product_id in data_collections.keys():
            continue
    except Exception as e:
        print(i)
        continue

    product_dict['link'] = product_link[1:]
    price_range = product.find_all('span', attrs={'class': 'ZEgDH9'})
    if len(price_range) == 2:
        product_dict['lower_price'] = price_range[0].text
        product_dict['upper_price'] = price_range[1].text
    elif len(price_range) == 1:
        product_dict['lower_price'] = price_range[0].text

    description = product.find('div', attrs={'class': 'ie3A+n bM+7UW Cve6sh'})
    product_dict['description'] = description.text

    data_collections[product_id] = product_dict

df = pd.DataFrame.from_dict(data_collections, orient='index')
df.to_json('data.json', indent=2, force_ascii=False, orient='records')
