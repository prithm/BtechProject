import sys
import pickle
import difflib
from bs4 import BeautifulSoup
import re
import distance
from nltk.corpus import stopwords
stop = stopwords.words('english')
import operator
from gensim.models import doc2vec
import scipy.spatial.distance as ds

if __name__ == '__main__':
	print 'initialising'
	posts = pickle.load( open(sys.argv[1], "rb") )
	testPosts = pickle.load( open(sys.argv[2], "rb") )
	model = doc2vec.Doc2Vec.load(sys.argv[3])
	tagSet = set()
	num = 100000
	posts = posts[0:num]
	for post in posts:
		if int(post['postTypeId']) != 1:
			continue
		tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()
		for tag in tags:
			tagSet.add(tag)

	taglist = list(tagSet)

	print 'initialised'
	

	out = []
	for post in testPosts:
		text = BeautifulSoup(post['body']).get_text()
		text = re.sub('(\\n)|(\')|(/)|(\d+)', ' ', text)
		text = text.lower()
		tempDict = {}
		textWords = text.split()
		for textWord in textWords:
			simTags = difflib.get_close_matches(textWord, taglist)
			if len(simTags) > 0 and len(simTags[0]) > 1:
				simTag = simTags[0]
				jac    = 1 - distance.jaccard(textWord, simTag)
				if jac > 0.8:
					if simTag not in tempDict:
						tempDict[simTag] = 0.0
					tempDict[simTag] += jac
		sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1))
		sorted_x.reverse()
		sorted_x = sorted_x[:10]
		print sorted_x
		sum_ = 0.0
		for pair in sorted_x:
			sum_ += pair[1]
		matchedTags = []
		for pair in sorted_x:
			matchedTags.append(pair[0])
		# print matchedTags

		inferVector = model.infer_vector(textWords, alpha=0.1, min_alpha=0.0001)
		rec_tags = {}
		sims = model.docvecs.most_similar([inferVector])
		for sim in sims:
			doc_id = int(sim[0].split('_')[1])
			prob = -sim[1]
			tags = posts[doc_id]['tags'].replace('<', ' ').replace('>', ' ').strip().split()
			for tag in tags:
				if tag not in rec_tags:
					rec_tags[tag] = prob
				else:
					rec_tags[tag] += prob

		rec_tags_sorted = sorted(rec_tags.items(), key=lambda x:x[1])
		rec_tags_sorted_truncate = []
		for i in xrange(0,min(10-len(matchedTags),len(rec_tags_sorted))):
			rec_tags_sorted_truncate.append(rec_tags_sorted[i][0])

		matchedTags += rec_tags_sorted_truncate	
		
		temp = {}
		temp['expected'] = post['expected']
		temp['body'] = post['body']
		temp['predicted_by_Hybrid_Matching'] = matchedTags
		out.append(temp) 

	pickle.dump( out, open(sys.argv[4], "wb") )
	print out
