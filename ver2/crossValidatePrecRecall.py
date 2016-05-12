import sys
import pickle
from calcPrecisionRecall import calcPrecision_2,calcRecall_2

if __name__ == '__main__':

	prefix = sys.argv[1]
	end = int(sys.argv[2])

	cumPre_cv = [0.0, 0.0, 0.0]
	cumRec_cv = [0.0, 0.0, 0.0]
		
	for i in xrange(0,end):
		cumPre = [0.0, 0.0, 0.0]
		cumRec = [0.0, 0.0, 0.0]
		qcount = 0.0
		filename = prefix+'TestPosts_50K_EnTagRec_PosTagged_WVTool_'+str(i)+'_SeedTagsByStringAndWVTool_0_6_0_2.txt'
		print filename
		with open(filename, 'r') as f:
			for line in f:
				qcount += 1.0
				post = eval(line.strip('\n'))
				expectedTags = post['expected']
				# predictedTags = [item[0] for item in post['predicted_by_String_Matching']]
				# predictedTags = [item[0] for item in post['predicted_By_FIC']]
				# predictedTags = [item[0] for item in post['predicted_by_Doc2Vec_Matching']]
				# predictedTags = [item[0] for item in post['predicted_by_StringAndFIC_Matching']]
				# predictedTags = [item[0] for item in post['predicted_by_StringAndWVTool_Matching']]
				# predictedTags = [item[0] for item in post['final_Recommended_Tags']]
				# predictedTags = [item[0] for item in post['spread_final_Recommended_Tags']]
				
				#for baseline checking
				# predictedTags = [item[0] for item in post['predicted']]
				# predictedTags = [item[0] for item in post['predicted_By_EnTagRec']]
				if qcount%1000 == 0:
					print qcount
					sys.stdout.flush()				
				if len(predictedTags) <= 0:
					continue
				post['precision'] = calcPrecision_2(expectedTags, predictedTags)
				post['recall'] = calcRecall_2(expectedTags, predictedTags)

				cumPre[0] += post['precision'][0]
				cumPre[1] += post['precision'][1]
				cumPre[2] += post['precision'][2]
				cumRec[0] += post['recall'][0]
				cumRec[1] += post['recall'][1]
				cumRec[2] += post['recall'][2]

			# wfile.write(str(post) + '\n')
			# wfile.flush()

	# wfile.close()
		print 'Num Docs', qcount
		print 'Precision: ',
		print cumPre[0]/qcount,
		print cumPre[1]/qcount,
		print cumPre[2]/qcount
		print 'Recall: ',
		print cumRec[0]/qcount,
		print cumRec[1]/qcount,
		print cumRec[2]/qcount
		cumPre_cv[0] += cumPre[0]/qcount
		cumPre_cv[1] += cumPre[1]/qcount
		cumPre_cv[2] += cumPre[2]/qcount
		cumRec_cv[0] += cumRec[0]/qcount
		cumRec_cv[1] += cumRec[1]/qcount
		cumRec_cv[2] += cumRec[2]/qcount

	print 'Precisioncv: ',
	print cumPre_cv[0]/end,
	print cumPre_cv[1]/end,
	print cumPre_cv[2]/end
	print 'Recall: ',
	print cumRec_cv[0]/end,
	print cumRec_cv[1]/end,
	print cumRec_cv[2]/end



# Final Metapath based ranking: ( alphas = [0.8, 0.1, 0.1] )
# Precision:  0.338928970917 0.252176174497 0.151531040268
# Recall:  0.485513842282 0.593263422819 0.710253215884









	# f = open(sys.argv[1], 'r')
	# outs = []
	# for line in f:
	# 	outs.append(eval(line.strip('\n')))
	# f.close()

	# for i in xrange(0,len(outs)):
	# 	expected = outs[i]['expected']
	# 	predicted = outs[i]['combined_meta_tanks']
	# 	outs[i]['precision_by_combined_meta'] = {}
	# 	outs[i]['recall_by_combined_meta'] = {}
	# 	if len(predicted) > 0:
	# 		for k in [3,5,min(10,len(predicted))]:
	# 			tp = 0.0
	# 			fp = 0.0
	# 			for tag_p in predicted[:k]:
	# 				tag = tag_p[0]
	# 				cnt = 0
	# 				for tag2 in expected:
	# 					jac    = 1 - distance.jaccard(tag, tag2)
	# 					if jac > 0.6 or tag in tag2 or tag2 in tag:
	# 						tp += 1
	# 						cnt = 1
	# 						break
	# 				if cnt == 0:
	# 					fp += 1
	# 			# print tp,fp,len(expected),len(predicted),k
	# 			prec = tp/(tp+fp)
	# 			rec = tp/len(expected)
	# 			if rec > 1.0:
	# 				rec = 1.0
	# 			outs[i]['precision_by_combined_meta'][k] = prec
	# 			outs[i]['recall_by_combined_meta'][k] = rec
	# 	print outs[i]


# Some good news. (to some extent)
# Precision: (@3 : 0.301) (@5 : 0.24) (@10 : 0.176) 
# Recall:  (@3 : 0.304) (@5 : 0.403666666667) (@10 : 0.553666666667)

# Better than other methods but not much.
