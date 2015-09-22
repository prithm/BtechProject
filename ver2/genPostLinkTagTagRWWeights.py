import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genOwnerPostCount(postInfo, postLinkInfo, fileout):
	ownerPostCount = {}
	ownerTagCount = {}
	tagPostCount = {}
	postLinkPostIds = {} #contains postIds from which there are links to this postId
	postLinkCount = {}
	postUserId = {}

	postInfoFile = open(postInfo, 'r')
	cnt = 0
	for line in postInfoFile:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt

		lineParts = line.strip().strip('\n').split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		postId = lineParts[2]
		tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()

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

		#if cnt > 1000:
		#	break
		
	postInfoFile.close()

	
	postLinkInfoFile = open(postLinkInfo, 'r')
	cnt = 0
	for line in postLinkInfoFile:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt
		try:
			lineParts = line.strip().strip('\n').split(' ')
			fromPostId = lineParts[0]
			toPostId = lineParts[1]
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
			postLinkInfoFile.close()
			exit()

	postLinkInfoFile.close()


	tagTagProbFile = open(fileout, 'w')
	postInfoFile = open(postInfo, 'r')
	cnt = 0
	for line in postInfoFile:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt

		lineParts = line.strip().strip('\n').split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		postId = lineParts[2]

		tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()

		if postTypeId == 1:
			if postId not in postLinkPostIds.keys():
				continue

			for parentId in postLinkPostIds[postId]:
				if parentId not in postUserId.keys():
					continue
				parentIdUser = postUserId[parentId]
				for tag1 in tags:
					for tag2,tagCount in ownerTagCount[parentIdUser].items():
						prob = \
						(float(tagCount)/tagPostCount[tag2])\
						*(1.0/ownerPostCount[parentIdUser])\
						*(1.0/postLinkCount[parentId])\
						*(1.0/ownerPostCount[ownerUserId])\
						*(1.0/len(tags))

						tagTagProbFile.write(tag1 + ' ' + tag2 + ' ' + str(prob) + '\n')

		#if cnt > 1000:
		#	break
		
	postInfoFile.close()
	tagTagProbFile.close()
	# ownerPostCountOutputFile = open(fileout, 'w')
	# for ownerUserId, count in ownerPostCount.items():
	# 	ownerPostCountOutputFile.write(ownerUserId + ' ' + str(count) + '\n')

	# ownerPostCountOutputFile.close()

	# ownerTagCountOutputFile = open(fileout2, 'w')
	# for tag, count in ownerTagCount.items():
	# 	ownerPostCountOutputFile.write(tag + ' ' + str(count) + '\n')

	# ownerTagCountOutputFile.close()
	with open('ownerPostCount_link', 'w') as f:
		for key,value in ownerPostCount.items():
			f.write(str(key) + ' ' + str(value) + '\n')
	
	with open('tagPostCount_link', 'w') as f:
		for key,value in tagPostCount.items():
			f.write(str(key) + ' ' + str(value) + '\n')

	with open('ownerTagCount_link', 'w') as f:
		for key,value in ownerTagCount.items():
			tempDict = {}
			tempDict[key] = value
			f.write(str(tempDict) + '\n')


def main():
	genOwnerPostCount(sys.argv[1], sys.argv[2], sys.argv[3])
	
if __name__ == '__main__':
	main()