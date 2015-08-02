import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genOwnerPaperCountTempFile(input, postType, fileout):
	tree = ET.parse(input)
	rawPosts = tree.getroot()
	tempFile = open(fileout + '.temp.txt', 'w')
	for rawPost in rawPosts:
		post = rawPost.attrib
		ownerUserId = post.get('OwnerUserId')
		postTypeId = post.get('PostTypeId')
		if postTypeId is not None and int(postTypeId) == postType and ownerUserId is not None and ownerUserId != '-1':
			tempFile.write(ownerUserId + '\n')
	tempFile.close()

def genOwnerPostCount(fileout):
	ownerPostCount = {}
	tempFile = open(fileout + '.temp.txt', 'r')
	for line in tempFile:
		ownerUserId = line.strip('\n').strip()
		if ownerUserId not in ownerPostCount.keys():
				ownerPostCount[ownerUserId] = 1
		else: 
			ownerPostCount[ownerUserId] += 1
	tempFile.close()
	return ownerPostCount

def printSameOwnerPaperCount(ownerPostCount, fileout):
	sameOwnerPaperCountOutputFile = open(fileout,'w')
	for owner,count in ownerPostCount.items():
			out = owner + ' ' + str(count)
			sameOwnerPaperCountOutputFile.write(out + '\n')
	sameOwnerPaperCountOutputFile.close()	 	

def main():
	genOwnerPaperCountTempFile(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	ownerPostCount = genOwnerPostCount(sys.argv[3])
	printSameOwnerPaperCount(ownerPostCount, sys.argv[3])
	
if __name__ == '__main__':
	main()