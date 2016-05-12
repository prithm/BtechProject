import time
import sys
import pickle
import difflib
from bs4 import BeautifulSoup
import re
import distance
# from nltk.corpus import stopwords
# stop = stopwords.words('english')
import operator

print "Initialising"
taglist = pickle.load(open(sys.argv[1], 'rb'))
print 'Initialised'
sys.stdout.flush()


if __name__ == '__main__':
	testPosts = pickle.load( open(sys.argv[2], 'rb') )
	topK = int(sys.argv[3])
	
	wfile = open(sys.argv[4], 'w')
	out = []
	cnt = -1
	cumRec = 0.0
	for post in testPosts:
		#start_time = time.time()
		cnt += 1
		text = post['body']
		# text = BeautifulSoup(post['Body']).get_text()
		# text = re.sub('(\\n)|(\')|(/)|(\d+)', ' ', text)
		# text = text.lower()
		tempDict = {}
		textWords = text.split()
		for textWord in textWords:
			# if textWord in stop:
			# 	continue
			simTags = difflib.get_close_matches(textWord, taglist)
			simTags = simTags[:20]

			for simTag in simTags:
				simTag = simTags[0]
				jac    = 1 - distance.jaccard(textWord, simTag)
				if jac > 0.8:
					if simTag not in tempDict:
						tempDict[simTag] = 0.0
					tempDict[simTag] += jac
		
		sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True)
		sorted_x = sorted_x[:topK]
		
		sum_ = 0.0
		for pair in sorted_x:
			sum_ += pair[1]
		matchedTags = []
		for pair in sorted_x:
			matchedTags.append((pair[0],pair[1]/sum_))
		# print matchedTags

		# tags = post['Tags']
		# expectedTags = tags.replace('<', ' ').replace('>', ' ').strip().split()
		expectedTags = post['tags']

		#predictedTags = [item[0] for item in matchedTags]
		#cumRec += calcRecall(expectedTags, predictedTags)
		
		#print("--- %s seconds ---" % (time.time() - start_time))
		#sys.stdout.flush()
		
		if cnt%500 == 0:
			print cnt 
			sys.stdout.flush()
		
		temp = {}
		temp['expected'] = expectedTags
		temp['Id'] = post['Id']
		temp['index'] = cnt
		temp['predicted_by_String_Matching'] = matchedTags
		wfile.write(str(temp)+'\n') 
		wfile.flush()
		
		#if cnt >= 1:
		#	break

	wfile.close()	
	# pickle.dump( out, open(sys.argv[3], "wb") )
	# print out
	#print cumRec/(cnt+1.0)
