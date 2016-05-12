import sys
import re
from bs4 import BeautifulSoup
from gensim.models import doc2vec
import pickle
import scipy.spatial.distance as ds

if __name__ == '__main__':

	out = pickle.load(open(sys.argv[1], 'rb'))
	model = doc2vec.Doc2Vec.load(sys.argv[2])
	test_docs = pickle.load(open(sys.argv[3], 'rb'))
	wfile = open(sys.argv[4], 'w')
	topK = int(sys.argv[5])
	print 'Initialised'
	sys.stdout.flush()
	
	cnt = -1
	for test_doc in test_docs:
		cnt += 1
		body = test_doc['Body']
		expectedTags = test_doc['Tags'].replace('<', ' ').replace('>', ' ').strip().split()
		clean_body = BeautifulSoup(body).get_text()
		clean_body = re.sub(r'\n',' ',clean_body)
		clean_body = re.sub('\W+',' ',clean_body)
		clean_body = re.sub(' . ',' ',clean_body)
		inferVector = model.infer_vector(clean_body.split(), alpha=0.1, min_alpha=0.0001)
		rec_tags = {}
		sims = model.docvecs.most_similar([inferVector])
		for sim in sims:
			doc_id = int(sim[0].split('_')[1])
			prob = sim[1]
			tags = out[doc_id]['tags'].replace('<', ' ').replace('>', ' ').strip().split()
			for tag in tags:
				if tag not in rec_tags:
					rec_tags[tag] = prob
				else:
					rec_tags[tag] += prob

		rec_tags_sorted = sorted(rec_tags.items(), key=lambda x:x[1], reverse= True)
		rec_tags_sorted = rec_tags_sorted[:topK]
		
		sum_ = 0.0
		for item in rec_tags_sorted:
			sum_ += item[1]
		matchedTags = []
		for item in rec_tags_sorted:
			matchedTags.append((item[0],item[1]/sum_))


		temp = {}
		temp['expected'] = expectedTags
		temp['Id'] = test_doc['Id']
		temp['index'] = cnt
		temp['predicted_by_Doc2Vec_Matching'] = matchedTags
		wfile.write(str(temp)+'\n') 
		wfile.flush()
		# print orig_tags, rec_tags_sorted_truncate

	wfile.close()
	# pickle.dump(predicted_tags, open(sys.argv[3], 'wb'))



