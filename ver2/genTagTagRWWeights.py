import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genOwnerPostCount(postInfo, postType, fileout):
	ownerPostCount = {}
	ownerTagCount = {}
	tagPostCount = {}

	postInfoFile = open(postInfo, 'r')
	cnt = 0
	for line in postInfoFile:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt

		lineParts = line.strip().strip('\n').split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()

		if postTypeId == postType:
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

		if cnt > 1000:
			break
		
	postInfoFile.close()

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
		tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()

		if postTypeId == postType:
			for tag1 in tags:
				for tag2,tagCount in ownerTagCount[ownerUserId].items():
					prob = \
					(float(tagCount)/tagPostCount[tag2])\
					*(1.0/ownerPostCount[ownerUserId])*(1.0/len(tags))

					tagTagProbFile.write(tag1 + ' ' + tag2 + ' ' + str(prob) + '\n')

		if cnt > 1000:
			break
		
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
	with open('ownerPostCount', 'w') as f:
		for key,value in ownerPostCount.items():
			f.write(str(key) + ' ' + str(value) + '\n')
	
	with open('tagPostCount', 'w') as f:
		for key,value in tagPostCount.items():
			f.write(str(key) + ' ' + str(value) + '\n')

	with open('ownerTagCount', 'w') as f:
		for key,value in ownerTagCount.items():
			tempDict = {}
			tempDict[key] = value
			f.write(str(tempDict) + '\n')


def main():
	genOwnerPostCount(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	
if __name__ == '__main__':
	main()