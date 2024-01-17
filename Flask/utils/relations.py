import json
import sqlite3
from functools import lru_cache

favorites = {}


class Recommendations:
    def __init__(self, first_list: list, second_list: list):

        dict_vectors = {"Vector1": [[], []], "Vector2": [[], []]}
        for i in range(len(first_list)):
            try:
                dict_vectors.get("Vector1")[0].append(float(first_list[i]))
                dict_vectors.get("Vector2")[0].append(float(second_list[i]))

            except Exception:
                if first_list[i] and second_list[i]:
                    dict_vectors.get("Vector1")[1].append(first_list[i])
                    dict_vectors.get("Vector2")[1].append(second_list[i])
                pass
        # print(dict_vectors.get("Vector1")[1], ";;;", dict_vectors.get("Vector1")[0])
        self.__first_list_str = dict_vectors.get("Vector1")[1]
        self.__first_list_int = dict_vectors.get("Vector1")[0]
        self.__second_list_str = dict_vectors.get("Vector2")[1]
        self.__second_list_int = dict_vectors.get("Vector2")[0]

    def main_action(self):
        integer_part = self.cos_simlrt(self.Vi1, self.Vi2) * 10
        x = 0
        for i in range(len(self.Vs1)):
            x += self.jaccard_similarity_of_two_words(self.Vs1[i], self.Vs2[i])
        try:
            x /= len(self.Vs1)
            final_simularity = (x + integer_part) / 11
        except ZeroDivisionError:
            final_simularity = integer_part / 10
        return final_simularity

    @property
    def Vs1(self):
        return self.__first_list_str

    @property
    def Vi1(self):
        return self.__first_list_int

    @property
    def Vs2(self):
        return self.__second_list_str

    @property
    def Vi2(self):
        return self.__second_list_int

    @staticmethod
    def jaccard_similarity_of_two_words(word1: str, word2: str, alpha=1, beta=5):
        set_letters1 = set(word1)
        set_letters2 = set(word2)
        set_bigrams1 = set(word1[i:i + 2] for i in range(len(word1) - 1))
        set_bigrams2 = set(word2[i:i + 2] for i in range(len(word2) - 1))

        intersection_letters = set_letters1 & set_letters2
        union_letters = set_letters1 | set_letters2

        intersection_bigrams = set_bigrams1 & set_bigrams2
        union_bigrams = set_bigrams1 | set_bigrams2
        if len(word1) == 0 and len(word2) == 0:
            return 0
        jaccard_letters = len(intersection_letters) / len(union_letters)
        if len(word1) > 1 and len(word2) > 1:

            jaccard_bigrams = len(intersection_bigrams) / len(union_bigrams)
            similarity = alpha * jaccard_letters + beta * jaccard_bigrams
            return similarity / (alpha + beta)
        else:
            similarity = alpha * jaccard_letters
            return similarity / alpha

    @staticmethod
    def Euclid_dist(v1, v2):
        res = 0
        for i in range(len(v1)):
            res += (v1[i] - v2[i]) ** 2
        return res ** .5

    @staticmethod
    def cos_simlrt(v1, v2):
        s1 = sum([v1[i] * v2[i] for i in range(len(v1))])
        s2 = sum([v1[i] ** 2 for i in range(len(v1))]) ** 0.5
        s3 = sum([v2[i] ** 2 for i in range(len(v1))]) ** 0.5
        cos_simlrt = s1 / (s2 * s3)
        # cos_dst = 1 - cos_simlrt
        return cos_simlrt


@lru_cache(None)
def relation_find(a, b):
    recommendation = Recommendations(a, b)
    return recommendation.main_action()


def reformation_to_recomendation(d: dict):
    salePrice = d.get("salePrice")
    brandName = d.get('extra', {}).get("brandName")
    shortage = d.get('extra', {}).get("shortage")
    CPU = d.get('extra', {}).get("CPU")
    Display = d.get('extra', {}).get("Display")
    diagonal = d.get('extra', {}).get("diagonal")
    lst = [salePrice, brandName, shortage, CPU, Display, diagonal]
    return lst

def get_recomrndations(username):
    conn = sqlite3.connect("data/users.sql")
    cursor = conn.cursor()
    cursor.execute('SELECT favorites FROM users WHERE username=?', (username,))
    user = cursor.fetchone()
    if not user:
        return []
    user = user[0]
    if user:
        favorite_items = user.split("/")
    else:
        favorite_items = []
    conn.close()
    with open('/Users/sergeybudygin/PycharmProjects/Market/Flask/utils/perfectdata.json') as file:
        data = json.load(file)
    for i in data:
        if i not in favorite_items:

            lst = reformation_to_recomendation(data.get(i))
            sum_of_rec = 0
            for j in favorite_items:
                fav_lst = reformation_to_recomendation(data.get(j))
                sum_of_rec += relation_find(tuple(fav_lst), tuple(lst))
            data[i]["rec"] = sum_of_rec
        else:
            data[i]["rec"] = None
    lst = []
    for i in data:
        if data[i].get("rec"):
            lst.append(
                {"rec": data[i].get("rec"),
                 "price": data[i].get("salePrice"),
                 "rate": data[i].get("rating"),
                 "name": data[i].get("modelName"),
                 "productId": data[i].get("productId")})
    lst.sort(key=lambda x: list(x.values())[0])
    return lst


def save_favorite_prod(a, username, limit=7):
    conn = sqlite3.connect("data/users.sql")
    cursor = conn.cursor()
    cursor.execute('SELECT favorites FROM users WHERE username=?', (username,))
    user = cursor.fetchone()[0]
    if user:
        user = user.split("/")
    else:
        user = []
    if a not in user:
        user.append(a)
    else:
        user.remove(a)
    user = "/".join(user[-limit:])
    cursor.execute('UPDATE users SET favorites=? WHERE username=?', (user, username))
    cursor.execute('SELECT favorites FROM users WHERE username=?', (username,))
    conn.commit()
    cursor.close()
    conn.close()
    # with open('/Users/sergeybudygin/PycharmProjects/Market/Flask/utils/perfectdata.json') as file:
    #     data = json.load(file)
    # global favorites
    # if a not in favorites:
    #     lst = reformation_to_recomendation(data.get(a))
    #     favorites[a] = lst
    # else:
    #     favorites.pop(a)
    # with open('/Users/sergeybudygin/PycharmProjects/Market/Flask/utils/favorites.json', 'w') as file:
    #     json.dump(favorites, file)


if __name__ == "__main__":
    x = [123, 431, 2332]
    y = [0, 431, 2332]
    rec = Recommendations(y, x)
    print(rec.main_action())
