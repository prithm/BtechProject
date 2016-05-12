import sys
import rank_aggregators as r
import pickle

def get_combined_ranks(ranklists):
	emptyRankList = 0
	nonEmptyRankList = -1
	for ranklist in ranklists:
		if len(ranklist) == 0:
			emptyRankList += 1
	if emptyRankList >= 1:
		for ranklist in ranklists:
			if len(ranklist) > 0:
				sorted_ranklist = sorted(ranklist.items(), key=lambda x:x[1], reverse = True)
				return sorted_ranklist[:10],1.0
		return None,None

	ranker_names = [str(i) for i in xrange(0,len(ranklists))]
	objects = {}
	oid = 0
	oid_name = {}
	num = len(ranklists)
	for i in xrange(0,num):
		sorted_ranklist = sorted(ranklists[i].items(), key=lambda x:x[1], reverse = True)
		for k in xrange(0,len(sorted_ranklist)):
			key = sorted_ranklist[k][0]
			val = float(sorted_ranklist[k][1])
			if key not in objects:
				oid_name[oid] = key
				oid += 1
				objects[oid] = [None for j in xrange(0,num)]
			objects[oid][i] = k
	
	alpha = 0.85
	ranker, score = r.pagerank_aggregator(objects, 0.000001, alpha)
	final_ranklist = sorted(ranker.items(), key=lambda x:x[1])
	final_ranklist = final_ranklist[:10]
	final_keys = []
	for i in xrange(0,len(final_ranklist)):
		final_keys.append(oid_name[final_ranklist[i][0]])
	return final_keys,score

if __name__ == '__main__':
	ranklists = pickle.load( open(sys.argv[1], 'rb'))
	ranker, score = get_combined_ranks(ranklists) 
	print score
	pickle.dump(ranker, open(sys.argv[2], 'wb'))
	print 'Done'
