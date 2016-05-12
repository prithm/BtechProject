# import networkx as nx
import sys
import pickle
import operator
import time


# G = nx.DiGraph()
tags = set()
# zeroDict = {}
print "Initialising"
tagTagProb = pickle.load(open(sys.argv[1], 'rb'))
print 'Initialised'
sys.stdout.flush()

#tagTagProb = {}
tagKeys = set()
ecnt = 0
for tag1,valueDict in tagTagProb.items():
	tags.add(tag1)
	tagKeys.add(tag1)
	#sorted_x = sorted(valueDict.items(), key=operator.itemgetter(1), reverse=True)
	#summ = 0.0
	#sorted_x = sorted_x[0:20]
	#for item in sorted_x:
	#	summ = summ + item[1]
	#tagTagProb[tag1] = {}
	#for item in sorted_x:
	#	ecnt += 1
	#	tagTagProb[tag1][item[0]] = item[1]/summ
	#	tags.add(item[0])
	for tag2,wt in valueDict.items():
		tags.add(tag2)
		ecnt += 1

print ecnt
sys.stdout.flush()

#for tag1,valueDict in tagTagProb.items():
# 	for tag2,wt in valueDict.items():
# 		tags.add(tag1)
# 		tags.add(tag2)
# 		G.add_edge(tag1, tag2, weight=float(wt))
# 		zeroDict[tag1] = 0.0
# 		zeroDict[tag2] = 0.0
# print 'Graph made'

tagList = list(tags)		

# def genRWR(id_,start,end):
# 	print start,end,len(tags)
		
# 	f = open('out_answer_'+str(id_)+'.txt', 'w')
# 	cnt = 0
# 	for i in xrange(start,end):
# 		tag = tagList[i]
# 		print tag
# 		cnt += 1
# 		if cnt%100 == 0:
# 			print cnt
# 		tempDict = zeroDict
# 	 	tempDict[tag] = 1.0
# 	 	out = {}
# 	 	out[tag] = nx.pagerank(G, personalization = tempDict, max_iter=100)
# 	 	f.write(str(out)+'\n')
# 	 	f.flush()
# 	 	tempDict[tag] = 0.0
# 		#if cnt >= 1:
# 		#	break
# 	f.close()
# 	f = open('done_answer_'+str(id_)+'.txt', 'w')
# 	f.write('done'+'\n')
# 	f.close()	

def myRWR(restart_tags, alpha):
	num_tags = len(tagList)
	num_restart_tags = len(restart_tags)
	pi_prev = {}
	pi_cur = {}

	for tag in tagList:
		pi_prev[tag] = 1.0/num_tags
	
	for i in xrange(0,20):
		#print 'Convergence iter:',i
		#sys.stdout.flush()
		#ccnt = 0	
		for tag1,prev_score in pi_prev.items():
			if tag1 not in tagKeys:
				continue
			valueDict = tagTagProb[tag1]
			for tag2,wt in valueDict.items():
				#ccnt += 1
				#if ccnt%10000 == 0:
				#	print 'ccnt',ccnt
				#	sys.stdout.flush()
				if tag2 not in pi_cur.keys():
					pi_cur[tag2] = 0.0
				pi_cur[tag2] += wt*prev_score
		 
		pi_prev = {}
		for tag,score in pi_cur.items():
			pi_prev[tag] = (1-alpha)*score
			
		for tag in restart_tags:
			if tag not in pi_prev.keys():
				pi_prev[tag] = 0.0
			pi_prev[tag] += alpha*(1.0/num_restart_tags)

		pi_cur = {}
	

	# for i in xrange(0,1):
	# 	#print 'Convergence iter:',i
	# 	#sys.stdout.flush()
	# 	#ccnt = 0	
	# 	for tag1,valueDict in tagTagProb.items():
	# 		for tag2,wt in valueDict.items():
	# 			#ccnt += 1
	# 			#if ccnt%10000 == 0:
	# 			#	print 'ccnt',ccnt
	# 			#	sys.stdout.flush()
	# 			if tag2 not in pi_cur.keys():
	# 				pi_cur[tag2] = 0.0
	# 			if tag1 in pi_prev.keys():
	# 				pi_cur[tag2] += wt*pi_prev[tag1]
		 
	# 	pi_prev = {}
	# 	for tag,score in pi_cur.items():
	# 		pi_prev[tag] = (1-alpha)*score
			
	# 	for tag in restart_tags:
	# 		if 	tag not in pi_prev.keys():
	# 			pi_prev[tag] = 0.0
	# 		pi_prev[tag] += alpha*(1.0/num_restart_tags)

	# 	pi_cur = {}

	
	return pi_prev


def genRWR(id_,start,end):
	alpha = 0.2
	print id_,start,end		
	f = open('out_sameOwner_'+ str(id_) +'.txt', 'w')
	cnt = 0
	for tag_i in xrange(start,end):
		tag = tagList[tag_i]
		start_time = time.time()
		print tag
		sys.stdout.flush()
		cnt += 1
		if cnt%100 == 0:
			print cnt
			sys.stdout.flush()
		out = {}
		# out[tag] = nx.pagerank(G, personalization = tempDict, max_iter=100)
		out[tag] = myRWR([tag],alpha)
		print 'will print now'
		sys.stdout.flush()
		f.write(str(out)+'\n')
		f.flush()
		print("--- %s seconds ---" % (time.time() - start_time))
		print 'going to next tag'
		sys.stdout.flush()
		#if cnt >= 2:
		#	break
	f.close()
	f = open('done_sameOwner_'+str(id_)+'.txt', 'w')
	f.write('done'+'\n')
	f.close()	


if __name__ == '__main__':
	genRWR(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]))
	
