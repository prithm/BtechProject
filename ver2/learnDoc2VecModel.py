import sys
import re
from bs4 import BeautifulSoup
from gensim.models import doc2vec
import pickle
import scipy.spatial.distance as ds

if __name__ == '__main__':
	out = pickle.load(open(sys.argv[1], 'rb'))
	sentences = []
	num = len(out)
	for i in xrange(0, num):
		if int(out[i]['postTypeId']) != 1:
			continue
		body = out[i]['Body']
		tags = out[i]['tags']
		expected = tags.replace('<', ' ').replace('>', ' ').strip().split()
		if len(expected) <= 0:
			continue
		clean_body = BeautifulSoup(body).get_text()
		clean_body = re.sub(r'\n',' ',clean_body)
		clean_body = re.sub('\W+',' ',clean_body)
		clean_body = re.sub(' . ',' ',clean_body)
		string = "SENT_" + str(i)
		sentence = doc2vec.LabeledSentence(clean_body.split(), [string])
		sentences.append(sentence)
		# print clean_body
		
	print "Finished Preprocessing"
	model = doc2vec.Doc2Vec(sentences, size=40, window=8, min_count=1, workers=1, alpha=0.1, min_alpha=0.0001)	
	model.save(sys.argv[2])
	print 'done'

	# for i in xrange(0,num):
	# 	string = "SENT_" + str(i)
	# 	vec = model.docvecs[string]
	# 	tags = out[i]['tags'].replace('<', ' ').replace('>', ' ').strip().split()
	# 	for tag in tags:
	# 		if tag not in tag_counts:
	# 			tag_counts[tag] = 1
	# 			tag_vectors[tag] = vec
	# 		else:
	# 			tag_counts[tag] += 1
	# 			tag_vectors[tag] += vec

		
	# for tag in tag_vectors.keys():
	# 	tag_vectors[tag] = tag_vectors[tag]/tag_counts[tag]		


	# print out[0]['tags']
	# body = out[0]['Body']
	# clean_body = BeautifulSoup(body).get_text()
	# clean_body = re.sub(r'\n',' ',clean_body)
	# clean_body = re.sub('\W+',' ',clean_body)
	# clean_body = re.sub(' . ',' ',clean_body)
	# getTags(sys.argv[2],clean_body)
