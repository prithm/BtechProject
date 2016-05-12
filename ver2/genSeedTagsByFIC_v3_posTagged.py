import sys
import pickle
import nltk
from bs4 import BeautifulSoup
import re
from nltk.stem.porter import *
import os


stemmer = PorterStemmer()

stopwords \
= ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'yo', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
stopwords_2 \
= ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']
stopwords_3 \
= ["'tis","'twas","ain't","aren't","can't","could've","couldn't","didn't","doesn't","don't","hasn't","he'd","he'll","he's","how'd","how'll","how's","i'd","i'll","i'm","i've","isn't","it's","might've","mightn't","must've","mustn't","shan't","she'd","she'll","she's","should've","shouldn't","that'll","that's","there's","they'd","they'll","they're","they've","wasn't","we'd","we'll","we're","weren't","what'd","what's","when","when'd","when'll","when's","where'd","where'll","where's","who'd","who'll","who's","why'd","why'll","why's","won't","would've","wouldn't","you'd","you'll","you're","you've"]

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def convert(name):
	s1 = first_cap_re.sub(r'\1_\2', name)
	return all_cap_re.sub(r'\1_\2', s1).lower()


K_FIC = 70

def find_spreading_actvation(source_tag,predicted_tags,P_tag_tag,cur_hop,max_hop):
	if cur_hop > max_hop:
		return predicted_tags
	else:
		if source_tag not in P_tag_tag.keys():
			return predicted_tags
		for tag in P_tag_tag[source_tag].keys():
			if tag not in predicted_tags.keys():
				predicted_tags[tag] = 0.0
			w = predicted_tags[source_tag]*P_tag_tag[source_tag][tag]
			if w > predicted_tags[tag]:
				predicted_tags[tag] = w
				# predicted_tags = find_spreading_actvation(tag,predicted_tags,P_tag_tag,cur_hop+1,max_hop)
		return predicted_tags

def find_associated_tags(body,P_word_tag,P_tag_tag):
	# words  =  body.split()
	# pos_tags = nltk.pos_tag(words)
	
	predicted_tags = {}
	cumm_n = 0.0
	# for word,pos_tag in pos_tags:
	for word_pos_tag in body:
		
		pos_tag = word_pos_tag.split('_')[-1]
		word = word_pos_tag.split('_')[0]
		
		if not pos_tag.startswith('NN'):
			continue
		# word = word.lower()
		if word.startswith('http://'):
			# print word
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
				
				if word_i in P_word_tag.keys():
					for tag in P_word_tag[word_i].keys():
						if tag not in predicted_tags.keys():
							predicted_tags[tag] = 0.0
						predicted_tags[tag] += P_word_tag[word_i][tag]
						cumm_n += P_word_tag[word_i][tag]
			
	for tag in predicted_tags.keys():
		predicted_tags[tag] /= cumm_n
	
	sorted_x = sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)
	sorted_x = sorted_x[:K_FIC]
	predicted_tags = {}
	for tag,prob in sorted_x:
		predicted_tags[tag] = prob
	
	predicted_tags_keys = predicted_tags.keys()	
	for source_tag in predicted_tags_keys:
		for tag in P_tag_tag[source_tag].keys():
			if tag not in predicted_tags.keys():
				predicted_tags[tag] = 0.0
			w = predicted_tags[source_tag]*P_tag_tag[source_tag][tag]
			if w > predicted_tags[tag]:
				predicted_tags[tag] = w
	return predicted_tags



if __name__ == '__main__':
	validationPosts = pickle.load( open(sys.argv[1], 'rb') )
	print len(validationPosts)
	
	part_ = int(sys.argv[2])
	for part in xrange(part_,part_+1):
		print part
		sys.stdout.flush()
		P_word_tag 	= pickle.load( open(sys.argv[3],'rb'))
		P_tag_tag 	= pickle.load( open(sys.argv[4],'rb'))
		# validationPosts	= pickle.load( open('../data/TestPosts_50K_EnTagRec_'+str(part)+'_.pickle','rb'))

		# validationPrediction = {}
		# validationPrediction['expected'] = []
		# validationPrediction['predicted'] = []
		print 'Init'
		sys.stdout.flush()	
		wfile = open(sys.argv[5], 'w')
		cnt = 0
		for post in validationPosts:
			# if int(post['PostTypeId']) != 1:
			# 	continue
			# print post['Body']
			cnt += 1
			#print cnt
			#sys.stdout.flush()
			if cnt%50 == 0:
				print cnt
				sys.stdout.flush()
				wfile.flush()
				#break
			# body =  BeautifulSoup(post['Body'], 'lxml').get_text()
			# body = re.sub(r'\n',' ',body)
			# body = body.encode("utf-8")
			# body = re.sub('[^a-zA-Z]', ' ', body)
			# curr_tags = post['Tags'].strip().strip('>').strip('<').replace('><', ' ').strip().split(' ')
			# everything['docs'].append(body)
			# everything['tags'].append(curr_tags)
			
			body = post['body']
			curr_tags = post['tags']

			pos_tags = ''
			for word_pos_tag_i in post['postagged']:
				pos_tags += ' ' + word_pos_tag_i
			pos_tags = pos_tags.strip()
			pos_tags_list = pos_tags.split()

			# predicted_tags = find_associated_tags(body,P_word_tag,P_tag_tag)
			predicted_tags = find_associated_tags(pos_tags_list,P_word_tag,P_tag_tag)
			
			sorted_x = sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)
			predicted = sorted_x[:20]
			# validationPrediction['expected'].append(curr_tags)
			# validationPrediction['predicted'].append(predicted)
			tempu = {}
			tempu['expected'] = curr_tags
			
			matched_Tags = []
			sum_ = 0.0
			for it in predicted:
				sum_ += it[1]
			for it in predicted:
				matched_Tags.append( (it[0],it[1]/sum_) )
			tempu['predicted_By_FIC'] = matched_Tags
			wfile.write(str(tempu)+'\n')
			#wfile.flush()
		
		wfile.flush()
		wfile.close()


		# pickle.dump( validationPrediction, open('../data/AllPostsSeedTags_50K_EnTagRec_ByFIC'+str(part)+'_.pickle', 'wb') )
