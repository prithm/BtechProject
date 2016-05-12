import sys
import pickle
import distance


def calcPrecision(expected,predicted):
	expectedSet = set(expected)
	precision = []	
	for i in [3,5,10]:
		predicted_truncate = predicted[:i]
		num = 0.0
		den = i*1.0
		for item in predicted_truncate:
			if item in expectedSet:
				num += 1.0
		precision.append(num/den)
	return precision

def calcPrecision_2(expected,predicted):
	expectedSet = set(expected)
	precision = []	
	for i in [3,5,10]:
		predicted_truncate = predicted[:i]
		num = 0.0
		den = i*1.0
		for item in predicted_truncate:
			if item in expectedSet:
				num += 1.0
			else:
				for item2 in expectedSet:
					jac    = 1 - distance.jaccard(item, item2)
					#if jac > 0.8 or item in item2 or item2 in item:
					if jac > 1.6:
						num += 1.0
						break
		precision.append(num/den)
	return precision

def calcRecall(expected,predicted):
	den = 1.0*len(expected)
	recall = []
	for i in [3,5,10]:
		predicted_truncate = predicted[:i]
		predictedSet = set(predicted_truncate)
		num = 0.0
		for item in expected:
			if item in predictedSet:
				num += 1.0
		recall.append(num/den)
	return recall


def calcRecall_2(expected,predicted):
	den = 1.0*len(expected)
	recall = []
	for i in [3,5,10]:
		predicted_truncate = predicted[:i]
		predictedSet = set(predicted_truncate)
		num = 0.0
		for item in expected:
			if item in predictedSet:
				num += 1.0
			else:
				for item2 in predictedSet:
					jac    = 1 - distance.jaccard(item, item2)
					#if jac > 0.8 or item in item2 or item2 in item:
					if jac > 1.6:
						num += 1.0
						break				
		recall.append(num/den)
	return recall

if __name__ == '__main__':

	cumPre = [0.0, 0.0, 0.0]
	cumRec = [0.0, 0.0, 0.0]
	part = int(sys.argv[2])
	cnt = 0.0
	num = 47691
	start = int(0.1*(part)*num)
	end = int(0.1*(part+1)*num)
	cnt = -1
	qcount = 0.0
	wfile = open(sys.argv[3],'w')
	with open(sys.argv[1], 'r') as f:
		for line in f:
			cnt += 1.0
			# if cnt%500 == 0:
			# 	print cnt
			# 	sys.stdout.flush()
			
			if part>=0 and (cnt < start or cnt >= end):
				if cnt%500 == 0:
					print cnt
					sys.stdout.flush()
				continue

			if cnt%500 == 0:
				print cnt, 'Test'
				sys.stdout.flush()
			
			qcount += 1.0
			post = eval(line.strip('\n'))
			expectedTags = post['expected']
			#predictedTags = [item[0] for item in post['predicted_by_String_Matching']]
			#predictedTags = [item[0] for item in post['predicted_by_Doc2Vec_Matching']]
			#predictedTags = [item[0] for item in post['predicted_By_FIC']]
			#predictedTags = [item[0] for item in post['predicted_by_StringAndFIC_Matching']]
			predictedTags = [item[0] for item in post['final_Recommended_Tags']]
			# predictedTags = [item[0] for item in post['predicted_by_Hybrid_Matching']]
			
			# predictedTags = [item[0] for item in post['predicted_by_SimRank']]
			#predictedTags = [item[0] for item in post['predicted_by_TermTag']]
			#for baseline checking
			# predictedTags = [item[0] for item in post['predicted']]
			# predictedTags = [item[0] for item in post['predicted_By_EnTagRec']]
			
			
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

			out = ''
			out += str(post['precision'][0]) + ','
			out += str(post['precision'][1]) + ','
			out += str(post['precision'][2]) + ','
			out += str(post['recall'][0]) + ','
			out += str(post['recall'][1]) + ','
			out += str(post['recall'][2])
			
			wfile.write(str(out) + '\n')
			wfile.flush()

	wfile.close()
	print 'Num Docs', qcount
	print 'Precision: ',
	print cumPre[0]/qcount,
	print cumPre[1]/qcount,
	print cumPre[2]/qcount
	print 'Recall: ',
	print cumRec[0]/qcount,
	print cumRec[1]/qcount,
	print cumRec[2]/qcount













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
