import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle

# fromId toId linkType
def genPostLinkInfo(postLinkFile, fileout):
	
	out = []
	cnt = 0
	with open(postLinkFile,'r') as f:
		for line in f: 
			cnt += 1
			if cnt % 10000 == 0:
				print cnt

			if cnt < 3:
				continue
			try:
				post = ET.fromstring(line.strip().strip('\n').strip())
			except Exception as e:
				continue

			sourcePostId = post.get('PostId')
			targetPostId = post.get('RelatedPostId')
			linkType = post.get('LinkTypeId')
			if sourcePostId is not None and targetPostId is not None and linkType is not None:
				# if sourcePostId in questionIds and targetPostId in questionIds:
				# postLinkInfoOutputFile.write(sourcePostId + ' ' + targetPostId + ' ' + linkType + '\n')
				tempDict = {}
				tempDict['sourcePostId'] = sourcePostId
				tempDict['targetPostId'] = targetPostId
				tempDict['linkType'] = int(linkType)
				out.append(tempDict)
			# if cnt > 200000:	
			# 	break

	pickle.dump(out, open(fileout, 'wb') )		
	


def main():
	genPostLinkInfo(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()