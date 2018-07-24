# encoding=utf8


"""
词库3笛卡尔积
"""


import csv
import pandas as pd


def gen_cartsian_for_two_list(lista, listb):
    res = ['%s；%s' % (a, b) for a in lista for b in listb]
    return res


def gen_words_csv(filename):
    f = open(filename, 'r')
    csv_reader = csv.reader(f)
    data_list = list(csv_reader)
    df = pd.DataFrame(data_list)
    words_list = []
    for i in range(0, len(data_list[0])-1):
        if i%2 != 0 :
            continue
        x = i
        y = i + 1
        x_values = df[x].values
        y_values = df[y].values
        x_values = [x for x in x_values if x]
        y_values = [y for y in y_values if y]
        cartsian = gen_cartsian_for_two_list(x_values, y_values)
        words_list += cartsian
    with open('cartisian_words.csv', 'w') as f:
        for w in words_list:
            f.write(w+'\n')


if __name__ == '__main__':
    filename = 'test.csv'
    filename = 'wordlib_verb_and_n.csv'
    gen_words_csv(filename)
