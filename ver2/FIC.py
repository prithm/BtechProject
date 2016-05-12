import sys
import pickle
import nltk

if __name__ == '__main__':
	everything = pickle.load( open(sys.argv[1], 'rb') )
	num = len(everything)
	part_ = int(sys.argv[2])	
	#part is the part being left out part = 1, means 2 to 10 are taken
	for part in xrange(part_,part_+1):
		print part
		sys.stdout.flush()
		P_word_tag = {}
		P_tag_tag = {}
		P_tag = {}
		test_posts = []
		start = int(0.1*(part)*num)
		end = int(0.1*(part+1)*num)
		cnt = 0
		qcount = 0
		for i in xrange(0,num):

			cnt += 1
			#if cnt == 3:
			#	break
			if cnt % 500 == 0:
				print cnt
				sys.stdout.flush()

			if i >= start and i < end:
				test_posts.append(everything[i])
				continue
			
			qcount += 1
			tags = everything[i]['tags']
			words  =  everything[i]['body'].strip().split()
			# pos_tags = nltk.pos_tag(words)
			#print tags

			for word in words:
			# for word,pos_tag in pos_tags:
				# if not pos_tag.startswith('NN'):
				# 	continue
				if word not in P_word_tag.keys():
					P_word_tag[word] = {}
				for tag in tags:
					P_word_tag[word][tag] = 1.0
			
			for tag in tags:		
				if tag not in P_tag.keys():
					P_tag[tag] = 0.0
				P_tag[tag] += 1.0

			if len(tags) > 0:
				for j in xrange(0,len(tags)):
					if tags[j] not in P_tag_tag.keys():
						P_tag_tag[tags[j]] = {}				
					for k in xrange(0,len(tags)):
						if j == k:
							continue
						if tags[k] not in P_tag_tag[tags[j]].keys():
							P_tag_tag[tags[j]][tags[k]] = 0.0	
						P_tag_tag[tags[j]][tags[k]] += 1.0
			#print P_tag
			#print P_tag_tag
			#print P_word_tag
			#print 
		for tag_1 in P_tag_tag.keys():
			for tag_2 in P_tag_tag[tag_1].keys():
				P_tag_tag[tag_1][tag_2] /= (P_tag[tag_1]+P_tag[tag_2]-P_tag_tag[tag_1][tag_2])

		# print P_tag_tag
		print qcount
		pickle.dump(P_word_tag, open('P_word_tag_50K_EnTagRec_wvtools_'+str(part)+'_.pickle','wb'))
		pickle.dump(P_tag_tag,  open('P_tag_tag_50K_EnTagRec_wvtools_'+str(part)+'_.pickle','wb'))
		pickle.dump(test_posts, open('TestPosts_50K_EnTagRec_wvtools_'+str(part)+'_.pickle','wb'))
