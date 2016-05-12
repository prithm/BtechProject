import sys

if __name__ == '__main__':
	wfile = open(sys.argv[2],'w')
	alpha = [0.0,0.0,0.0]
	alpha[0] = float(sys.argv[3])
	alpha[1] = float(sys.argv[4])
	alpha[2] = float(sys.argv[5])

	with open(sys.argv[1], 'r') as f:
		for line in f:
			post = eval(line.strip('\n'))
			metapathnum = 0
			overall = {}
			for ranklist in post['predicted_by_Metapaths_Combined_Ranks']:
				rank_num = 0
				for tag,prob in ranklist:
					rank_num += 1
					if tag not in overall.keys():
						overall[tag] = 0.0
					overall[tag] += alpha[metapathnum]*(prob)
					#if rank_num >= 10:
					#	break
				metapathnum += 1		
			sorted_x = sorted(overall.items(), key=lambda x:x[1], reverse= True)
			sorted_x = sorted_x[:20]
			sum_ = 0.0
			for item in sorted_x:
				sum_ += item[1]
			matchedTags = []
			for item in sorted_x:
				matchedTags.append((item[0],item[1]/sum_))
			post['final_Recommended_Tags'] = matchedTags
			wfile.write(str(post)+'\n')
			wfile.flush()

	wfile.close()











# import sys
# import pickle
# import difflib
# from bs4 import BeautifulSoup
# import re
# import distance
# from nltk.corpus import stopwords
# stop = stopwords.words('english')
# import operator
# from gensim.models import doc2vec
# import scipy.spatial.distance as ds


# if __name__ == '__main__':
	
# 	alpha = 0.2

# 	survey_q_seeds = []
# 	with open(sys.argv[1],'r') as f:
# 		for line in f:
# 			survey_q_seeds.append(eval(line.strip('\n')))
	
# 	survey_q_m = []
# 	with open(sys.argv[2],'r') as f:
# 		for line in f:
# 			survey_q_m.append(eval(line.strip('\n')))

# 	# print len(survey_q_seeds)
# 	# print survey_q_seeds[0].keys()
# 	# print len(survey_q_m)
# 	# print survey_q_m[0].keys()

# 	for i in xrange(0,len(survey_q_seeds)):

# 		tag_set = set()
# 		seed_set = {}
# 		probs = {}
		
# 		for tag_p in survey_q_seeds[i]['probs']:
# 			tag_set.add(tag_p[0])
# 			seed_set[tag_p[0]] = tag_p[1]
# 			probs[tag_p[0]] = {}

# 		meta = survey_q_m[i]['predicted_by_Metapaths']
# 		for seed in seed_set.keys():
# 			if seed in meta.keys() and len(meta[seed]) > 0:
# 				ranklists = meta[seed][0]
# 				for ranklist in ranklists:
# 					summ = 0.0
# 					for newtag,p in ranklist:
# 						tag_set.add(newtag)
# 						summ += p
# 					for newtag,p in ranklist:
# 						if newtag not in probs[seed].keys():
# 							probs[seed][newtag] = 0.0
# 						probs[seed][newtag] += p/summ	

# 		for key1 in probs.keys():
# 			for key2 in probs[key1].keys():
# 				probs[key1][key2] = probs[key1][key2]

# 		tag_list = list(tag_set)

# 		final_prob = {}

# 		for tag in tag_list:
# 			tot  = 0.0
# 			for seed in seed_set.keys():
# 				if tag not in probs[seed].keys():
# 					tot += (1 - alpha)*seed_set[seed]
# 				else:
# 					tot += alpha*probs[seed][tag] + (1 - alpha)*seed_set[seed]

# 			final_prob[tag] = tot	

# 		final_sorted_x = sorted(final_prob.items(), key=operator.itemgetter(1), reverse = True)
# 		survey_q_seeds[i]['combined_meta_tanks'] = final_sorted_x[:15]
# 		print survey_q_seeds[i]









