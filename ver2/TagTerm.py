import sys
import re
import pickle
import math	

if __name__ == '__main__':
	
	overall = pickle.load(open(sys.argv[1], 'rb'))
	n_term_tag = pickle.load(open(sys.argv[2], 'rb'))
	test_posts = pickle.load(open(sys.argv[3], 'rb'))
	#wordset = set()
	#with open(sys.argv[4],'r') as f:
	#	for line in f:
	#		wordset.add(line.strip('\n'))

	print len(test_posts)
	sys.stdout.flush()

	wfile = open(sys.argv[4], 'w')
	
	cnt = 0	
	for test_post in test_posts:
		cnt += 1
		if cnt%100 == 0:
			print cnt
			sys.stdout.flush()

		terms = overall[test_post['Id']]['terms'].split()
		#print terms
			
		rec_tags = {}
		for term in terms:
			if term in n_term_tag.keys():
				#print 'Term', term, 'Entered',
				sys.stdout.flush()
				for tag in n_term_tag[term].keys():
					#print '(',tag,n_term_tag[term][tag],')',
					sys.stdout.flush()
					if tag not in rec_tags.keys():
						rec_tags[tag] = (1.0 - n_term_tag[term][tag])
					else:
						rec_tags[tag] *= (1.0 - n_term_tag[term][tag])
				#print 

		for rec_tag in rec_tags.keys():
			rec_tags[rec_tag] = 1.0 - rec_tags[rec_tag]
		rec_tags_sorted = sorted(rec_tags.items(), key=lambda x:x[1], reverse= True)
		rec_tags_sorted = rec_tags_sorted[:50]
		
		matchedTags = []
		sum_ = 0.0
		for item in rec_tags_sorted:
			sum_ += item[1]

		for item in rec_tags_sorted:
			matchedTags.append((item[0],item[1]/sum_))


		temp = {}
		temp['expected'] = test_post['Tags'].strip('<').strip('>').split('><')
		temp['Id'] = test_post['Id']
		temp['index'] = cnt
		temp['predicted_by_TermTag'] = matchedTags
		wfile.write(str(temp)+'\n') 
		wfile.flush()
		# print orig_tags, rec_tags_sorted_truncate
		#break

	wfile.close()
	# pickle.dump(predicted_tags, open(sys.argv[3], 'wb'))



