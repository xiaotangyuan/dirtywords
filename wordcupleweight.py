"""
用于疑似词这种有权重的敏感词检测
词组加权重模式
wordcuple_weight_list = [
    (2, ('word1', 'word2')),
    (6, ('word1', 'word2', 'word3')),
    (4, ('word1')),
]


1 先使用init_dirtyword_tree_dict()构建词库tree_dict
2 使用find_word_from_tree_dict检查出所有敏感词
3 遍历检查出来的敏感词，到wordcuple_weight_list核对是否有正确的组合，如果有返回敏感词词组及权重
"""

import csv
import wordutil


wordcuple_weight_list = []


def init_wordcupleweight_info():
    filename = 'wordcupleweight.csv'
    with open(filename) as f:
        readCSV = csv.reader(f, delimiter=',')
        for row in readCSV:
            weight, words = row[0], row[1:]
            weight = weight.strip()
            words = [w.strip() for w in words]
            if len(words) == 0:
                continue
            words = [w for w in words if len(w) > 0]
            wordcuple_weight_list.append((int(weight), words))
            for word in words:
                wordutil.add_word_to_tree(word)
    # print(wordutil.tree_dict)


def find_word_and_weight_from_tree_dict(content):
    words_return = []
    max_weight = 0

    words_list_res = wordutil.find_word_from_tree_dict(content, return_all_dirty_words=True)
    for weight, words in wordcuple_weight_list:
        has_all_limit_words = True
        for word in words:
            if word not in words_list_res:
                has_all_limit_words = False
                break
        if has_all_limit_words is True:
            words_return += words
            if weight > max_weight:
                max_weight = weight
    return max_weight, words_return


init_wordcupleweight_info()


def test():
    content = '我们敏感词测试这里可以有淘宝刷单欢迎联系qq或微信'
    max_weight, words_return = find_word_and_weight_from_tree_dict(content)
    print(max_weight, words_return)


if __name__ == '__main__':
    test()