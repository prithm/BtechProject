import sys
import pickle
from combineRanks import get_combined_ranks

if __name__ == '__main__':
	survey = []
	with open(sys.argv[1],'r') as f:
		for line in f:
			survey.append(eval(line.strip('\n')))
			
	num_dicts = int(sys.argv[2])
	meta_dicts = []
	for i in xrange(3,3+num_dicts):
		temp = pickle.load( open(sys.argv[i],'rb') )
		meta_dicts.append(temp)
	#print 'Init done'
	#sys.stdout.flush()
	cnt = 0
	for s in survey:
		# print s
		expected = s['expected']
		try:
			# seeds = [it[0] for it in s['predicted_by_StringAndFIC_Matching']]
			seeds = [it[0] for it in s['predicted_by_StringAndWVTool_Matching']]
		except Exception as e:
			seeds = [it[0] for it in s['predicted_by_Hybrid_Matching']]
		s['predicted_by_Metapaths'] =  {}
		temp = []
		for seed in seeds:
			ranklists = []
			cnt += 1
			#if cnt%100:
			#	print cnt
			#	sys.stdout.flush()
			s['predicted_by_Metapaths'][seed] = []
			for meta_dict in meta_dicts:
				if seed in meta_dict.keys():
					sorted_x = sorted(meta_dict[seed].items(), key=lambda x:x[1], reverse = True)	
					sorted_x = sorted_x[:10]
					ranklists.append(sorted_x)
			#comb_ranklists,score = get_combined_ranks(ranklists)
			# s['predicted_by_Metapaths'][seed].append(ranklists)
			s['predicted_by_Metapaths'][seed] = ranklists
		
		print s
		sys.stdout.flush()
