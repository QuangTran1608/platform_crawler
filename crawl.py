from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep

wd = webdriver.Chrome()
wd.get('https://shopee.vn/search?keyword=laptop')
sleep(5)
soup = BeautifulSoup(wd.page_source, "html.parser")
tables = soup.find_all('div', attrs={'class': 'tWpFe2'})

with open('result.html', 'w', encoding='utf-8') as f:
    for table in tables:
        f.write(table.prettify())
        f.write('#'*80)

data_collections = []
for table in tables:
    product_dict = {'upper_price': 'NA',
                    'lower_price': 'NA',
                    'description': 'NA'}
    price_range = table.find_all('span', attrs={'class': 'ZEgDH9'})
    description = table.find('div', attrs={'class': 'ie3A+n bM+7UW Cve6sh'})
    if len(price_range) == 2:
        product_dict['lower_price'] = price_range[0].text
        product_dict['upper_price'] = price_range[1].text
    elif len(price_range) == 1:
        product_dict['lower_price'] = price_range[0].text
    product_dict['description'] = description.text
    data_collections.append(product_dict)

df = pd.DataFrame.from_records(data_collections)
df.to_json('data.json', indent=2, force_ascii=False, orient='records')
