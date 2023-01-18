from seleniumwire import webdriver
from seleniumwire.utils import decode
import json
import time
import pandas as pd

driver = webdriver.Chrome()

driver.get('https://shopee.co.id/search?keyword=laptop')
time.sleep(5)

for request in driver.requests:
    if request.response:
        if request.url.startswith('https://shopee.co.id/api/v4/search/search_items?by=relevancy&keyword='):
            response = request.response
            body = decode(response.body, response.headers.get('Content-Encoding', 'Identity'))
            decode_body = body.decode('utf8')
            json_data = json.loads(decode_body)

            product_name = json_data['items']
            count = 0

            data = []
            for i in range(0, len(product_name)):
                name = json_data['items'][i]['item_basic']['name']
                price = json_data['items'][i]['item_basic']['price']
                sold = json_data['items'][i]['item_basic']['sold']
                stock = json_data['items'][i]['item_basic']['stock']
                count += 1
                data.append(
                    (name, price, sold, stock)
                )
            df = pd.DataFrame(data, columns=['Nama Barang', 'Harga', 'Terjual', 'Stock'])
            print(df)