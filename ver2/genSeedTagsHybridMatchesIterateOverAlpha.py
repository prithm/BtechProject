import sys
import operator
from calcPrecisionRecall import calcPrecision_2, calcRecall_2

if __name__ == '__main__':

	# alpha = float(sys.argv[4])
	topK = 10

	postsWithSeedTags = []
	with open(sys.argv[1], 'r') as f:
		for line in f:
			post = eval(line.strip('\n'))
			postsWithSeedTags.append(post)

	index = -1
	with open(sys.argv[2], 'r') as f:
		for line in f:
			index += 1
			post = eval(line.strip('\n'))
			# if post['index'] != postsWithSeedTags[index]['index']:
			# 	print 'ERROR'
			# 	exit()

			# postsWithSeedTags[index]['predicted_By_FIC'] = post['predicted_By_FIC']
			postsWithSeedTags[index]['predicted_by_Doc2Vec_Matching'] = post['predicted_by_Doc2Vec_Matching']

	wfile = open(sys.argv[3], 'w')
	out = 'alpha,cum_pre@3,cum_pre@5,cum_pre@10,cum_rec@3,cum_rec@5,cum_rec@10'
	wfile.write(out + '\n')

	cum_rec_max = -1.0
	alpha_max = -1.0
	for alpha_i in xrange(0,11):
		cum_rec = [0.0, 0.0, 0.0]
		cum_pre = [0.0, 0.0, 0.0]
		alpha = 0.1*alpha_i
		cnt = 0.0
		for i in xrange(0,len(postsWithSeedTags)):
			post = postsWithSeedTags[i]
			predicted_by_String_Matching = post['predicted_by_String_Matching']
			# predicted_By_FIC = post['predicted_By_FIC']
			predicted_by_Doc2Vec_Matching = post['predicted_by_Doc2Vec_Matching']
			temp = {}
			for tag,prob in predicted_by_String_Matching:
				temp[tag] = alpha*prob
			# for tag,prob in predicted_By_FIC:
			for tag,prob in predicted_by_Doc2Vec_Matching:
				if tag not in temp.keys():
					temp[tag] = (1.0-alpha)*prob
				else:
					temp[tag] += (1.0-alpha)*prob

			sorted_tags = sorted(temp.items(), key=operator.itemgetter(1), reverse=True)
			sorted_tags = sorted_tags[:topK]
			predicted = [it[0] for it in sorted_tags]
			expected = post['expected']
			precision = calcPrecision_2(expected, predicted)
			recall = calcRecall_2(expected, predicted)

			cum_pre[0] += precision[0]
			cum_pre[1] += precision[1]
			cum_pre[2] += precision[2]

			cum_rec[0] += recall[0]
			cum_rec[1] += recall[1]
			cum_rec[2] += recall[2]
			cnt += 1.0
			# matchedTags = []
			# sum_ = 0.0
			# for sorted_tag in sorted_tags:
			# 	sum_ += sorted_tag[1]
			# for sorted_tag in sorted_tags:
			# 	matchedTags.append((sorted_tag[0],sorted_tag[1]/sum_))

		cum_pre[0] /= cnt
		cum_pre[1] /= cnt
		cum_pre[2] /= cnt
		cum_rec[0] /= cnt
		cum_rec[1] /= cnt
		cum_rec[2] /= cnt
		
		if cum_rec[2] > cum_rec_max:
			cum_rec_max = cum_rec[2]
			alpha_max = alpha		
			
		# postsWithSeedTags[i]['predicted_by_StringAndFIC_Matching'] = matchedTags
		out = ''
		out += str(alpha)
		for it in cum_pre:
			out += ',' + str(it)
		for it in cum_rec:
			out += ',' + str(it)
		wfile.write(out+'\n')
		print out
		wfile.flush()

	wfile.close()












# import sys
# import pickle
# import difflib
# from bs4 import BeautifulSoup
# import re
# import distance
# from nltk.corpus import stopwords
# stop = stopwords.words('english')
# import operator
# from gensim.models import doc2vec
# import scipy.spatial.distance as ds

# if __name__ == '__main__':
# 	print 'initialising'
# 	posts = pickle.load( open(sys.argv[1], "rb") )
# 	testPosts = pickle.load( open(sys.argv[2], "rb") )
# 	model = doc2vec.Doc2Vec.load(sys.argv[3])
# 	tagSet = set()
# 	num = 1000
# 	posts = posts[0:num]
# 	for post in posts:
# 		if int(post['postTypeId']) != 1:
# 			continue
# 		tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()
# 		for tag in tags:
# 			tagSet.add(tag)

# 	taglist = list(tagSet)

# 	print 'initialised'
	

# 	out = []
# 	for post in testPosts:
# 		text = BeautifulSoup(post['body']).get_text()
# 		text = re.sub('(\\n)|(\')|(/)|(\d+)', ' ', text)
# 		text = text.lower()
# 		tempDict = {}
# 		textWords = text.split()
# 		for textWord in textWords:
# 			simTags = difflib.get_close_matches(textWord, taglist)
# 			if len(simTags) > 0 and len(simTags[0]) > 1:
# 				simTag = simTags[0]
# 				jac    = 1 - distance.jaccard(textWord, simTag)
# 				if jac > 0.8:
# 					if simTag not in tempDict:
# 						tempDict[simTag] = 0.0
# 					tempDict[simTag] += jac
# 		sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1))
# 		sorted_x.reverse()
# 		sorted_x = sorted_x[:10]
# 		print sorted_x
# 		sum_ = 0.0
# 		for pair in sorted_x:
# 			sum_ += pair[1]
# 		matchedTags = []
# 		for pair in sorted_x:
# 			matchedTags.append(pair[0])
# 		# print matchedTags

# 		inferVector = model.infer_vector(textWords, alpha=0.1, min_alpha=0.0001)
# 		rec_tags = {}
# 		sims = model.docvecs.most_similar([inferVector])
# 		for sim in sims:
# 			doc_id = int(sim[0].split('_')[1])
# 			prob = -sim[1]
# 			tags = posts[doc_id]['tags'].replace('<', ' ').replace('>', ' ').strip().split()
# 			for tag in tags:
# 				if tag not in rec_tags:
# 					rec_tags[tag] = prob
# 				else:
# 					rec_tags[tag] += prob

# 		rec_tags_sorted = sorted(rec_tags.items(), key=lambda x:x[1])
# 		rec_tags_sorted_truncate = []
# 		for i in xrange(0,min(10-len(matchedTags),len(rec_tags_sorted))):
# 			rec_tags_sorted_truncate.append(rec_tags_sorted[i][0])

# 		matchedTags += rec_tags_sorted_truncate	
		
# 		temp = {}
# 		temp['expected'] = post['expected']
# 		temp['body'] = post['body']
# 		temp['predicted_by_Hybrid_Matching'] = matchedTags
# 		out.append(temp) 

# 	pickle.dump( out, open(sys.argv[4], "wb") )
# 	print out
