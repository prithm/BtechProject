import time
import sys
import pickle
import difflib
from bs4 import BeautifulSoup
import re
import distance
# from nltk.corpus import stopwords
# stop = stopwords.words('english')
import operator

print "Initialising"
taglist = pickle.load(open(sys.argv[1], 'rb'))
print 'Initialised'
sys.stdout.flush()

first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

def convert(name):
	s1 = first_cap_re.sub(r'\1_\2', name)
	return all_cap_re.sub(r'\1_\2', s1).lower()


if __name__ == '__main__':
	testPosts = pickle.load( open(sys.argv[2], 'rb') )
	topK = int(sys.argv[3])
	
	wfile = open(sys.argv[4], 'w')
	out = []
	cnt = -1
	cumRec = 0.0
	for post in testPosts:
		#start_time = time.time()
		cnt += 1
		text = post['body']
		# text = BeautifulSoup(post['Body']).get_text()
		# text = re.sub('(\\n)|(\')|(/)|(\d+)', ' ', text)
		# text = text.lower()
		tempDict = {}
		# textWords = text.split()
		pos_tags = ''
		for word_pos_tag_i in post['postagged']:
			pos_tags += ' ' + word_pos_tag_i
		pos_tags = pos_tags.strip()
		pos_tags_list = pos_tags.split()

		# pos_tags = ''
		sum_ = 0.0
		# for word,pos_tag in pos_tags:
		for word_pos_tag in pos_tags_list:
			pos_tag = word_pos_tag.split('_')[-1]
			word = word_pos_tag.split('_')[0]
			if not pos_tag.startswith('NN'):
				continue
			#word = word.lower()
			if word.startswith('http://'):
				# print word
				continue

			# if word.lower() in stopwords or word.lower() in stopwords_2 or word.lower() in stopwords_3:
			# 	# print word,pos_tag
			# 	continue

			word = re.sub('^[\d]+', ' ', word)
			word = re.sub('[\d]+$', ' ', word)
			word = word.strip()
			
			if len(word) == 0:
				continue

			words_ = word.split('.')
			for words_i in words_:
				words = convert(words_i).split('_')
				for word_i in words:
					word_i = word_i.lower()
					simTags = difflib.get_close_matches(word_i, taglist)
					simTags = simTags[:20]
					#print word_i
					#print simTags
					for simTag in simTags:
						#simTag = simTags[0]
						jac    = 1 - distance.jaccard(word_i, simTag)
						
						#print simTag,jac
						if jac > 0.6:
							if simTag not in tempDict:
								tempDict[simTag] = 0.0
							tempDict[simTag] += jac
							sum_ += jac

		sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True)
		sorted_x = sorted_x[:topK]
		
		# sum_ = 0.0
		# for pair in sorted_x:
		# 	sum_ += pair[1]

		matchedTags = []
		for pair in sorted_x:
			matchedTags.append((pair[0],pair[1]/sum_))
		# print matchedTags

		# tags = post['Tags']
		# expectedTags = tags.replace('<', ' ').replace('>', ' ').strip().split()
		expectedTags = post['tags']

		#predictedTags = [item[0] for item in matchedTags]
		#cumRec += calcRecall(expectedTags, predictedTags)
		
		#print("--- %s seconds ---" % (time.time() - start_time))
		#sys.stdout.flush()
		
		if cnt%500 == 0:
			print cnt 
			sys.stdout.flush()
		
		temp = {}
		temp['expected'] = expectedTags
		temp['Id'] = post['Id']
		temp['index'] = cnt
		temp['predicted_by_String_Matching'] = matchedTags
		wfile.write(str(temp)+'\n') 
		wfile.flush()
		#print temp
		#if cnt >= 0:
		#	break

	wfile.close()	
	# pickle.dump( out, open(sys.argv[3], "wb") )
	# print out
	#print cumRec/(cnt+1.0)
