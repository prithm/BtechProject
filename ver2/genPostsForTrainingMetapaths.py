import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle

#postType ownerUser postId parentId tags
def genPostTypeOwnerIdAndSelfId(input, idfile, fileout):
	cnt = 0
	out = []

	ownerIdset = set()
	tagSet = set()
	a = pickle.load(open(idfile,'rb'))
	for ai in a:
		ownerIdset.add(int(ai['ownerUserId']))
		for tag in ai['tags']:
			tagSet.add(tag)
	print 'Init done'
	print len(tagSet)
	sys.stdout.flush()
	qcount = 0		
	wfile = open(fileout,'w')
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

			if postTypeId != '1':
				continue

			body = post.get('Body')
			tags = post.get('Tags')
			if tags is None:
				tags = '<>'
			tags = tags.replace('<', ' ').replace('>', ' ').strip().split()
			if len(tags) <= 0:
				continue

			if postTypeId is not None and postId is not None and ownerUserId is not None and int(ownerUserId) in ownerIdset and ownerUserId != '-1':
				parentId = '-1'
				tempDict = {}
				mod_tags = []
				for tag in tags:
					if tag in tagSet:
						mod_tags.append(tag) 
				if len(mod_tags) <= 0:
					continue
				tempDict['Id'] = postId
				tempDict['ownerUserId'] = ownerUserId
				tempDict['postTypeId'] = postTypeId
				tempDict['parentId'] = parentId
				tempDict['tags'] = mod_tags
				# tempDict['Body'] = body
				# out.append(tempDict)
				wfile.write(str(tempDict)+'\n')
				qcount += 1
				# postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + ' ' + parentId + ' ' + tags + '\n')
				if qcount%1000 == 0:
					wfile.flush()
					print 'qcount:',qcount,'cnt:',cnt
					sys.stdout.flush()
				if qcount >= 500000:
					break
			# if cnt % 1000 == 0:
			# 	print cnt

				
	# pickle.dump( out, open(fileout, "wb") )
	wfile.flush()
	wfile.close()


def main():
	genPostTypeOwnerIdAndSelfId(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	main()
