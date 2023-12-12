import requests
import json
import os
from config import headers, cookies, id_parsing, prices_parsing, descripion_parsing
from math import ceil


def get_data():
    if not os.path.exists('data'):
        os.mkdir('data')

    params = id_parsing()
    # echo -n 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==' | base64 -d
    sess = requests.Session()
    response = sess.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                        headers=headers).json()
    total_number_of_items = response.get('body').get('total')
    if total_number_of_items is None:
        return 'Товары не найдены!'
    pages = ceil(total_number_of_items / 24)

    description = {}
    ids = {}
    prices = {}
    for page in range(pages):
        offset = str(page * 24)
        params = id_parsing(offset=offset)
        response = sess.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                            headers=headers).json()
        product_ids = response.get('body').get('products')
        ids[page] = product_ids
        # ------ next block: prices
        product_ids_str = ','.join(product_ids)
        params, headers1 = prices_parsing(product_ids_str)
        try:
            response_price = sess.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                      headers=headers1).json()
        except requests.exceptions.JSONDecodeError:
            continue
        # ------ next block: description
        json_data = descripion_parsing(product_ids)

        response = sess.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                             json=json_data).json()
        description[page] = response
        # ------ back to block: prices
        material_prices = response_price.get('body').get('materialPrices')

        for product in material_prices:
            product_id = product.get('price').get('productId')
            product_base_price = product.get('price').get('basePrice')
            product_sale_price = product.get('price').get('salePrice')
            product_bonus = product.get('bonusRubles').get('total')
            prices[product_id] = {
                "basePrice": product_base_price,
                "salePrice": product_sale_price,
                "bonus": product_bonus
            }
        print(f'[+] Page {page} from {pages}')
    for items in description.values():
        items = items.get('body').get('products')
        if items:
            for product in items:
                product_id = product.get('productId')
                if product_id in prices:
                    price = prices[product_id]
                    product["basePrice"] = price.get('basePrice')
                    product["salePrice"] = price.get('salePrice')
                    product["bonus"] = price.get('bonus')
                    product["link"] = f"https://www.mvideo.ru/products/{product.get('nameTranslit')}-{product_id}"

    with open(f'data/result.json', 'w') as file:
        json.dump(description, file, indent=4, ensure_ascii=True)


def main():
    get_data()
    pass


if __name__ == '__main__':
    main()
