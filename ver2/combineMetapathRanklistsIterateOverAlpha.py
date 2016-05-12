import sys
from calcPrecisionRecall import calcPrecision_2, calcRecall_2

if __name__ == '__main__':

	wfile = open(sys.argv[2], 'w')
	metapathcnt = int(sys.argv[3])
	# alpha = float(sys.argv[4])
	out = 'alpha,'
	out += 'pre1@3,pre1@5,pre1@10,'
	out += 'rec1@3,rec1@5,rec1@10,'
	out += 'pre2@3,pre2@5,pre2@10,'
	out += 'rec2@3,rec2@5,rec2@10,'
	out += 'pre3@3,pre3@5,pre3@10,'
	out += 'rec3@3,rec3@5,rec3@10'
	out += '\n'
	wfile.write(out)
	wfile.flush()	
		
	for alpha_i in xrange(0,11):
		alpha = 0.1*alpha_i
		cumPre = []
		cumRec = []
		for i in xrange(0,metapathcnt):
			cumPre.append([0.0, 0.0, 0.0])
			cumRec.append([0.0, 0.0, 0.0])

		totcnt = 0.0
	
		with open(sys.argv[1], 'r') as f:
			for line in f:
				totcnt += 1.0
				post = eval(line.strip('\n'))
				seedTagProb = {}

				expectedTags = post['expected']

				# for item in post['predicted_by_StringAndFIC_Matching']:predicted_by_StringAndWVTool_Matching
				for item in post['predicted_by_StringAndWVTool_Matching']:
					seedTagProb[item[0]] = item[1]

				overall = {}
				for i in xrange(0,metapathcnt):
					overall[i] = {}
				for seedTag in post['predicted_by_Metapaths'].keys():
					metapathnum = 0
					for ranklist in post['predicted_by_Metapaths'][seedTag]:
						rank_num = 0.0
						for item in ranklist:
							rank_num += 1.0
							rec_tag = item[0]
							#rec_prob = item[1]/rank_num
							rec_prob = item[1]/1.0
							if metapathnum not in overall.keys():
								overall[metapathnum] = {}
							if rec_tag not in overall[metapathnum].keys():
								overall[metapathnum][rec_tag] = 0.0

							#overall[metapathnum][rec_tag] += alpha*rec_prob + (1.0-alpha)*(seedTagProb[seedTag])
							overall[metapathnum][rec_tag] += (1.0-alpha)*rec_prob*(seedTagProb[seedTag])
							if rank_num >= 10.0:
								break
						metapathnum += 1	
				
				for metapathnum in overall.keys():
					for rec_tag in overall[metapathnum].keys():
						if rec_tag in seedTagProb.keys():
							overall[metapathnum][rec_tag] += alpha * seedTagProb[rec_tag]
				
				# post['predicted_by_Metapaths_Combined_Ranks'] = []		
				for i in xrange(0,metapathcnt):		
					sorted_x = sorted(overall[i].items(), key=lambda x:x[1], reverse= True)
					sorted_x = sorted_x[:20]
					sum_ = 0.0
					for item in sorted_x:
						sum_ += item[1]
					matchedTags = []
					for item in sorted_x:
						matchedTags.append((item[0],item[1]/sum_))

					predictedTags = [item[0] for item in matchedTags]
					prec = calcPrecision_2(expectedTags, predictedTags)
					rec = calcRecall_2(expectedTags, predictedTags)
					# post['predicted_by_Metapaths_Combined_Ranks'].append(matchedTags)
					cumPre[i][0] += prec[0]
					cumPre[i][1] += prec[1]
					cumPre[i][2] += prec[2]
					cumRec[i][0] += rec[0]
					cumRec[i][1] += rec[1]
					cumRec[i][2] += rec[2]				
		
	
		out = str(alpha) + ','
		for j in xrange(0, metapathcnt):
			out += str(cumPre[j][0]/totcnt) + ',' + str(cumPre[j][1]/totcnt) + ',' + str(cumPre[j][2]/totcnt) + ',' 
			out += str(cumRec[j][0]/totcnt) + ',' + str(cumRec[j][1]/totcnt) + ',' + str(cumRec[j][2]/totcnt) + ',' 
		out += '\n'
		print out
		wfile.write(out)
		wfile.flush()	

	wfile.close()







# import sys
# import rank_aggregators as r
# import pickle

# def get_combined_ranks(ranklists):
# 	emptyRankList = 0
# 	nonEmptyRankList = -1
# 	for ranklist in ranklists:
# 		if len(ranklist) == 0:
# 			emptyRankList += 1
# 	if emptyRankList >= 1:
# 		for ranklist in ranklists:
# 			if len(ranklist) > 0:
# 				sorted_ranklist = ranklist
# 				return sorted_ranklist[:10],1.0
# 		return None,None

# 	ranker_names = [str(i) for i in xrange(0,len(ranklists))]
# 	objects = {}
# 	oid = 0
# 	oid_name = {}
# 	occur = {}
# 	num = len(ranklists)
# 	for i in xrange(0,num):
# 		sorted_ranklist = ranklists[i]
# 		for k in xrange(0,len(sorted_ranklist)):
# 			key = sorted_ranklist[k][0]
# 			val = float(sorted_ranklist[k][1])
# 			if key not in occur.keys():
# 				occur[key] = oid
# 				oid_name[oid] = key
# 				objects[oid] = [None for j in xrange(0,num)]
# 				oid += 1
# 			objects[occur[key]][i] = k
	
# 	# print objects
# 	# print oid_name
# 	alpha = 0.85
# 	ranker, score = r.pagerank_aggregator(objects, 0.000001, alpha)
# 	final_ranklist = sorted(ranker.items(), key=lambda x:x[1])
# 	final_ranklist = final_ranklist[:10]
# 	final_keys = []
# 	for i in xrange(0,len(final_ranklist)):
# 		final_keys.append(oid_name[final_ranklist[i][0]])
# 	return final_keys,score

# if __name__ == '__main__':
# 	ranklists = pickle.load( open(sys.argv[1], 'rb'))
# 	ranker, score = get_combined_ranks(ranklists) 
# 	print score
# 	pickle.dump(ranker, open(sys.argv[2], 'wb'))
# 	print 'Done'
