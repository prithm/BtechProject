import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genOwnerPostCount(postInfo, postType, fileout):
	ownerPostCount = {}
	postInfoFile = open(postInfo, 'r')
	for line in postInfoFile:
		lineParts = line.strip().strip('\n').split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		if postTypeId == postType:
			if ownerUserId not in ownerPostCount.keys():
				ownerPostCount[ownerUserId] = 1
			else: 
				ownerPostCount[ownerUserId] += 1
	postInfoFile.close()

	ownerPostCountOutputFile = open(fileout, 'w')
	for ownerUserId, count in ownerPostCount.items():
		ownerPostCountOutputFile.write(ownerUserId + ' ' + str(count))

	ownerPostCountOutputFile.close()

def main():
	genOwnerPostCount(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	
if __name__ == '__main__':
	main()