import sys
import re
from bs4 import BeautifulSoup
from gensim.models import doc2vec
import pickle
import scipy.spatial.distance as ds

if __name__ == '__main__':
	out = pickle.load(open(sys.argv[1], 'rb'))
	model = doc2vec.Doc2Vec.load(sys.argv[2])
	test_docs = out[2001:2020]
	predicted_tags = []

	for test_doc in test_docs:
		if int(test_doc['postTypeId']) != 1:
			continue
		body = test_doc['Body']
		orig_tags = test_doc['tags'].replace('<', ' ').replace('>', ' ').strip().split()
		clean_body = BeautifulSoup(body).get_text()
		clean_body = re.sub(r'\n',' ',clean_body)
		clean_body = re.sub('\W+',' ',clean_body)
		clean_body = re.sub(' . ',' ',clean_body)
		inferVector = model.infer_vector(clean_body.split(), alpha=0.1, min_alpha=0.0001)
		rec_tags = {}
		sims = model.docvecs.most_similar([inferVector])
		for sim in sims:
			doc_id = int(sim[0].split('_')[1])
			prob = -sim[1]
			tags = out[doc_id]['tags'].replace('<', ' ').replace('>', ' ').strip().split()
			for tag in tags:
				if tag not in rec_tags:
					rec_tags[tag] = prob
				else:
					rec_tags[tag] += prob

		rec_tags_sorted = sorted(rec_tags.items(), key=lambda x:x[1])
		rec_tags_sorted_truncate = []
		for i in xrange(0,min(10,len(rec_tags_sorted))):
			rec_tags_sorted_truncate.append(rec_tags_sorted[i][0])

		temp = {}
		temp['expected'] = orig_tags
		temp['predicted'] = rec_tags_sorted_truncate
		temp['body'] = BeautifulSoup(body).get_text()
		predicted_tags.append(temp)
		print orig_tags, rec_tags_sorted_truncate

	pickle.dump(predicted_tags, open(sys.argv[3], 'wb'))



