import sys
import pickle
import nltk
from nltk.stem.porter import *
import re
import os

stopwords \
= ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'yo', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
stopwords_2 \
= ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']
stopwords_3 \
= ["'tis","'twas","ain't","aren't","can't","could've","couldn't","didn't","doesn't","don't","hasn't","he'd","he'll","he's","how'd","how'll","how's","i'd","i'll","i'm","i've","isn't","it's","might've","mightn't","must've","mustn't","shan't","she'd","she'll","she's","should've","shouldn't","that'll","that's","there's","they'd","they'll","they're","they've","wasn't","we'd","we'll","we're","weren't","what'd","what's","when","when'd","when'll","when's","where'd","where'll","where's","who'd","who'll","who's","why'd","why'll","why's","won't","would've","wouldn't","you'd","you'll","you're","you've"]


stemmer = PorterStemmer()

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def convert(name):
	s1 = first_cap_re.sub(r'\1_\2', name)
	return all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == '__main__':
	everything = pickle.load( open(sys.argv[1], 'rb') )
	num = len(everything)
	
	#part is the part being left out part = 1, means 2 to 10 are taken
	for part in xrange(0,1):
		P_word_tag = {}
		P_tag_tag = {}
		P_tag = {}
		test_posts = []
		start = int(0.1*(part)*num)
		end = int(0.1*(part+1)*num)
		cnt = 0

		for i in xrange(0,num):

			cnt += 1
			if cnt % 100 == 0:
				print cnt
				sys.stdout.flush()

			if i >= start and i < end:
				test_posts.append(everything[i])
				continue
			
			tags = everything[i]['tags']
			# words  =  everything[i]['body'].strip().split()
			# pos_tags = nltk.pos_tag(words)
			pos_tags = ''
			for word_pos_tag_i in everything[i]['postagged']:
				pos_tags += ' ' + word_pos_tag_i
			pos_tags = pos_tags.strip()
			pos_tags_list = pos_tags.split()

			# for word,pos_tag in pos_tags:
			for word_pos_tag in pos_tags_list:
				pos_tag = word_pos_tag.split('_')[-1]
				word = word_pos_tag.split('_')[0]
				if not pos_tag.startswith('NN'):
					continue
				#word = word.lower()
				if word.startswith('http://'):
					print word
					continue

				if word.lower() in stopwords or word.lower() in stopwords_2 or word.lower() in stopwords_3:
					# print word,pos_tag
					continue
				word = re.sub('^[\d]+', ' ', word)
				word = re.sub('[\d]+$', ' ', word)
				word = word.strip()
				
				if len(word) == 0:
					continue

				words_ = word.split('.')
				for words_i in words_:
					words = convert(words_i).split('_')
					for word_i in words:
						# if re.sub()
						word_i = word_i.lower()
						try:
							word_i = stemmer.stem(word_i)
						except Exception as e:
							# print word
							continue

						if word_i not in P_word_tag.keys():
							P_word_tag[word_i] = {}
						for tag in tags:
							P_word_tag[word_i][tag] = 1.0
				
			for tag in tags:		
				if tag not in P_tag.keys():
					P_tag[tag] = 0.0
				P_tag[tag] += 1.0

			if len(tags) > 0:
				for j in xrange(0,len(tags)):
					if tags[j] not in P_tag_tag.keys():
						P_tag_tag[tags[j]] = {}				
					for k in xrange(0,len(tags)):
						if j == k:
							continue
						if tags[k] not in P_tag_tag[tags[j]].keys():
							P_tag_tag[tags[j]][tags[k]] = 0.0	
						P_tag_tag[tags[j]][tags[k]] += 1.0

		for tag_1 in P_tag_tag.keys():
			for tag_2 in P_tag_tag[tag_1].keys():
				P_tag_tag[tag_1][tag_2] /= (P_tag[tag_1]+P_tag[tag_2]-P_tag_tag[tag_1][tag_2])


		pickle.dump(P_word_tag, open('P_word_tag_50K_EnTagRec_PosTagged_'+str(part)+'_.pickle','wb'))
		pickle.dump(P_tag_tag,  open('P_tag_tag_50K_EnTagRec_PosTagged_'+str(part)+'_.pickle','wb'))
		pickle.dump(test_posts, open('TestPosts_50K_EnTagRec_PosTagged_'+str(part)+'_.pickle','wb'))
