import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle
# from nltk.stem.porter import *
import re


# stemmer = PorterStemmer()

# first_cap_re = re.compile('(.)([A-Z][a-z]+)')
# all_cap_re = re.compile('([a-z0-9])([A-Z])')

# def convert(name):
# 	s1 = first_cap_re.sub(r'\1_\2', name)
# 	return all_cap_re.sub(r'\1_\2', s1).lower()

# from nltk.corpus import stopwords

# stopwords \
# = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'yo', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
# stopwords_2 \
# = ['a','able','about','across','after','all','almost','also','am','among','an','and','any','are','as','at','be','because','been','but','by','can','cannot','could','dear','did','do','does','either','else','ever','every','for','from','get','got','had','has','have','he','her','hers','him','his','how','however','i','if','in','into','is','it','its','just','least','let','like','likely','may','me','might','most','must','my','neither','no','nor','not','of','off','often','on','only','or','other','our','own','rather','said','say','says','she','should','since','so','some','than','that','the','their','them','then','there','these','they','this','tis','to','too','twas','us','wants','was','we','were','what','when','where','which','while','who','whom','why','will','with','would','yet','you','your']
# stopwords_3 \
# = ["'tis","'twas","ain't","aren't","can't","could've","couldn't","didn't","doesn't","don't","hasn't","he'd","he'll","he's","how'd","how'll","how's","i'd","i'll","i'm","i've","isn't","it's","might've","mightn't","must've","mustn't","shan't","she'd","she'll","she's","should've","shouldn't","that'll","that's","there's","they'd","they'll","they're","they've","wasn't","we'd","we'll","we're","weren't","what'd","what's","when","when'd","when'll","when's","where'd","where'll","where's","who'd","who'll","who's","why'd","why'll","why's","won't","would've","wouldn't","you'd","you'll","you're","you've"]

#postType ownerUser postId parentId tags

def genTraningAnswersForEnTagRec(input, qfile, fileout):
	cnt = 0
	out = []
	tag_count = {}

	# training_qs = pickle.load( open(qfile,'rb') )
	acount = 0
	q_ids = set()
	owners = set()
	with open(qfile,'r') as training_qs:
		for line in training_qs:
			q = eval(line.strip('\n'))
			owners.add(int(q['ownerUserId'])) 
			q_ids.add(int(q['Id']))

	wfile = open(fileout, 'w')		
	with open(input,'r') as f:
		for line in f: 
			cnt += 1
			if cnt < 3:
				continue
			try:
				post = ET.fromstring(line.strip().strip('\n').strip())
			except Exception as e:
				continue

			postTypeId = post.get('PostTypeId')
			if postTypeId is None or postTypeId != '2':
				continue

			postId = post.get('Id')
			ownerUserId = post.get('OwnerUserId')
			# body = post.get('Body')
			# tags = post.get('Tags')
			parentId = post.get('ParentId')
			if parentId is None or ownerUserId is None:
				continue

			if int(parentId) not in q_ids or int(ownerUserId) not in owners:
				continue
			
			#if tags is None:
			#	tags = '<>'
			
			if postTypeId is not None and postId is not None and ownerUserId is not None:
				
				# parentId = '-1'
				tempDict = {}
				tempDict['Id'] = postId
				tempDict['ownerUserId'] = ownerUserId
				tempDict['postTypeId'] = postTypeId
				tempDict['parentId'] = parentId
				#print body
				#sys.stdout.flush()
				# body =  BeautifulSoup(body, 'lxml').get_text()
				# body = re.sub(r'\n',' ',body)
				# body = body.encode("utf-8")
				# body = re.sub('[^a-zA-Z]', ' ', body)
				# taglist = tags.strip().strip('>').strip('<').replace('><', ' ').strip().split(' ')
				# tempDict['tags'] = taglist
				# for tag in taglist:
				# 	if tag not in tag_count.keys():
				# 		tag_count[tag] = 0
				# 	tag_count[tag] += 1
				# filtered_body = ""
				# words = body.split()
				# for word in words:
				# 	new_words = convert(word).split('_')
				# 	for new_word in new_words:
				# 		if new_word in stopwords or new_word in stopwords_2 or new_word in stopwords_3:
				# 			continue
				# 		else:
				# 			new_word = new_word.lower()
				# 			new_word = stemmer.stem(new_word)
				# 			if new_word == 'c' or len(new_word) > 1:
				# 				filtered_body += ' ' + new_word
				# tempDict['body'] = body
				#print filtered_body
				#sys.stdout.flush()
				# out.append(tempDict)
				wfile.write(str(tempDict)+'\n')

				acount += 1
				if acount % 1000 == 0:
					print 'acount',acount,'cnt',cnt
					wfile.flush()
					sys.stdout.flush()
				if acount >= 500000:
					break	
				
				#break
				# postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + ' ' + parentId + ' ' + tags + '\n')

			if cnt % 1000 == 0:
				print 'acount',acount,'cnt',cnt
				sys.stdout.flush()
		
	# pickle.dump( out, open(fileout, "wb") )
	wfile.flush()
	wfile.close()


def main():
	genTraningAnswersForEnTagRec(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	main()
