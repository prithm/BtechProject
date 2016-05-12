import sys
from calcPrecisionRecall import calcPrecision_2, calcRecall_2

if __name__ == '__main__':
	wfile = open(sys.argv[2],'w')
	
	with open(sys.argv[1], 'r') as f:
		for line in f:
			post = eval(line.strip('\n'))
			expectedTags = post['expected']
			metapathnum = 0
			overallPrecRec = {}
			
			for ranklist in post['predicted_by_Metapaths_Combined_Ranks']:
				matchedTags = []
				predictedTags = [item[0] for item in ranklist]
				prec = calcPrecision_2(expectedTags, predictedTags)
				rec = calcRecall_2(expectedTags, predictedTags)
				overallPrecRec[str(metapathnum)] = {}
				overallPrecRec[str(metapathnum)]['prec'] = prec
				overallPrecRec[str(metapathnum)]['rec'] = rec
				metapathnum += 1	
			
			predictedTags = [item[0] for item in post['final_Recommended_Tags']]
			prec = calcPrecision_2(expectedTags, predictedTags)
			rec = calcRecall_2(expectedTags, predictedTags)
			overallPrecRec['hybrid_all_metapaths'] = {}
			overallPrecRec['hybrid_all_metapaths']['prec'] = prec
			overallPrecRec['hybrid_all_metapaths']['rec'] = rec
			post['PreRecMeasure'] = overallPrecRec
			wfile.write(str(post)+'\n')
			wfile.flush()

	wfile.close()