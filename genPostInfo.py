import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys

#postType ownerUser postId parentId tags
def genPostTypeOwnerIdAndSelfId(input, fileout):
	cnt = 0
	
	postInfoOutputFile = open(fileout, 'w')
	with open(input,'r') as f:
		for line in f: 
			cnt += 1
			if cnt < 3:
				continue
			try:
				post = ET.fromstring(line.strip().strip('\n').strip())
			except Exception as e:
				continue

			postId = post.get('Id')
			ownerUserId = post.get('OwnerUserId')
			postTypeId = post.get('PostTypeId')
			
			tags = post.get('Tags')
			if tags is None:
				tags = '<>'
			
			if postTypeId is not None and postId is not None and ownerUserId is not None and ownerUserId != '-1':
				if postTypeId == '2':
					parentId = post.get('ParentId')
					if parentId is None:
						parentId = '-1'
				else:
					parentId = '-1'
				postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + ' ' + parentId + ' ' + tags + '\n')

			if cnt % 1000 == 0:
				print cnt

	postInfoOutputFile.close()


def main():
	genPostTypeOwnerIdAndSelfId(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()