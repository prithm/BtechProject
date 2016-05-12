import sys
import pickle
import nltk
from bs4 import BeautifulSoup
import re

K_FIC = 70

def find_spreading_actvation(source_tag,predicted_tags,P_tag_tag,cur_hop,max_hop):
	if cur_hop > max_hop:
		return predicted_tags
	else:
		if source_tag not in P_tag_tag.keys():
			return predicted_tags
		for tag in P_tag_tag[source_tag].keys():
			if tag not in predicted_tags.keys():
				predicted_tags[tag] = 0.0
			w = predicted_tags[source_tag]*P_tag_tag[source_tag][tag]
			if w > predicted_tags[tag]:
				predicted_tags[tag] = w
				# predicted_tags = find_spreading_actvation(tag,predicted_tags,P_tag_tag,cur_hop+1,max_hop)
		return predicted_tags

def find_associated_tags(body,P_word_tag,P_tag_tag):
	words  =  body.split()
	pos_tags = nltk.pos_tag(words)
	predicted_tags = {}
	cumm_n = 0.0
	for word,pos_tag in pos_tags:
		if not pos_tag.startswith('NN'):
			continue
		if word in P_word_tag.keys():
			for tag in P_word_tag[word].keys():
				if tag not in predicted_tags.keys():
					predicted_tags[tag] = 0.0
				predicted_tags[tag] += P_word_tag[word][tag]
				cumm_n += P_word_tag[word][tag]
	for tag in predicted_tags.keys():
		predicted_tags[tag] /= cumm_n
	# sorted_x = sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)
	# sorted_x = sorted_x[:K_FIC]
	# predicted_tags = {}
	# for tag,prob in sorted_x:
		# predicted_tags[tag] = prob
	#print sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)[:20]
	#print
	predicted_tags_keys = predicted_tags.keys()	
	for source_tag in predicted_tags_keys:
		for tag in P_tag_tag[source_tag].keys():
			if tag not in predicted_tags.keys():
				predicted_tags[tag] = 0.0
			w = predicted_tags[source_tag]*P_tag_tag[source_tag][tag]
			if w > predicted_tags[tag]:
				predicted_tags[tag] = w
	#print sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)[:20]
	#print 
	return predicted_tags



if __name__ == '__main__':
	validationPosts = pickle.load( open(sys.argv[1], 'rb') )
	part_ = int(sys.argv[2])
	for part in xrange(part_,part_+1):
		print part
		sys.stdout.flush()
		P_word_tag 	= pickle.load( open(sys.argv[3],'rb'))
		P_tag_tag 	= pickle.load( open(sys.argv[4],'rb'))
		# validationPosts	= pickle.load( open('../data/TestPosts_50K_EnTagRec_'+str(part)+'_.pickle','rb'))

		# validationPrediction = {}
		# validationPrediction['expected'] = []
		# validationPrediction['predicted'] = []
		print 'Init'
		sys.stdout.flush()	
		wfile = open(sys.argv[5], 'w')
		cnt = 0
		for post in validationPosts:
			# if int(post['PostTypeId']) != 1:
			# 	continue
			# print post['Body']
			cnt += 1
			#print cnt
			#sys.stdout.flush()
			if cnt%500 == 0:
				print cnt
				sys.stdout.flush()
				wfile.flush()
				#break
			# body =  BeautifulSoup(post['Body'], 'lxml').get_text()
			# body = re.sub(r'\n',' ',body)
			# body = body.encode("utf-8")
			# body = re.sub('[^a-zA-Z]', ' ', body)
			# curr_tags = post['Tags'].strip().strip('>').strip('<').replace('><', ' ').strip().split(' ')
			# everything['docs'].append(body)
			# everything['tags'].append(curr_tags)
			
			body = post['body']
			curr_tags = post['tags']
			#print body
			#print curr_tags
			#print 
			predicted_tags = find_associated_tags(body,P_word_tag,P_tag_tag)
			sorted_x = sorted(predicted_tags.items(), key=lambda x:x[1], reverse= True)
			predicted = sorted_x[:70]
			# validationPrediction['expected'].append(curr_tags)
			# validationPrediction['predicted'].append(predicted)
			tempu = {}
			tempu['expected'] = curr_tags
			
			matched_Tags = []
			sum_ = 1.0
			for it in predicted:
				sum_ += it[1]
			for it in predicted:
				matched_Tags.append( (it[0],it[1]/sum_) )
			tempu['predicted_By_FIC'] = matched_Tags
			wfile.write(str(tempu)+'\n')
			wfile.flush()
			#break
		
		wfile.flush()
		wfile.close()


		# pickle.dump( validationPrediction, open('../data/AllPostsSeedTags_50K_EnTagRec_ByFIC'+str(part)+'_.pickle', 'wb') )
