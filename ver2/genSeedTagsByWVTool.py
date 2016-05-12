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
	num = num/(math.sqrt(den1)*math.sqrt(den2))
	return num
	

if __name__ == '__main__':
	
	everything = pickle.load(open(sys.argv[1], 'rb'))
	
	num = len(everything)
	part = int(sys.argv[2])
	wfile = open(sys.argv[3],'w')
	start = int(0.1*(part)*num)
	end = int(0.1*(part+1)*num)

	test_posts = []
	try:
		test_posts = pickle.load(open(sys.argv[4], 'rb'))
	except Exception as e:
		cnt = 0
		for i in xrange(0,num):
			if i >= start and i < end:
				test_posts.append(everything[i])
		pickle.dump(test_posts, open(sys.argv[4],'wb'))					
	
	print len(test_posts)
	sys.stdout.flush()
	cnt = 0	
	for test_post in test_posts:
		cnt += 1
		if cnt%50 == 0:
			print cnt
			sys.stdout.flush()

		sim_dict = {}
		for i in xrange(0,num):
			if i >= start and i < end:
				continue
			sim_dict[i] = find_cosine_sim(everything[i]['wv'],test_post['wv'])

		rec_tags = {}
		sum_ = 0.0	
		sims = sorted(sim_dict.items(), key=lambda x:x[1], reverse= True)
		sims = sims[:50]
		for index,val in sims:
			tags = everything[index]['tags']
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
		temp['expected'] = test_post['tags']
		temp['Id'] = test_post['Id']
		temp['index'] = cnt
		temp['predicted_by_Doc2Vec_Matching'] = matchedTags
		wfile.write(str(temp)+'\n') 
		wfile.flush()
		# print orig_tags, rec_tags_sorted_truncate
		# break

	wfile.close()
	# pickle.dump(predicted_tags, open(sys.argv[3], 'wb'))



