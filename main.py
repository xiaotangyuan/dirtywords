import json, os
import logging
import flask
from flask import Flask, request, redirect, url_for
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import flask_login
import wordutil
import wordcupleweight


import logging
logfile = 'checkword.log'
logging.basicConfig(filename=logfile,
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
log = logging


app = Flask(__name__)
app.secret_key = 'dirtywordscheckerkey'

import services


login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    ms = services.MemberService()
    member = ms.get_member_by_id(user_id)
    # print(user_id, member)
    return member


# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users:
#         return

#     user = User()
#     user.id = email

#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['password'] == users[email]['password']

#     return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    email = flask.request.form['email']
    password = flask.request.form['password']
    email = email.strip()
    if email:
        member = services.Member.query.filter_by(email=email).first()
    if member:
        ms = services.MemberService()
        pw_md5 = ms.get_password_md5(password)
        if pw_md5 == member.password:
            flask_login.login_user(member)
            return flask.redirect(flask.url_for('managewords'))

    return 'Bad login'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/checkwords', methods=['POST'])
def checkword():
    content = request.form.get('content')
    origin_id = request.form.get('origin_id')
    wordlibs = request.form.get('wordlibs')
    openid = request.form.get('openid')

    log.info('[content] %s, %s' % (openid, content))

    ms = services.MemberService()
    member = ms.get_member_by_openid(openid)
    if not member:
        return 'bad openid: %s' % openid
    if not wordlibs:
        wordlibs = ['wordlib1', 'wordlib2', 'wordlib3']
    else:
        wordlibs = wordlibs.split(',')

    words = services.get_dirtywords_in_wordlibs(content, member.id, wordlibs)
    res = {
        'wordlibs': wordlibs,
        'shootwords': words
    }
    res = json.dumps(res, ensure_ascii=False)
    return res


@app.route('/testcheckwords', methods=['GET', 'POST'])
@flask_login.login_required
def testcheckwords():
    if request.method == 'POST':
        content = request.form.get('content')
        origin_id = request.form.get('origin_id')
        wordlibs = request.form.get('wordlibs')
        openid = flask_login.current_user.openid

        log.info('[content] %s' % content)

        ms = services.MemberService()
        member = ms.get_member_by_openid(openid)
        if not member:
            return 'bad openid: %s' % openid 
        if not wordlibs:
            wordlibs = ['wordlib1', 'wordlib2', 'wordlib3']

        words = services.get_dirtywords_in_wordlibs(content, member.id, wordlibs)
        res = {
            'wordlibs': wordlibs,
            'shootwords': words
        }
        res = json.dumps(res, ensure_ascii=False)
        return res
    else:
        return render_template("inputtext.html")


@app.route('/checkcupleweightword', methods=['GET', 'POST'])
@flask_login.login_required
def checkcupleweightword():
    content = request.form.get('content')
    max_weight, words_list = wordcupleweight.find_word_and_weight_from_tree_dict(content)
    res = {
        'max_weight': max_weight,
        'words_list': words_list
    }
    return json.dumps(res)


@app.route('/managewords', methods=['GET'])
@flask_login.login_required
def managewords():
    current_user = flask_login.current_user
    wordlib = request.args.get('wordlib')
    if not wordlib:
        wordlib = 'wordlib1'
    # lwm = wordutil.LimitWordManager()
    # data = lwm.get_wordlib(wordlib)[1]
    sw = services.WordLibService()
    wordlibobj = sw.get_wordlib(current_user.id, wordlib)
    if wordlibobj:
        data = json.loads(wordlibobj.wordjsonlist)
    else:
        data = []
    data = [d+'\n' for d in data]
    rows = len(data) + 5
    return render_template("managewords.html", data=data, rows=rows, wordlibname=wordlib, current_user=current_user)


@app.route('/submitwords', methods=['POST'])
@flask_login.login_required
def submitwords():
    user_id = flask_login.current_user.id
    wordlib = request.form.get('wordlib')
    words = request.form.get('words')
    words = words.strip()
    words = [w.strip() for w in words.split('\n') if w]
    wordjsonlist = json.dumps(words, ensure_ascii=False)
    sw = services.WordLibService()
    sw.update(user_id, wordlib, wordjsonlist)
    # lwm = wordutil.LimitWordManager()
    # lwm.update_wordlib(wordjsonlist, wordlib)
    wordutil.init_dirtyword_tree_dict_from_sqlite()
    # wordutil.add_wordlib_to_tree_dict_from_sqlite(wordlib)
    # res = {'status':'success'}
    # return json.dumps(res)
    return redirect(url_for('managewords')+'?wordlib=%s' % wordlib)


@app.route('/tree', methods=['get'])
@flask_login.login_required
def tree():
    tree_json = json.dumps(wordutil.tree_dict, ensure_ascii=False)
    return tree_json


@app.route('/hello')
def index():
    return 'hello'


if __name__ == '__main__':
    import sys
    port = sys.argv[1]
    debug = sys.argv[2]
    if debug == 'False':
        debug = False
    else:
        debug = True
    app.run('0.0.0.0', port=port, debug=debug)
