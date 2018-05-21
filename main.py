import json
from flask import Flask, request
from wordutil import find_word_from_tree_dict, init_dirtyword_tree_dict


app = Flask(__name__)
init_dirtyword_tree_dict()


@app.route('/checkwords', methods=['GET', 'POST'])
def checkword():
	# content = request.form.get('content')
	content = request.args.get('content')
	words_list = find_word_from_tree_dict(content, return_all_dirty_words=True)
	return json.dumps(words_list)


@app.route('/hello')
def index():
	return 'hello'


if __name__ == '__main__':
	app.run()
