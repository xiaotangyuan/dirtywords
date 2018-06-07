"""
构造词组的tree和检测一个字符串内容是否包含tree中的词
"""

import json
import sqlite3


tree_dict = {}


wordlibnames = ['wordlib1','wordlib2','wordlib3']


def make_recursion_dict(word):
    the_dict = {
        'word_end': True,
    }
    for w in word[::-1]:
        the_dict = {
            w: the_dict.copy(),
        }
    return the_dict


def add_word_to_tree(word):
    word = word.strip()
    word = word.replace('\n', '')
    now_dict = tree_dict
    for index, w in enumerate(word):
        if w not in now_dict:
            d = make_recursion_dict(word[index+1:])
            now_dict[w] = d
            return
        now_dict = now_dict[w]
    now_dict['word_end'] = True


def find_word_from_tree_dict(content, return_all_dirty_words=False):
    now_dict = tree_dict
    words_list = []
    words = []
    content_str_num = len(content)
    for index, w in enumerate(content):
        # print('check word:', w, now_dict.get(w), bool(now_dict.get(w)))
        while now_dict.get(w):
            # print('in while：', index)
            words.append(w)
            now_dict = now_dict.get(w)
            index += 1
            if index > content_str_num - 1:
                w = None
            else:
                w = content[index]
            # print('next w:', w)
            # print('now_dict:', now_dict, now_dict.get(w, {}))
            # 单个字符一般不会是敏感词，所以len(words) > 1
            if now_dict and len(words) > 1 and 'word_end' in now_dict:
                words_list.append(words.copy())
                if return_all_dirty_words is False:
                    return words_list

        now_dict = tree_dict
        words = []
    words_list = [''.join(item) for item in words_list]
    return words_list


def test_find_word():
    import pprint
    word1 = '这是一个词语a'
    word2 = '这是一个词语b'
    word3 = '这是一个词语'
    word4 = '这是'
    word5 = '这是第二个词语'
    word6 = '这是一'
    for word in [word1, word2, word3, word4, word5, word6]:
        add_word_to_tree(word)
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(tree_dict)

    print('-----')
    content = 'ahahah啊哈这是'
    word = find_word_from_tree_dict(content)
    print(word)


def load_words_data_to_tree_dict(filename):
    with open(filename, newline='\n') as f:
        for word in f.readlines():
            add_word_to_tree(word)


def init_dirtyword_tree_dict():
    filename = 'dirtywords.txt'
    load_words_data_to_tree_dict(filename)


class LimitWordManager(object):
    def __init__(self):
        self.conn = self.get_db_conn()
        self.cursor = self.conn.cursor()

    def get_db_conn(self):
        dbfilename = 'limitwords.db'
        return sqlite3.connect(dbfilename)

    def create_wordlib_table(self):
        c = self.conn.cursor()
        c.execute("CREATE TABLE wordlib (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            WORDJSONLIST TEXT NOT NULL, \
            WORDLIBNAME TEXT NOT NULL UNIQUE)")
        self.conn.commit()

    def insert_wordlib(self, wordjsonlist, wordlibname):
        c = self.cursor
        sql = "INSERT INTO wordlib (WORDJSONLIST, WORDLIBNAME) \
            VALUES ('%s', '%s')" % (wordjsonlist, wordlibname)
        c.execute(sql);
        self.conn.commit()

    def update_wordlib(self, wordjsonlist, wordlibname):
        c = self.cursor
        sql = "UPDATE wordlib SET WORDJSONLIST='%s' WHERE WORDLIBNAME='%s'" % (wordjsonlist, wordlibname) 
        c.execute(sql);
        self.conn.commit()

    def get_wordlib(self, wordlibname):
        c = self.cursor
        sql = "select * from wordlib where WORDLIBNAME='%s'" % wordlibname
        data = c.execute(sql).fetchone()
        return data

    def get_all_words(self):
        words = []
        for wordlib in wordlibnames:
            data = self.get_wordlib(wordlib)[1]
            for w in json.loads(data):
                words.append(w)
        return words


def add_wordlib_to_tree_dict_from_sqlite(wordlibname):
    lwm = LimitWordManager()
    words = lwm.get_wordlib(wordlibname)[1]
    words = json.loads(words)
    for w in words:
        add_word_to_tree(w)


def init_dirtyword_tree_dict_from_sqlite():
    wordlibnames = ['wordlib1','wordlib2','wordlib3']
    for wordlibname in wordlibnames:
        add_wordlib_to_tree_dict_from_sqlite(wordlibname)


def init_db():
    lwm = LimitWordManager()
    lwm.create_wordlib_table()
    for wordlibname in wordlibnames:
        wordjsonlist = ["刷单"]
        wordjsonlist = json.dumps(wordjsonlist, ensure_ascii=False)
        lwm.insert_wordlib(wordjsonlist, wordlibname)


def test_LimitWordManager():
    lwm = LimitWordManager()
    # lwm.create_wordlib_table()
    wordjsonlist = json.dumps(['测试3','测试4'], ensure_ascii=False)
    wordlibname = 'wordlib1'
    # lwm.insert_wordlib(wordjsonlist, wordlibname)
    # print(lwm.get_wordlib(wordlibname))
    print(lwm.get_all_words())



if __name__ == '__main__':
    # filename = 'dirtywords.txt'
    # load_words_data_to_tree_dict(filename)

    # test_find_word()
    # with open('content2.txt', encoding='utf-8') as f:
    #     content = f.read()
    # print(len(content))
    # word = find_word_from_tree_dict(content)
    # print('got word:', word)
    test_LimitWordManager()
    # init_db()

