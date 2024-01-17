import json


def get_characteristic(username, productID):
    with open('/Users/sergeybudygin/PycharmProjects/Market/Flask/utils/perfectdata.json') as file:
        data = json.load(file)
    lst = []
    product = data.get(productID, {}).get("extra", {})
    for i in product:
        lst.append({"name": i, "description": product[i]})
    return lst, data.get(productID, {}).get("salePrice", {}), data.get(productID, {}).get("modelName", {})

if __name__ == "__main__":
    print(get_characteristic)