import json
from typing import List

from googletrans import Translator


#  pip install googletrans==3.1.0a0

class Filter:
    @staticmethod
    def check_extra(dict_input, name, lst):
        return dict_input.get("extra", {}).get(name) in lst

    def get_rating_modelName_salePrice(self, brandName, shortage, CPU, Display, diagonal,
                                       guarantee):
        print("get_rating_modelName_salePrice",brandName, shortage, CPU, Display, diagonal,
                                       guarantee )
        with open('/Users/sergeybudygin/PycharmProjects/Market/Flask/utils/perfectdata.json') as file:
            data = json.load(file)
        lst_products = []
        for product in data:
            if len(brandName) > 0 and not self.check_extra(product, "brandName", brandName):
                continue
            elif len(shortage) > 0 and not self.check_extra(product, "shortage", shortage):
                continue
            elif len(CPU) > 0 and not self.check_extra(product, "CPU", CPU):
                continue
            elif len(Display) > 0 and not self.check_extra(product, "Display", Display):
                continue
            elif len(diagonal) > 0 and not self.check_extra(product, "diagonal", diagonal):
                continue
            elif len(guarantee) > 0 and not self.check_extra(product, "guarantee", guarantee):
                continue
            else:
                rating = product.get('rating')
                modelName = product.get('modelName')[:30]
                salePrice = product.get('salePrice')
                lst_products.append([rating, modelName, salePrice])
        return lst_products

    @staticmethod
    def get_all_for_filtest(name: str):
        with open('/Users/sergeybudygin/PycharmProjects/Market/Flask/utils/perfectdata.json') as file:
            data = json.load(file)
        lst = set()
        for product in data:
            lst.add(product.get("extra").get(name))
        return lst

    @staticmethod
    def sorted_by_price(lst: list, decrease: bool = True):
        lst = sorted(lst, key=lambda x: x[-1], reverse=decrease)
        return lst

    @staticmethod
    def sorted_by_name(lst: list, decrease: bool = True):
        lst = sorted(lst, key=lambda x: x[1], reverse=decrease)
        return lst

    @staticmethod
    def sets_work(set1, set2):
        return set1.intersection(set2)

    def sort_list_clever(self, name, lst):
        if name in {"price-increasing", "price-decreasing"}:
            dec = name == "price-decreasing"
            lst = self.sorted_by_price(lst, decrease=dec)
        if name in {"good-rating", "bad-rating"}:
            dec = name == "good-rating"
            lst = self.sorted_by_rating(lst, decrease=dec)
        if name in {"from-a-to-z", "from-z-to-a"}:
            dec = name == "from-z-to-a"
            lst = self.sorted_by_name(lst, decrease=dec)

        return lst

    @staticmethod
    def sorted_by_rating(lst: list, decrease: bool = True):
        print(lst)
        if decrease:
            lst = sorted(lst, key=lambda x: 0 if x[0] == '-' else x[0], reverse=decrease)
        else:
            lst = sorted(lst, key=lambda x: 5 if x[0] == '-' else x[0], reverse=decrease)
        return lst


if __name__ == '__main__':
    pass
