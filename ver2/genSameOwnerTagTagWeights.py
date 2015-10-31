import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys
import pickle

def genSameOwnerTagTagWeights(postInfo, fileout):
	ownerPostCount = {}
	ownerTagCount = {}
	tagPostCount = {}

	tagTotProb = {}
	print 'initialising'
	posts = pickle.load(open(postInfo, 'rb'))
	print 'initialised'
	cnt = 0
	for post in posts:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt

		postTypeId = post['postTypeId']
		ownerUserId = post['ownerUserId']
		tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()
		if int(postTypeId) == 1:
			if ownerUserId not in ownerPostCount.keys():
				ownerPostCount[ownerUserId] = 1
			else: 
				ownerPostCount[ownerUserId] += 1
			
			if ownerUserId not in ownerTagCount.keys():
				ownerTagCount[ownerUserId] = {}
				
			for tag in tags:
				if tag not in ownerTagCount[ownerUserId].keys():
					ownerTagCount[ownerUserId][tag] = 0
				ownerTagCount[ownerUserId][tag] += 1 
				
				if tag not in tagPostCount.keys():
					tagPostCount[tag] = 0
				tagPostCount[tag] += 1 

		# if cnt > 1000:
		# 	break

	tagTagProb = {}
	cnt = 0
	for post in posts:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt

		postTypeId = post['postTypeId']
		ownerUserId = post['ownerUserId']
		tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()

		if int(postTypeId) == 1:
			for tag2,tagCount in ownerTagCount[ownerUserId].items():
				if tag2 not in tagTagProb:
					tagTagProb[tag2] = {}
					tagTotProb[tag2] = 0.0
				for tag1 in tags:
					prob = \
					(float(tagCount)/tagPostCount[tag2])\
					*(1.0/ownerPostCount[ownerUserId])*(1.0/len(tags))

					if tag1 not in tagTagProb[tag2]:
						tagTagProb[tag2][tag1] = 0.0
					tagTagProb[tag2][tag1] += prob
					tagTotProb[tag2] += prob

		# if cnt > 1000:
		# 	break
	
	for tag1,valueDict in tagTagProb.items():
		for tag2,val in valueDict.items():
			tagTagProb[tag1][tag2] = val/tagTotProb[tag1]

	pickle.dump(tagTagProb, open(fileout, 'wb'))	
	

def main():
	genSameOwnerTagTagWeights(sys.argv[1], sys.argv[2])
	
if __name__ == '__main__':
	main()