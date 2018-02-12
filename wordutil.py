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

