import json
def get_rating_modelName_salePrice():
    with open('../parsing_mvideo/data/data.json') as file:
        data = json.load(file)
    lst_products = []
    for page in data.values():
        page = page.get('body').get('products')
        for product in page:
            rating = product.get('rating').get('star')
            if rating:
                rating = str(round(float(rating), 1))
            else:
                rating = '-'
            modelName = product.get('modelName')[:30]
            salePrice = product.get('salePrice')
            lst_products.append([rating, modelName, salePrice])
    return lst_products


if __name__ == '__main__':
    print(get_rating_modelName_salePrice())
