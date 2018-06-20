import hashlib
import json
from functools import lru_cache
import datetime
from models import Member, WordLib, db
from wordmanager import WordManager


def md5(astring):
    return hashlib.md5(astring.encode('utf-8')).hexdigest()

def gen_useropenid(email):
    basekeystring = 'dirtywordschecker'
    concatstring = basekeystring+email
    return md5(concatstring)


class MemberService:
    def get_password_md5(self, password):
        return md5(password)

    def create(self, email, password):
        password = self.get_password_md5(password)
        openid = gen_useropenid(email)
        # print(password, openid)
        member = Member(email=email, password=password, openid=openid, created_date=datetime.datetime.utcnow())
        db.session.add(member)
        db.session.commit()

    def get_member_by_email(self, email):
        return Member.query.filter_by(email=email).first()

    def get_member_by_id(self, member_id):
        return Member.query.filter_by(id=member_id).first()

    def get_member_by_openid(self, openid):
        return Member.query.filter_by(openid=openid).first()


class WordLibService:

    def create(self, user_id, wordlibname, wordjsonlist):
        wl = WordLib(userid=user_id, wordlibname=wordlibname, wordjsonlist=wordjsonlist, created_date=datetime.datetime.utcnow())
        db.session.add(wl)
        db.session.commit()

    def delete(self, user_id, wordlibname):
        wl = WordLib(userid=user_id, wordlibname=wordlibname)
        db.session.add(wl)
        db.session.commit()

    def get_wordlib(self, user_id, wordlibname):
        wl = WordLib.query.filter_by(userid=user_id, wordlibname=wordlibname).first()
        return wl

    def update(self, user_id, wordlibname, wordjsonlist):
        wl = self.get_wordlib(user_id, wordlibname)
        if wl:
            wl.wordjsonlist = wordjsonlist
            db.session.commit()
        else:
            self.create(user_id, wordlibname, wordjsonlist)


@lru_cache(maxsize=100)
def get_wordlib3_wordset(user_id):
    ws = WordLibService()
    wl = ws.get_wordlib(user_id, 'wordlib3')
    wordset_list = []
    for w_line in json.loads(wl.wordjsonlist):
        w_line_set = set()
        for w in w_line.split('；'):
            if w:
                w_line_set.add(w)
        wordset_list.append(w_line_set)
    return wordset_list


def get_dirty_words_in_wordlib3(dirtywords, user_id):
    # print('got dirtywords lib3:', dirtywords)
    wordset_list = get_wordlib3_wordset(user_id)
    dirtywords_set = set(dirtywords)
    for wordset in wordset_list:
        shootwords = dirtywords_set & wordset
        # print('check:', dirtywords_set, wordset, shootwords)
        if shootwords == wordset:
            return shootwords
    return []


@lru_cache(maxsize=100)
def get_tree_dict_for_wordlib(user_id, wordlibname):
    ws = WordLibService()
    wl = ws.get_wordlib(user_id, wordlibname)
    if not wl:
        return {}
    words = wl.get_words_list()
    wm = WordManager(words)
    tree_dict = wm.init_tree_dict()
    return tree_dict, words


def get_dirtywords_in_wordlib(content, user_id, wordlibname):
    tree_dict, words = get_tree_dict_for_wordlib(user_id, wordlibname)
    if not tree_dict:
        return []
    # print('got tree',tree_dict)
    wm = WordManager()
    wm.set_tree_dict(tree_dict)
    dirtywords_list = wm.find_word_from_tree_dict(content, return_all_dirty_words=True)
    if wordlibname == 'wordlib1':
        return dirtywords_list
    if wordlibname == 'wordlib2':
        if len(dirtywords_list) >= 2:
            return dirtywords_list
        else:
            return []
    if wordlibname == 'wordlib3':
        return get_dirty_words_in_wordlib3(dirtywords_list, user_id)


def get_dirtywords_in_wordlibs(content, user_id, wordlibnames):
    dirtywords_list = []
    for wordlibname in wordlibnames:
        dirtywords_list += get_dirtywords_in_wordlib(content, user_id, wordlibname)
    return dirtywords_list


if __name__ == '__main__':
    db.create_all()
    # ms = MemberService()
    # email = 'yt.luo@idiaoyan.com'
    # password = '123456'
    # # ms.create(email, password)
    # member = ms.get_member_by_email(email)
    # print(member)