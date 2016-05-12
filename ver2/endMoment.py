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
	surveyqs = pickle.load(open(sys.argv[1],'rb'))
	for surveyq in surveyqs:
		text = surveyq['body']
		text = re.sub('(\\n)|(\')|(/)|(\d+)', ' ', text)
		text = text.lower()
		tempDict = {}
		textWords = text.split()
		simTags = surveyq['predicted_by_Hybrid_Matching']
		for textWord in textWords:
			for simTag in simTags:
				jac    = 1 - distance.jaccard(textWord, simTag)
				if jac > 0.8:
					if simTag not in tempDict:
						tempDict[simTag] = 0.0
					tempDict[simTag] += jac
		
		if len(tempDict.keys()) < len(simTags):
			for simTag in simTags:
				if simTag not in tempDict.keys():
					tempDict[simTag] = 0.0
				tempDict[simTag] += 0.8*tempDict[simTag] + 0.2*(1.0/len(simTags))
		
		sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1), reverse = True)

		summ = 0.0
		for item in sorted_x:
			summ += item[1]
		for i in xrange(0,len(sorted_x)):
			sorted_x[i] = (sorted_x[i][0],sorted_x[i][1]/summ)

		surveyq['probs'] = sorted_x
		print surveyq
		# break		