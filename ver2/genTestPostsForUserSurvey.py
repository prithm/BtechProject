import sys
import pickle

if __name__ == '__main__':
	testPostsOrig = pickle.load(open(sys.argv[1],'rb'))
	testIndices = {}
	cnt = 0
	with open(sys.argv[2],'r') as f:
		for line in f:
			cnt += 1
			if cnt <= 50:
				testIndices[int(line.strip('\n'))] = 'LowerViewCount'
			else:
				testIndices[int(line.strip('\n'))] = 'HigherViewCount' 
	testPostsResults = []
	cnt = -1
	out = []
	with open(sys.argv[3],'r') as f:
		for line in f:
			cnt += 1
			if cnt in testIndices.keys():
				post = eval(line.strip())
				body = testPostsOrig[cnt]['Body']
				expected = post['expected']
				seedSet = [i[0] for i in post['predicted_by_Hybrid_Matching']]
				metapaths = [i[0] for i in post['final_Recommended_Tags']]
				tempDict = {}
				tempDict['Body'] = body
				tempDict['expected'] = expected
				tempDict['predicted_by_Hybrid_Matching'] = seedSet
				tempDict['final_Recommended_Tags'] = metapaths
				tempDict['ViewCount'] = testIndices[cnt]
				out.append(tempDict)

	pickle.dump(out, open(sys.argv[4], 'wb'))