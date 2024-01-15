x = [1, 987, 3]
y = [1, 2, 1234]


class Recommendations():
    def __init__(self, first_list: list, second_list: list):

        dict_vectors = {"Vector1": [[], []], "Vector2": [[], []]}
        for i in first_list:
            try:
                dict_vectors.get("Vector1")[0].append(float(i))
            except Exception:
                dict_vectors.get("Vector1")[1].append(i)
        for i in second_list:
            try:
                dict_vectors.get("Vector2")[0].append(float(i))
            except Exception:
                dict_vectors.get("Vector2")[1].append(i)
        self.__first_list_str = dict_vectors.get("Vector1")[1]
        self.__first_list_int = dict_vectors.get("Vector1")[0]
        self.__second_list_str = dict_vectors.get("Vector2")[1]
        self.__second_list_int = dict_vectors.get("Vector2")[0]

    def main_action(self):
        integer_part = self.cos_simlrt(self.Vi1, self.Vi2) * 10
        x = 0
        for i in range(len(self.Vs1)):
            x += self.jaccard_similarity_of_two_words(self.Vs1[i], self.Vs2[i])
        x /= len(self.Vs1)
        final_simularity = (x + integer_part) / 11
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
        print("cos_simlrt", v1, v2, cos_simlrt)
        return cos_simlrt

if __name__ == "__main__":
    rec = Recommendations(y, x)
    print(rec.main_action())
