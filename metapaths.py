import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys


def parsePostXML(input):
	posts = []
	tree = ET.parse(input)
	rawPosts = tree.getroot()
	for rawPost in rawPosts:
		postJson = rawPost.attrib
		posts.append(postJson)
	return posts

def sameOwnerPaperCount(posts, postType):
	ownerPostCount = {}
	for post in posts:
		ownerUserId = post.get('OwnerUserId')
		postTypeId = post.get('PostTypeId')
		if postTypeId is not None and int(postTypeId) == postType and ownerUserId is not None and ownerUserId != '-1':
			if ownerUserId not in ownerPostCount.keys():
				ownerPostCount[ownerUserId] = 1
			else: 
				ownerPostCount[ownerUserId] += 1
	return ownerPostCount

def printSameOwnerPaperCount(ownerPostCount, fileout):
	sameOwnerPaperCountOutputFile = open(fileout,'w')
	for owner,count in ownerPostCount.items():
			out = owner + ' ' + str(count)
			sameOwnerPaperCountOutputFile.write(out + '\n')
		 	

def main():
	posts = parsePostXML(sys.argv[1])
	ownerPostCount = sameOwnerPaperCount(posts, int(sys.argv[2]))
	printSameOwnerPaperCount(ownerPostCount, sys.argv[3])
	
if __name__ == '__main__':
	main()