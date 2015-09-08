import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genOwnerPostCount(postInfo, postType, fileout):
	ownerPostCount = {}
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

			for tag in tags:
				if tag not in tagPostCount.keys():
					tagPostCount[tag] = 1
				else: 
					tagPostCount[tag] += 1

		if cnt > 1000:
			break
		
	postInfoFile.close()

	ownerPostCountOutputFile = open(fileout, 'w')
	for ownerUserId, count in ownerPostCount.items():
		ownerPostCountOutputFile.write(ownerUserId + ' ' + str(count) + '\n')

	ownerPostCountOutputFile.close()

	tagPostCountOutputFile = open(fileout2, 'w')
	for tag, count in tagPostCount.items():
		ownerPostCountOutputFile.write(tag + ' ' + str(count) + '\n')

	tagPostCountOutputFile.close()


def main():
	genOwnerPostCount(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4])
	
if __name__ == '__main__':
	main()