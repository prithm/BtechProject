import sys
import pickle


if __name__ == '__main__':
	train_posts = pickle.load( open(sys.argv[1], 'rb' ) )
	wordvecs = pickle.load( open(sys.argv[2], 'rb' ) )
	n_term_tag = {}
	n_tag = {}
	for post in train_posts:
		post_id = post['Id']
		terms = wordvecs[post_id]['terms'].split()
		tags = post['tags'].strip('<').strip('>').split('><')
		seen = {}
		for tag in tags:
			if tag not in n_tag.keys():
				n_tag[tag] = 1.0
			else:
				n_tag[tag] += 1.0

		for term in terms:
			if term not in seen.keys():
				seen[term] = 1
				if term not in n_term_tag.keys():
					n_term_tag[term] = {}
				for tag in tags:
					if tag not in n_term_tag[term].keys():
						n_term_tag[term][tag] = 1.0
					else:
						n_term_tag[term][tag] += 1.0



	for term in n_term_tag.keys():
		for tag in n_term_tag[term].keys():
			n_term_tag[term][tag] /= n_tag[tag]


	pickle.dump(n_term_tag, open(sys.argv[3],'wb'))
