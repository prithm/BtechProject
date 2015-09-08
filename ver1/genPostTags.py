import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys


def genPostTags(input, postType, fileout):
	tree = ET.parse(input)
	rawPosts = tree.getroot()
	tempFile = open(fileout + '.temp.txt', 'w')

	for rawPost in rawPosts:
		postJson = rawPost.attrib
		postId = postJson.get('Id')
		rawTags = postJson.get('Tags')
		postTypeId = postJson.get('PostTypeId')
		if postTypeId is not None and int(postTypeId) == postType and postId is not None and rawTags is not None:
			tags = rawTags.strip().strip('<').strip('>').split('><')
			for tag in tags:
				tempFile.write(postId + ' ' + tag + '\n')
	
	tempFile.close()			


def genTagCount(fileout):
	tagPostCount = {}
	tempFile = open(fileout + '.temp.txt', 'r')
	for line in tempFile:
		tag = line.strip('\n').strip().split(' ')[1]
		if tag not in tagPostCount.keys():
			tagPostCount[tag] = 1
		else: 
			tagPostCount[tag] += 1
	tempFile.close()
	return tagPostCount

def printTagPostCount(tagPostCount, fileout):
	tagPostCountOutputFile = open(fileout,'w')
	for tag,count in tagPostCount.items():
		out = tag + ' ' + str(count)
		tagPostCountOutputFile.write(out + '\n')
	tagPostCountOutputFile.close()

def main():
	genPostTags(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	tagPostCount = genTagCount(sys.argv[3])
	printTagPostCount(tagPostCount, sys.argv[3])
	
if __name__ == '__main__':
	main()
