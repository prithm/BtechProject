import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle

#postType ownerUser postId parentId tags
def genPostTypeOwnerIdAndSelfId(input, fileout, idfile):
	cnt = 0
	out = []

	postIdset = set()
	with open(idfile, 'r') as f:
		for line in f:
			postIdset.add( int(line.strip('\n')) )

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
			body = post.get('Body')
			tags = post.get('Tags')
			if tags is None:
				tags = '<>'
			
			if postTypeId is not None and postId is not None and int(postId) in postIdset and ownerUserId is not None and ownerUserId != '-1':
				if postTypeId == '2':
					parentId = post.get('ParentId')
					if parentId is None:
						parentId = '-1'
				else:
					parentId = '-1'
				tempDict = {}
				tempDict['Id'] = postId
				tempDict['ownerUserId'] = ownerUserId
				tempDict['postTypeId'] = postTypeId
				tempDict['parentId'] = parentId
				tempDict['tags'] = tags
				tempDict['Body'] = body
				out.append(tempDict)
				# postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + ' ' + parentId + ' ' + tags + '\n')

			if cnt % 1000 == 0:
				print cnt

				
	pickle.dump( out, open(fileout, "wb") )


def main():
	genPostTypeOwnerIdAndSelfId(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	main()