import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys

#postType ownerUser postId parentId(absent in case of questions)
def genPostTypeOwnerIdAndSelfId(input, fileout):
	tree = ET.parse(input)
	rawPosts = tree.getroot()
	postInfoOutputFile = open(fileout, 'w')
	for rawPost in rawPosts:
		post = rawPost.attrib
		postId = post.get('Id')
		ownerUserId = post.get('OwnerUserId')
		postTypeId = post.get('PostTypeId')
		if postTypeId is not None and postId is not None and ownerUserId is not None and ownerUserId != '-1':
			if postTypeId == '2':
				parentId = post.get('ParentId')
				if parentId is not None:
					postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + ' ' + parentId + '\n')
			elif postTypeId == '1':
				postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + '\n')
	
	postInfoOutputFile.close()


def main():
	genPostTypeOwnerIdAndSelfId(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()