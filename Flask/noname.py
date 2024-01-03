import json

from googletrans import Translator

#  pip install googletrans==3.1.0a0

def get_perfect_dict_data():
    translator = Translator()
    with open('../parsing_mvideo/data/data.json') as file:
        data = json.load(file)
    lst_products = []
    for page in data.values():
        page = page.get('body').get('products')
        for product in page:
            rating = product.get('rating').get('star')
            if rating:
                rating = float(str(round(float(rating), 1)))
            else:
                rating = '-'
            modelName = product.get('modelName')
            salePrice = product.get('salePrice')
            name = product.get('name')
            brandName = product.get('brandName')
            extra = product.get("propertiesPortion")
            extra = list(map(lambda x: [x.get("name"), x.get("value")], extra))
            dict_extra = {}
            for i in extra:
                dict_extra[i[0]] = i[1]
            try:
                shortage = dict_extra.get('Встроенная память (ROM)')
                if shortage == "1":
                    shortage = "1024"
            except Exception as e:
                shortage = None
            CPU = dict_extra.get('Тип процессора')
            Display = dict_extra.get('Технология экрана')
            diagonal = dict_extra.get('Экран').split('"')[0]
            guarantee = dict_extra.get('Гарантия')
            try:
                guarantee = translator.translate(guarantee, dest='en', src='ru').text
            except Exception as e:
                pass
            nameTranslit = product.get("nameTranslit")
            d = {"modelName": modelName, "nameTranslit": nameTranslit, "salePrice": salePrice, "name": name,
                 "rating": rating,
                 "extra": {"brandName": brandName,
                           "shortage": shortage,
                           "CPU": CPU,
                           "Display": Display,
                           "diagonal": diagonal,
                           "guarantee": guarantee}}
            lst_products.append(d)
    with open('utils/perfectdata.json', "w") as file:
        json.dump(lst_products, file, ensure_ascii=True)
    return lst_products



if __name__ == '__main__':
    print(get_perfect_dict_data())
