"""
管理敏感词
"""


class WordManager:
	"""
	构建tree, 查找敏感词
	"""
	def __init__(self, words_list):
		self.words_list = words_list
		self.tree_dict = {}

	def init_tree_dict(self, words_list=None):
		if words_list is None:
			words_list = self.words_list
		for w in words_list:
			self.add_word_to_tree(w)

	def make_recursion_dict(self, word):
	    the_dict = {
	        'word_end': True,
	    }
	    for w in word[::-1]:
	        the_dict = {
	            w: the_dict.copy(),
	        }
	    return the_dict

	def add_word_to_tree(self, word):
	    word = word.strip()
	    word = word.replace('\n', '')
	    now_dict = self.tree_dict
	    for index, w in enumerate(word):
	        if w not in now_dict:
	            d = make_recursion_dict(word[index+1:])
	            now_dict[w] = d
	            return
	        now_dict = now_dict[w]
	    now_dict['word_end'] = True

	def set_tree_dict(self, tree_dict):
		self.tree_dict = tree_dict

	def find_word_from_tree_dict(self, content, return_all_dirty_words=False):
	    now_dict = self.tree_dict
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
	            # 单个字符一般不会是敏感词，所以len(words) > 1
	            if now_dict and len(words) > 1 and 'word_end' in now_dict:
	                words_list.append(words.copy())
	                if return_all_dirty_words is False:
	                    return words_list

	        now_dict = self.tree_dict
	        words = []
	    words_list = [''.join(item) for item in words_list]
	    return words_list
