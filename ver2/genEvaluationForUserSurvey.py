import sys
import pickle
import distance

def calcPrecision_3(expected,predicted):
	expectedSet = set(expected)
	precision = []	
	for i in [min(5,len(predicted))]:
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
					if jac > 0.8:
						num += 1.0
						break
		precision.append(num/den)
	return precision

def calcRecall_3(expected,predicted):
	den = 1.0*len(expected)
	recall = []
	for i in [min(5,len(predicted))]:
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
					if jac > 0.8:
						num += 1.0
						break				
		recall.append(num/den)
	return recall


if __name__ == '__main__':
	testPosts = pickle.load(open(sys.argv[1],'rb'))

	out = 'ViewCount,pre_expected,rec_expected,'
	out += 'pre_seed,rec_seed,'
	out += 'pre_metapaths,rec_metapaths'
	print out

	prefix = sys.argv[2]
	for id_ in xrange(1,9):
		cnt = -1

		cumPre = {}
		cumPre['expected'] = []
		cumPre['predicted_by_Hybrid_Matching'] = []
		cumPre['final_Recommended_Tags'] = []
		cumRec = {}
		cumRec['expected'] = []
		cumRec['predicted_by_Hybrid_Matching'] = []
		cumRec['final_Recommended_Tags'] = []
		preCount = []
		recCount = []

		for key in cumPre.keys():
			for i in xrange(0,10):
				cumPre[key].append([0.0])
				cumRec[key].append([0.0])
		
		for i in xrange(0,10):
			preCount.append(0.0)
			recCount.append(0.0)


		with open(prefix+str(id_)+'.tsv') as f:
			# print id_
			for line in f:
				cnt += 1
				if cnt <= 0:
					continue
				# print line
				lineParts = line.strip('\n').split('\t')[1:]
				lineParts_ = [linePart.strip().split(',') for linePart in lineParts]
				groundTruths = []
				for linePart in lineParts_:
					for i in xrange(0,len(linePart)):
						linePart[i] = linePart[i].strip()
					groundTruths.append(linePart)

				
				for i in xrange(10*(id_-1),10*id_):
					post = testPosts[i]
					# print post['ViewCount']
					if len(groundTruths[i%10]) > 0:
						preCount[i%10] += 1.0
						recCount[i%10] += 1.0
					for key in cumPre.keys():
						prec = calcPrecision_3(groundTruths[i%10], post[key])
						rec = calcRecall_3(groundTruths[i%10], post[key])
						for j in xrange(0,len(cumPre[key][i%10])): 
							cumPre[key][i%10][j] += prec[j]
							cumRec[key][i%10][j] += rec[j]
			
		for key in cumPre.keys():			
			for i in xrange(0,10):
				for j in xrange(0,len(cumPre[key][i])):
					cumPre[key][i][j] /= preCount[i]
					cumRec[key][i][j] /= preCount[i]

		for i in xrange(10*(id_-1),10*id_):
			out = testPosts[i]['ViewCount'] + ','
			for j in xrange(0 , len(cumPre['expected'][i%10])):
				out += str(cumPre['expected'][i%10][j]) + ','
			for j in xrange(0 , len(cumRec['expected'][i%10])):
				out += str(cumRec['expected'][i%10][j]) + ','

			for j in xrange(0 , len(cumPre['predicted_by_Hybrid_Matching'][i%10])):
				out += str(cumPre['predicted_by_Hybrid_Matching'][i%10][j]) + ','
			for j in xrange(0 , len(cumRec['predicted_by_Hybrid_Matching'][i%10])):
				out += str(cumRec['predicted_by_Hybrid_Matching'][i%10][j]) + ','
			
			for j in xrange(0 , len(cumPre['final_Recommended_Tags'][i%10])):
				out += str(cumPre['final_Recommended_Tags'][i%10][j]) + ','
			for j in xrange(0 , len(cumRec['final_Recommended_Tags'][i%10])):
				out += str(cumRec['final_Recommended_Tags'][i%10][j]) + ','	
			
			print out		
		# break

	# cnt = 0

	# for post in testPosts[:10]:
	# 	# print post.keys()
	# 	body =  BeautifulSoup(post['Body']).get_text()
	# 	body = re.sub(r'\n','. ',body)
	# 	# body = re.sub(r"\\\\'","'",body)
	# 	# body = re.sub(r'"','\"',body)
	# 	# body = re.sub(r'\\"','\"',body)
	# 	post['Body'] = body
	# 	post['expected'] = post['expected'][:5]
	# 	post['predicted_by_Hybrid_Matching'] = post['predicted_by_Hybrid_Matching'][:5]
	# 	post['final_Recommended_Tags'] = post['final_Recommended_Tags'][:5]
	# 	tot = set()
	# 	for tag in post['expected']:
	# 		tot.add(tag.strip())
	# 	for tag in post['predicted_by_Hybrid_Matching']:
	# 		tot.add(tag.strip())
	# 	for tag in post['final_Recommended_Tags']:
	# 		tot.add(tag.strip())
	# 	tempDict = {}
	# 	tempDict['Body'] = body
	# 	tempDict['Total'] = list(tot)	
	# 	cnt += 1
	# 	wfile.write(str(tempDict)+'\n')
	# 	wfile.flush()

	# wfile.close()
