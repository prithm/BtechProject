import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys
import pickle

def genOwnerPostCount(postInfo, postLinkInfo, fileout):
	ownerPostCount = {}
	ownerTagCount = {}
	tagPostCount = {}
	postLinkPostIds = {} #contains postIds from which there are links to this postId
	postLinkCount = {}
	postUserId = {}

	print 'initialising'
	sys.stdout.flush()
	posts = pickle.load(open(postInfo, 'rb'))
	postLinks = pickle.load(open(postLinkInfo, 'rb'))
	print 'initialised'
	sys.stdout.flush()
	cnt = 0
	for post in posts:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt
		
		postId = post['Id']
		postTypeId = int(post['postTypeId'])
		ownerUserId = post['ownerUserId']
		# tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()
		tags = post['tags']

		if postTypeId == 1:
			postUserId[postId] = ownerUserId

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
	
	cnt = 0
	for postLink in postLinks:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt
			sys.stdout.flush()
		try:
			fromPostId = postLink['sourcePostId']
			toPostId = postLink['targetPostId']
			if fromPostId not in postUserId.keys() or toPostId not in postUserId.keys():
				continue
			if toPostId not in postLinkPostIds.keys():
				postLinkPostIds[toPostId] = []
			postLinkPostIds[toPostId].append(fromPostId)
			
			if fromPostId not in postLinkCount.keys():
				postLinkCount[fromPostId] = 0
			postLinkCount[fromPostId] += 1
		
		except Exception as e:
			print line
			print e
			exit()


	tagTagProb = {}
	tagTotProb = {}
	cnt = 0
	for post in posts:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt

		postId = post['Id']
		postTypeId = int(post['postTypeId'])
		ownerUserId = post['ownerUserId']
		# tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()
		tags = post['tags']

		if postTypeId == 1:
			if postId not in postLinkPostIds.keys():
				continue

			for parentId in postLinkPostIds[postId]:
				if parentId not in postUserId.keys():
					continue
				parentIdUser = postUserId[parentId]
				for tag2,tagCount in ownerTagCount[parentIdUser].items():
					if tag2 not in tagTagProb:
						tagTagProb[tag2] = {}
						tagTotProb[tag2] = 0.0
					for tag1 in tags:
						prob = \
						(float(tagCount)/tagPostCount[tag2])\
						*(1.0/ownerPostCount[parentIdUser])\
						*(1.0/postLinkCount[parentId])\
						*(1.0/ownerPostCount[ownerUserId])\
						*(1.0/len(tags))

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
	genOwnerPostCount(sys.argv[1], sys.argv[2], sys.argv[3])
	
if __name__ == '__main__':
	main()