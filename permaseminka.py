import requests
from bs4 import BeautifulSoup
# import numpy as np
import pandas as pd
from datetime import date

# get count of all products (the number of goods will vary in time)

pre_URL = 'https://permaseminka.cz/2-home'
pre_page = requests.get(pre_URL)
pre_soup = BeautifulSoup(pre_page.content, 'html.parser')
pre_count = pre_soup.find('div', class_='product-count pull-right')
pre_count = pre_count.text[pre_count.text.find(" z ") + 3:]
product_count = int(pre_count[: pre_count.find("polo")])
print(product_count)

# now get the right URL with all products on the page
URL = f'https://permaseminka.cz/2-home?id_category=2&n={product_count}'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

# get list of all products
product_grid = soup.find('div', class_='product_list grid row')
all_products = product_grid.find_all('div', class_= 'product-image-container image')

product_table = []
for item in all_products:
    x = item.find('a', class_= 'product_img_link')
    try:
        item.find('span', class_="label labelnew").text
        new = 'Yes'
    except:
        new = None
    try:
        item.find('span', class_='labelsold label').text
        sold = 'Yes'
    except:
        sold = None
    product_table.append({"Title": x.get("title"), "New": new, "Sold": sold, "Link": x.get("href")})

# adding the Product Group from link
for n, i in enumerate(product_table):
    group_1 = i["Link"][i["Link"].find('.cz/')+4:]  # yes, too lazy to regexp :-P
    group_2 = group_1.find('/')
    product_table[n]["Group"] = group_1[:group_2]

# finalizing the results
df_final = pd.DataFrame(product_table)
df_final.set_index(keys=['Group', 'Title'], inplace=True)

# df_sold = df_final[df_final['Sold'] == 'Yes']
# df_new = df_final[df_final['New'] == 'Yes']
# df_available = df_final[pd.isnull(df_final['Sold'])]

# write the result to csv
today = date.today()
df_final.to_csv(f"permaseminka_{today}.csv")



