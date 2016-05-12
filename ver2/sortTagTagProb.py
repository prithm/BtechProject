import sys
import pickle
import operator
import time


# G = nx.DiGraph()
tags = set()
# zeroDict = {}
print "Initialising"
tagTagProbInit = pickle.load(open(sys.argv[1], 'rb'))
print 'Initialised'
sys.stdout.flush()

tagTagProb = {}
tagKeys = set()
ecnt = 0
for tag1,valueDict in tagTagProbInit.items():
	tags.add(tag1)
	tagKeys.add(tag1)
	sorted_x = sorted(valueDict.items(), key=operator.itemgetter(1), reverse=True)
	summ = 0.0
	sorted_x = sorted_x[0:20]
	for item in sorted_x:
		summ = summ + item[1]
	tagTagProb[tag1] = {}
	for item in sorted_x:
		ecnt += 1
		tagTagProb[tag1][item[0]] = item[1]/summ
		tags.add(item[0])
	

print ecnt
sys.stdout.flush()

pickle.dump(tagTagProb, open(sys.argv[2],'wb'))