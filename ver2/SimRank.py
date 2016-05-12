import sys
import re
import pickle
import math

def find_cosine_sim(a,b):
	num = 0
	for key,val in a.items():
		if key in b.keys():
			num += val*b[key]
	den1 = 0.0
	den2 = 0.0
	for key,val in a.items():
		den1 += val*val
	for key,val in b.items():
		den2 += val*val
	if den1 == 0 or den2 == 0:
		return 0.0
	num = num/(math.sqrt(den1)*math.sqrt(den2))
	return num
	

if __name__ == '__main__':
	
	overall = pickle.load(open(sys.argv[1], 'rb'))
	train_posts = pickle.load(open(sys.argv[2], 'rb'))
	test_posts = pickle.load(open(sys.argv[3], 'rb'))
	num = len(train_posts)

	print len(train_posts), len(test_posts)
	sys.stdout.flush()

	wfile = open(sys.argv[4], 'w')
	
	cnt = 0	
	for test_post in test_posts:
		cnt += 1
		if cnt%100 == 0:
			print cnt
			sys.stdout.flush()

		sim_dict = {}
		for i in xrange(0,num):
			sim_dict[i] = find_cosine_sim(overall[train_posts[i]['Id']]['tfidf'],overall[test_post['Id']]['tfidf'])

		rec_tags = {}
		sum_ = 0.0	
		sims = sorted(sim_dict.items(), key=lambda x:x[1], reverse= True)
		sims = sims[:50]
		for index,val in sims:
			tags = train_posts[index]['tags'].strip('<').strip('>').split('><')
			for tag in tags:
				if tag not in rec_tags:
					rec_tags[tag] = 1.0
				else:
					rec_tags[tag] += 1.0
				sum_ += 1
				
		rec_tags_sorted = sorted(rec_tags.items(), key=lambda x:x[1], reverse= True)
		rec_tags_sorted = rec_tags_sorted[:50]
		
		matchedTags = []
		for item in rec_tags_sorted:
			matchedTags.append((item[0],item[1]/sum_))


		temp = {}
		temp['expected'] = test_post['Tags'].strip('<').strip('>').split('><')
		temp['Id'] = test_post['Id']
		temp['index'] = cnt
		temp['predicted_by_SimRank'] = matchedTags
		wfile.write(str(temp)+'\n') 
		wfile.flush()
		# print orig_tags, rec_tags_sorted_truncate

	wfile.close()
	# pickle.dump(predicted_tags, open(sys.argv[3], 'wb'))



