import json
from flask import Flask, request
from flask import render_template
import wordutil
import wordcupleweight


app = Flask(__name__)
wordutil.init_dirtyword_tree_dict()


@app.route('/checkwords', methods=['GET', 'POST'])
def checkword():
    content = request.form.get('content')
    # content = request.args.get('content')
    words_list = wordutil.find_word_from_tree_dict(content, return_all_dirty_words=True)
    return json.dumps(words_list)


@app.route('/checkcupleweightword', methods=['GET', 'POST'])
def checkcupleweightword():
    content = request.form.get('content')
    max_weight, words_list = wordcupleweight.find_word_and_weight_from_tree_dict(content)
    res = {
        'max_weight': max_weight,
        'words_list': words_list
    }
    return json.dumps(res)


@app.route('/managewords', methods=['GET'])
def managewords():
    wordlib = request.form.get('wordlib')
    if not wordlib:
        wordlib = 'wordlib1'
    lwm = wordutil.LimitWordManager()
    data = lwm.get_wordlib(wordlib)[1]
    data = json.loads(data)
    data = [d+'\n' for d in data]
    rows = len(data) + 5
    return render_template("managewords.html", data=data, rows=rows)


@app.route('/submitwords', methods=['POST'])
def submitwords():
    wordlib = request.form.get('wordlib')
    words = request.form.get('words')
    words = words.strip()
    words = [w.strip() for w in words.split('\n') if w]
    wordjsonlist = json.dumps(words, ensure_ascii=False)
    lwm = wordutil.LimitWordManager()
    lwm.update_wordlib(wordjsonlist, wordlib)
    res = {'status':'success'}
    return json.dumps(res)


@app.route('/hello')
def index():
    return 'hello'


if __name__ == '__main__':
    import sys
    port = sys.argv[1]
    app.run('0.0.0.0', port=port, debug=True)
