import sys
import pickle
from bs4 import BeautifulSoup
import re
from gensim import corpora, models, similarities
from collections import defaultdict
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == '__main__':
	
	print 'Initialising Docs'
	sys.stdout.flush()
	
	# SAVING PART-----------------------------------------
	trainingPosts = pickle.load( open(sys.argv[1], 'rb') )
	everything = {}
	everything['docs'] = []
	everything['tags'] = []
	cnt = 0
	for post in trainingPosts:
		cnt += 1
		everything['docs'].append(post['body'])
		everything['tags'].append(post['tags'])
		# if cnt >= 10:
		# 	break
	pickle.dump(everything, open('LDA_50K_EnTagRec_Corpus.pickle','wb'))
	# print len(everything['docs']),len(everything['tags'])	
	
	#LOADING PART--------------------------------------------
	
	# everything = pickle.load( open(sys.argv[1], 'rb') )
	documents = everything['docs']
	tags = everything['tags']
	print len(documents),len(tags)

	print 'Initialising Docs done....'
	sys.stdout.flush()
	
	print 'Initialising Dict'
	sys.stdout.flush()
	
	#SAVING PART----------------------------------------------------
	# stoplist = set('how why has have where are not was is can from more may when whether there here for a of the and to in an then see it i he she'.split())
	texts = [[word for word in document.lower().split()] for document in documents]
	frequency = defaultdict(int)
	for text in texts:
		for token in text:
			frequency[token] += 1
	texts = [[token for token in text if frequency[token] > 1] for text in texts]
	
	dictionary = corpora.Dictionary(texts)
	dictionary.save('ldadict.dict')
	
	#LOADING PART-----------------------------------------
	# dictionary = corpora.Dictionary.load('ldadict.dict')
	# #print(dictionary)
	# #print(dictionary.token2id)

	id2word = {}
	for key,val in dictionary.token2id.items():
		id2word[val] = key

	print 'Initialising Dict done....'
	sys.stdout.flush()
	
	print 'Initialising Corpus'
	sys.stdout.flush()
	
	#SAVING PART-----------------------------------------	
	corpus_ = [dictionary.doc2bow(text) for text in texts]
	tfidf = models.TfidfModel(corpus_)
	tfidf.save('TfIdf.tfidf')
	mm = [tfidf[vec] for vec in corpus_]
	corpora.MmCorpus.serialize('ldacorpusmm.mm', mm)
	
	# print 'Corpus Done'
	
	#LOADING PART-----------------------------------------
	# mm = corpora.MmCorpus('ldacorpusmm.mm')

	print 'Initialising Corpus done....'
	sys.stdout.flush()
	
	print 'Initialising LDA '
	sys.stdout.flush()

	# SAVING PART-------------------------------------------
	lda = models.ldamodel.LdaModel(corpus=mm, id2word = id2word, num_topics=100, update_every=1, chunksize=1000, passes=1)
	lda.save('ldamodel.model')

	#LOADING PART------------------------------------------
	
	# lda = models.ldamodel.LdaModel.load('ldamodel.model')

	print 'Initialising LDA done....'
	sys.stdout.flush()
	
	# a = lda.show_topics(num_topics=100, num_words=10)
	# for ai in a:
	# 	print ai
	
	doc_topics = []
	
	#FOR NON CORPUS DOC--------------------------------------------------
	# for new_doc in documents:
	# 	new_doc = "define int percentage"
	# 	new_vec = tfidf[dictionary.doc2bow(new_doc.lower().split())]
	# 	doc_lda = lda[new_vec]
	# 	temp = []
	# 	for x in doc_lda:
	# 		temp.append(x[1])
	# 	doc_topics.append(temp)
	
	#FOR OLD DOCS---------------------------------------------------------
	print 'Initialising topic probs for docs'
	sys.stdout.flush()
	
	for old_vec in mm:
		doc_lda = lda[old_vec]
		# print doc_lda
		tempDict = {}
		for x in doc_lda:
			tempDict[x[0]] = x[1]
			# print temp
		# break
		doc_topics.append(tempDict)
	
	print 'Initialising topic probs for docs done....'
	sys.stdout.flush()
	
	# num_topics = len(doc_topics[0])

	print 'Initialising tag topic probs for docs'
	sys.stdout.flush()
	
	topic_tag = {}
	topic_den = {}
	for i in xrange(0,len(documents)):
		for topic in doc_topics[i].keys():
			if topic not in topic_den.keys():
				topic_den[topic] = 0.0
			topic_den[topic] += doc_topics[i][topic]

			if topic not in topic_tag.keys():
				topic_tag[topic] = {}		
			
			for tag in tags[i]:
				if len(tag) > 0:
					if tag not in topic_tag[topic].keys():
						topic_tag[topic][tag] = 0.0
					topic_tag[topic][tag] += doc_topics[i][topic] * 1.0 / len(tags[i])
			
	z = {}
	for topic in topic_tag.keys():
		z[topic] = 0.0
		for tag in topic_tag[topic].keys():
			topic_tag[topic][tag] /= topic_den[topic]
			z[topic] += topic_tag[topic][tag]

	for topic in topic_tag.keys():
		for tag in topic_tag[topic].keys():
			topic_tag[topic][tag] /= z[topic]
		
	pickle.dump(topic_tag, open('topic_tag.pickle', 'wb'))

	print 'Initialising tag topic probs for docs done....'
	sys.stdout.flush()


	print 'Validating on trainingPosts'
	sys.stdout.flush()

	validationPrediction = {}
	validationPrediction['expected'] = []
	validationPrediction['predicted'] = []

	wfile = open('../data/AllPostsSeedTags_50K_EnTagRec_ByLDA.txt','w')
	for i in xrange(0,len(documents)):
		print i
		sys.stdout.flush()

		predicted_tags = {}
		
		for topic in doc_topics[i].keys():
			for tag in topic_tag[topic].keys():
				if tag not in predicted_tags.keys():
					predicted_tags[tag] = 0.0
				predicted_tags[tag] += doc_topics[i][topic]*topic_tag[topic][tag]
		
		sorted_x = sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)
		predicted = sorted_x
		tempu = {}
		tempu['expected'] = tags[i]
		tempu['predicted'] = predicted
		wfile.write(str(tempu)+'\n')
		wfile.flush()

	wfile.flush()
	wfile.close()

	# pickle.dump( validationPrediction, open('AllPostsSeedTags_50K_EnTagRec_ByLDA.pickle', 'wb') )

	