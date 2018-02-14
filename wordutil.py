"""
构造词组的tree和检测一个字符串内容是否包含tree中的词
"""

tree_dict = {}


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
			if now_dict and len(words) > 1 and 'word_end' in now_dict:
				words_list.append(words.copy())
				if return_all_dirty_words is False:
					return words_list

		now_dict = tree_dict
		words = []
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
			word = word.strip()
			word = word.replace('\n', '')
			add_word_to_tree(word)

if __name__ == '__main__':
	filename = 'dirtywords.txt'
	load_words_data_to_tree_dict(filename)

	# test_find_word()
	with open('content2.txt', encoding='utf-8') as f:
		content = f.read()
	print(len(content))
	word = find_word_from_tree_dict(content)
	print('got word:', word)

