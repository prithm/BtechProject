# import sys
# import pickle
# from bs4 import BeautifulSoup
# import re

# if __name__ == '__main__':
# 	testPosts = pickle.load(open(sys.argv[1],'rb'))
# 	wfile = open(sys.argv[2], 'w')
# 	cnt = 0

# 	for post in testPosts[:10]:
# 		# print post.keys()
# 		body =  BeautifulSoup(post['Body']).get_text()
# 		body = re.sub(r'\n','. ',body)
# 		# body = re.sub(r"\\\\'","'",body)
# 		# body = re.sub(r'"','\"',body)
# 		# body = re.sub(r'\\"','\"',body)
# 		post['Body'] = body
# 		post['expected'] = post['expected'][:5]
# 		post['predicted_by_Hybrid_Matching'] = post['predicted_by_Hybrid_Matching'][:5]
# 		post['final_Recommended_Tags'] = post['final_Recommended_Tags'][:5]
# 		tot = set()
# 		for tag in post['expected']:
# 			tot.add(tag.strip())
# 		for tag in post['predicted_by_Hybrid_Matching']:
# 			tot.add(tag.strip())
# 		for tag in post['final_Recommended_Tags']:
# 			tot.add(tag.strip())
# 		tempDict = {}
# 		tempDict['Body'] = body
# 		tempDict['Total'] = list(tot)	
# 		cnt += 1
# 		wfile.write(str(tempDict)+'\n')
# 		wfile.flush()

# 	wfile.close()


# import sys

# if __name__ == '__main__':
# 	cntline = -1
# 	heading = []
# 	cum = {}
# 	cnt = {}
# 	with open(sys.argv[1],'r') as f:
# 		for line in f:
# 			cntline += 1
# 			if cntline <= 0:
# 				print line
# 				heading = line.strip('\n').split(',')
# 				continue
# 			lineParts = line.strip('\n').split(',')
# 			if lineParts[0] not in cnt.keys():
# 				cnt[lineParts[0]] = 0.0
# 				cum[lineParts[0]] = []
# 				for i in xrange(0,len(heading)-1):
# 					cum[lineParts[0]].append(0.0)
	
# 			cnt[lineParts[0]] += 1.0
# 			for i in xrange(1,len(heading)):
# 				cum[lineParts[0]][i-1] += float(lineParts[i])


# 	for key in cum.keys():
# 		for i in xrange(0,len(cum[key])):
# 			cum[key][i] /= cnt[key]
		
# 		print key,cum[key]
	
import sys
import pickle
		
# if __name__ == '__main__':
# 	a = pickle.load( open(sys.argv[1],'rb') )
# 	word_count = {}
# 	for post in a:
# 		words = post['body'].strip().split()
# 		for word in words:
# 			if word not in word_count.keys():
# 				word_count[word] = 0
# 			word_count[word] += 1
# 	cnt = 0
# 	for post in a:
# 		words = post['body'].strip().split()
# 		for word in words:
# 			if word_count[word] >= 20:
# 				cnt += 1
# 				break

# 	print cnt

if __name__ == '__main__':

	# cnt = 0
	# word_count = {}
	# a = []
	# with open(sys.argv[1], 'r') as f:
	# 	for line in f:
	# 		cnt += 1
	# 		if cnt%3 == 0:
	# 			words = line.strip('\n').strip().split()
	# 			k = []
	# 			for word in words:
	# 				if word == 'c' or len(word) > 1: 
	# 					if word not in word_count.keys():
	# 						word_count[word] = 0
	# 					word_count[word] += 1
	# 					k.append(word)
	# 			a.append(k)
			
	# 			if int(cnt/3)%1000 == 0:
	# 				print int(cnt/3)
	# 				sys.stdout.flush()

	# print len(word_count.keys())
	# wfile = open(sys.argv[2], 'w')
	# for ai in a:
	# 	out = ''
	# 	for word in ai:
	# 		if word_count[word] >= 20:
	# 			out += ' ' + word
	# 	wfile.write(out.encode('utf-8')+'\n')
	# 	wfile.flush()
	# wfile.close()


	# a = pickle.load( open('TrainingSetForEnTagRecUnfiltered.pickle','rb') )
	# print len(a)
	# cnt = 0
	# for post in a:
	# 	cnt += 1
	# 	if cnt%500 == 0:
	# 		print cnt
	# 		sys.stdout.flush()

	# 	wfile = open(sys.argv[1]+'/'+post['Id'],'w')
	# 	wfile.write(post['body'].encode('utf-8')+'\n')
	# 	wfile.flush()
	# 	wfile.close()

	# wordlist = {}
	# cnt = -1
	# with open('wordlist.txt') as f:
	# 	for line in f:
	# 		cnt += 1
	# 		wordlist[cnt] = line.strip('\n').strip().strip('\n')
	# post_bodies = {}
	# with open('wv.txt') as f:
	# 	for line in f:
	# 		lineParts = line.strip('\n').strip().strip('\n').split(';')
	# 		out = ''
	# 		words = lineParts[1].strip().split()
	# 		for word in words:
	# 			out += ' ' + wordlist[int(word.split(':')[0])]
	# 		# print out
	# 		out = out.strip()
	# 		if len(out) > 0:
	# 			post_bodies[int(lineParts[0])] = out
	# 		# break
	# a = pickle.load( open('TrainingSetForEnTagRecUnfiltered.pickle','rb') )
	# newone = []
	# for ai in a:
	# 	if int(ai['Id']) in post_bodies.keys():
	# 		ai['body_wv'] = post_bodies[int(ai['Id'])]
	# 		newone.append(ai)
	# print len(newone)
	# pickle.dump(newone,open(sys.argv[1],'wb')) 

	# tags = {}
	# a = pickle.load( open('TrainingSetForEnTagRecWVTools2.pickle','rb') )
	# for ai in a:
	# 	for tag in ai['tags']:
	# 		if tag not in tags.keys():
	# 			tags[tag] = 1
	# 		else:
	# 			tags[tag] += 1

	# cnt = 0
	# for tag,val in tags.items():
	# 	if val >= 50:
	# 		cnt += 1

	# print cnt

	wordlist = set()
	with open('wordlist_tfidf.txt') as f:
		for line in f:
			wordlist.add(line.strip('\n').strip().strip('\n'))
	
	post_bodies = []
	id_cnt = {}
	cnt = -1
	word_vectors = []
	with open('wv_tfidf.txt') as f:
		for line in f:
			cnt += 1
			lineParts = line.strip('\n').strip().strip('\n').split(';')
			id_cnt[int(lineParts[0])] = cnt
			# out = ''
			temp = {}
			words = lineParts[1].strip().split()
			for word in words:
				index = int(word.split(':')[0])
				score = float(word.split(':')[1])
				temp[index] = score
			word_vectors.append(temp)
			# # print out
			# out = out.strip()
			# if len(out) > 0:
			# 	post_bodies[int(lineParts[0])] = out
			# break
	
	with open('tokenized_tfidf.txt','r') as f:
		for line in f:
			body = line.strip().strip('\n').strip()
			words = body.split()
			newbody = ''
			for word in words:
				if word in wordlist:
					newbody += word + ' '
			newbody = newbody.strip()
			post_bodies.append(newbody)

	print len(post_bodies)

	a = pickle.load( open('TrainingSetForEnTagRecPosTagged.pickle','rb') )
	newone = []
	for ai in a:
		postId = int(ai['Id'])
		if postId not in id_cnt.keys():
			continue
		if len(post_bodies[id_cnt[postId]]) > 0:
			ai['body_wv'] = post_bodies[id_cnt[postId]]
			ai['wv'] = word_vectors[id_cnt[postId]]
			newone.append(ai)
	print len(newone)
	pickle.dump(newone,open(sys.argv[1],'wb')) 

	


