import sys
import pickle
import difflib
from bs4 import BeautifulSoup
import re
import distance
from nltk.corpus import stopwords
stop = stopwords.words('english')
import operator

if __name__ == '__main__':
	print 'initialising'
	taglist = pickle.load( open(sys.argv[1], "rb") )
	posts = pickle.load( open(sys.argv[2], "rb") )
	print 'initialised'
	out = {}
	for post in posts:
		if int(post['postTypeId']) != 1:
			continue
		text = BeautifulSoup(post['Body']).get_text()
		text = re.sub('(\\n)|(\')|(/)|(\d+)', ' ', text)
		text = text.lower()
		tempDict = {}
		textWords = text.split()
		for textWord in textWords:
			if textWord not in stop and len(textWord) > 2:
				simTag = difflib.get_close_matches(textWord, taglist)[0]
				jac    = 1 - distance.jaccard(textWord, simTag)
				if simTag not in tempDict:
					tempDict[simTag] = 0.0
				tempDict[simTag] += jac
		sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1))
		sorted_x.reverse()
		sorted_x = sorted_x[:10]
		sum_ = 0.0
		for pair in sorted_x:
			sum_ += pair[1]
		matchedTags = []
		for pair in sorted_x:
			matchedTags.append((pair[0],pair[1]/sum_))
		print matchedTags
		outDict = post
		outDict['MatchedTags'] = matchedTags
		out[post['Id']] = outDict	
		break

	pickle.dump( out, open(sys.argv[3], "wb") )
	print out
