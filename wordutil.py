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


def find_word_from_tree_dict(content):
	now_dict = tree_dict
	words = []
	for w in content:
		res = now_dict.get(w)
		if res is None:
			continue
		now_dict = res
		words.append(w)
		if 'word_end' in now_dict:
			break
	return words


if __name__ == '__main__':
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
	content = 'ahahah啊哈这是一个内容哦'
	word = find_word_from_tree_dict(content)
	print(word)

