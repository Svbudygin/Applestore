import requests
import json
import os
from config import headers, cookies, id_parsing, prices_parsing, descripion_parsing
from math import ceil

description = {}
ids = {}
prices = {}
sess = requests.Session()


def parsing_function_ids(offset='0'):
    params = id_parsing(offset)
    response = sess.get('https://www.mvideo.ru/bff/products/listing', params=params, cookies=cookies,
                        headers=headers).json()
    return response


def parsing_function_description(product_ids):
    json_data = descripion_parsing(product_ids)

    response = sess.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                         json=json_data).json()
    return response


def parsing_function_prices(product_ids):
    product_ids_str = ','.join(product_ids)
    params, headers1 = prices_parsing(product_ids_str)
    try:
        response_price = sess.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                                  headers=headers1).json()
        return response_price
    except requests.exceptions.JSONDecodeError:
        return None


def get_data():
    if not os.path.exists('data'):
        os.mkdir('data')

    total_number_of_items = parsing_function_ids().get('body').get('total')
    if total_number_of_items is None:
        return 'Товары не найдены!'
    pages = ceil(total_number_of_items / 24)

    for page in range(pages):
        product_ids = parsing_function_ids(offset=str(page * 24)).get('body').get('products')
        ids[page] = product_ids
        # ------ next block: prices
        response_price = parsing_function_prices(product_ids)
        if response_price is None:
            continue
        # ------ next block: description
        description[page] = parsing_function_description(product_ids)
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
