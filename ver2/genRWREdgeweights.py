import networkx as nx
import sys
import pickle

G = nx.DiGraph()
tags = set()
zeroDict = {}
print "Initialising"
tagTagProb = pickle.load(open(sys.argv[1], 'rb'))
print 'Initialised'
print 'Graph making...'
for tag1,valueDict in tagTagProb.items():
	for tag2,wt in valueDict.items():
		tags.add(tag1)
		tags.add(tag2)
		G.add_edge(tag1, tag2, weight=float(wt))
		zeroDict[tag1] = 0.0
		zeroDict[tag2] = 0.0
print 'Graph made'
tagList = list(tags)		

def genRWR(id_,start,end):
	print start,end,len(tags)
		
	f = open('out_'+str(id_)+'.txt', 'w')
	cnt = 0
	for i in xrange(start,end):
		tag = tagList[start]
		print tag
		cnt += 1
		if cnt%100 == 0:
			print cnt
		tempDict = zeroDict
	 	tempDict[tag] = 1.0
	 	out = {}
	 	out[tag] = nx.pagerank(G, personalization = tempDict, max_iter=100)
	 	f.write(str(out)+'\n')
	 	f.flush()
	 	tempDict[tag] = 0.0
		#if cnt >= 1:
		#	break
	f.close()
	f = open('done_'+str(id_)+'.txt', 'w')
	f.write('done'+'\n')
	f.close()	

if __name__ == '__main__':
	genRWR(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
	
