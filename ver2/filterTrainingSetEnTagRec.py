import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle
from nltk.stem.porter import *
import re
import os


stemmer = PorterStemmer()

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def convert(name):
	s1 = first_cap_re.sub(r'\1_\2', name)
	return all_cap_re.sub(r'\1_\2', s1).lower()

# from nltk.corpus import stopwords

stopwords \
= ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'yo', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
stopwords_2 \
= ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']
stopwords_3 \
= ["'tis","'twas","ain't","aren't","can't","could've","couldn't","didn't","doesn't","don't","hasn't","he'd","he'll","he's","how'd","how'll","how's","i'd","i'll","i'm","i've","isn't","it's","might've","mightn't","must've","mustn't","shan't","she'd","she'll","she's","should've","shouldn't","that'll","that's","there's","they'd","they'll","they're","they've","wasn't","we'd","we'll","we're","weren't","what'd","what's","when","when'd","when'll","when's","where'd","where'll","where's","who'd","who'll","who's","why'd","why'll","why's","won't","would've","wouldn't","you'd","you'll","you're","you've"]

#postType ownerUser postId parentId tags
def filter(input):
	posts = pickle.load( open(input, 'rb') )
	print len(posts)
	exit()

	cnt = 0
	word_count = {}
	wfile = open('test.txt','w')
	for post in posts:
		cnt += 1	
		# if cnt%1000 == 0:
		# 	print cnt
		# 	s
		body = post['body']
		body =  BeautifulSoup(body, 'lxml').get_text()
		body = re.sub(r'\n',' ',body)
		# body = body.encode("utf-8")
		words = body.split()
		post['words'] = []
		out1 = ''
		out2 = ''
		for word in words:
			word_filter = word.strip()
			word_filter = re.sub('^[^a-zA-Z]+', ' ', word_filter)
			word_filter = re.sub('[^a-zA-Z]+$', ' ', word_filter)
			word_filter = re.sub('^[\d]+', ' ', word_filter)
			word_filter = re.sub('[\d]+$', ' ', word_filter)
			word_filter = word_filter.strip()
			out1 += ' ' + word_filter
			# post['words'].append(word_filter)
			new_words = word_filter.split()
			for w in new_words:
				w = w.lower()
				if w not in stopwords and w not in stopwords_2 and w not in stopwords_3:
					w = stemmer.stem(w)
					w = re.sub('[^a-zA-Z]',' ',w)
					wss = w.split()
					for ws in wss:
						if ws not in word_count.keys():
							word_count[ws] = 0
						word_count[ws] += 1
						out2 += ' ' + ws	
		
		os.system(command)	
		wfile.write(body+'\n')
		wfile.write(out1+'\n')
		wfile.write(out2+'\n')
		wfile.flush()
		if cnt > 5:
			break

	wfile.close()		
		# for word in words:
		# 	new_words = convert(word).split('_')
		# 	for new_word in new_words:
		# 		if new_word in stopwords or new_word in stopwords_2 or new_word in stopwords_3:
		# 			continue
		# 		else:
		# 			new_word = new_word.lower()
		# 			new_word = stemmer.stem(new_word)
		# 			if new_word == 'c' or len(new_word) > 1:
		# 				filtered_body += ' ' + new_word
	l = 0
	for key in word_count.keys():
		if word_count[key] >= 20:
			l+=1
	print l
	print len(word_count.keys())	

def main():
	filter(sys.argv[1])

if __name__ == '__main__':
	main()
