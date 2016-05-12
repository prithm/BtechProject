import sys
import pickle
from bs4 import BeautifulSoup
import re
from gensim import corpora, models, similarities
from collections import defaultdict
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
	
	# topic_tag =	pickle.load( open('topic_tag.pickle', 'rb') )
	# topic_tag_sorted = {}
	# for topic in topic_tag.keys():
	# 	sorted_x = sorted(topic_tag[topic].items(), key=lambda x:x[1], reverse= True)
	# 	sorted_x = sorted_x[:20]
	# 	topic_tag_sorted[topic] = sorted_x
	# pickle.dump( topic_tag_sorted, open('topic_tag_sorted.pickle', 'wb') )
	# exit()


	print 'Initialising Docs'
	sys.stdout.flush()

	# SAVING PART-----------------------------------------
	validationPosts = pickle.load( open(sys.argv[1], 'rb') )
	everything = {}
	documents = []
	tags = []
	cnt = 0
	for post in validationPosts:
		if int(post['PostTypeId']) != 1:
			continue
		# print post['Body']
		cnt += 1
		body =  BeautifulSoup(post['Body'], 'lxml').get_text()
		body = re.sub(r'\n',' ',body)
		body = body.encode("utf-8")
		body = re.sub('[^a-zA-Z]', ' ', body)
		curr_tags = post['Tags'].strip().strip('>').strip('<').replace('><', ' ').strip().split(' ')
		documents.append(body)
		tags.append(curr_tags)
		# print curr_tags
		# break
		# if cnt >= 10:
		# 	break	
	print 'Initialising Docs done....'
	sys.stdout.flush()
	
	#LOADING PART-----------------------------------------
	print 'Initialising Dict'
	sys.stdout.flush()
	
	dictionary = corpora.Dictionary.load('ldadict.dict')
	tfidf = models.TfidfModel.load('TfIdf.tfidf')
	
	# #print(dictionary)
	# #print(dictionary.token2id)

	id2word = {}
	for key,val in dictionary.token2id.items():
		id2word[val] = key

	print 'Initialising Dict done....'
	sys.stdout.flush()
	
	#LOADING PART-----------------------------------------
	print 'Initialising Corpus'
	sys.stdout.flush()
	
	mm = corpora.MmCorpus('ldacorpusmm.mm')

	print 'Initialising Corpus done....'
	sys.stdout.flush()
	
	#LOADING PART------------------------------------------
	print 'Initialising LDA '
	sys.stdout.flush()
	
	lda = models.ldamodel.LdaModel.load('ldamodel.model')

	print 'Initialising LDA done....'
	sys.stdout.flush()
	
	doc_topics = []
	
	#FOR NON CORPUS DOC--------------------------------------------------
	print 'Initialising topic probs for docs'
	sys.stdout.flush()
	
	topic_tag =	pickle.load( open('topic_tag_sorted.pickle', 'rb') )
	predicted_tags = []
	for i in xrange(0,len(documents)):
		if i%500 == 0:
			print i
			sys.stdout.flush()
		new_vec = tfidf[dictionary.doc2bow(documents[i].lower().split())]
		doc_lda = lda[new_vec]
		tempDict = {}
		tag_probs = {}
		for x in doc_lda:
			topic = x[0]
			prob = x[1]
			# print topic
			# sys.stdout.flush()
			for tag,tag_prob in topic_tag[topic]:
				if tag not in tag_probs.keys():
					tag_probs[tag] = 0.0
				tag_probs[tag] += tag_prob*prob
		sorted_x = sorted(tag_probs.items(), key=lambda x:x[1], reverse= True)
		predicted = sorted_x[:20]
		predicted_tags.append(predicted)	
		# print predicted
		# break
			
	validationPrediction = {}
	validationPrediction['expected'] = tags
	validationPrediction['predicted'] = predicted_tags

	pickle.dump( validationPrediction, open('validationSeedTagsByLDA_2.pickle', 'wb') )
	
