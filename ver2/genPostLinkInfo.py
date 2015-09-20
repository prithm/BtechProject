import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys

# fromId toId linkType
def genPostLinkInfo(postInfo, postLinkFile, fileout):
	
	questionIds = set()
	postInfoFile = open(postInfo, 'r')
	for line in postInfoFile:
		postType = line.strip().strip('\n').split(' ')[0]
		postId = line.strip().strip('\n').split(' ')[2]
		if postType == '1':
			questionIds.add(postId)
	postInfoFile.close()

	tree = ET.parse(postLinkFile)
	rawPostLinks = tree.getroot()
	postLinkInfoOutputFile = open(fileout, 'w')
	for rawPostLink in rawPostLinks:
		postLink = rawPostLink.attrib
		sourcePostId = postLink.get('PostId')
		targetPostId = postLink.get('RelatedPostId')
		linkType = postLink.get('LinkTypeId')
		if sourcePostId is not None and targetPostId is not None and linkType is not None:
			if sourcePostId in questionIds and targetPostId in questionIds:
				postLinkInfoOutputFile.write(sourcePostId + ' ' + targetPostId + ' ' + linkType + '\n')

	postLinkInfoOutputFile.close()


def main():
	genPostLinkInfo(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	main()