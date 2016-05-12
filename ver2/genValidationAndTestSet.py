import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle

print 'Initialising'
sys.stdout.flush()
trainingTags = pickle.load( open(sys.argv[2],'rb') )
trainingTagSet = set(trainingTags)
print 'Initialised'
sys.stdout.flush()

#postType ownerUser postId parentId tags
def genValidationAndTestSet(input, fileout):
	cnt = 0
	out = []
	start = 500000
	entrycnt = 0
	with open(input,'r') as f:
		for line in f: 
			cnt += 1
			if cnt < start:
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

			if postTypeId is None or postTypeId != '1':
				continue

			if tags is None:
				continue
			taglist = tags.replace('<', ' ').replace('>', ' ').strip().split()
			if len(taglist) <= 0:
				continue
			
			flag = 0
			for tag in taglist:
				if tag in trainingTagSet:
					flag += 1
					# break

			if flag != len(taglist):
				continue

			# print cnt
			# sys.stdout.flush()
			


			if postTypeId is not None and postTypeId == '1' and postId is not None and ownerUserId is not None and ownerUserId != '-1':
				
				Id = post.get('Id')
				PostTypeId = post.get('PostTypeId')
				AcceptedAnswerId = post.get('AcceptedAnswerId')
				CreationDate = post.get('CreationDate')
				Score = post.get('Score')
				ViewCount = post.get('ViewCount')
				Body = post.get('Body')
				OwnerUserId = post.get('OwnerUserId')
				LastEditorUserId = post.get('LastEditorUserId')
				LastEditorDisplayName = post.get('LastEditorDisplayName')
				LastEditDate = post.get('LastEditDate')
				LastActivityDate = post.get('LastActivityDate')
				Title = post.get('Title')
				Tags = post.get('Tags')
				AnswerCount = post.get('AnswerCount')
				CommentCount = post.get('CommentCount')
				FavoriteCount = post.get('FavoriteCount')

				tempDict = {}
				tempDict['Id'] = Id
				tempDict['PostTypeId'] = PostTypeId
				tempDict['AcceptedAnswerId'] = AcceptedAnswerId
				tempDict['CreationDate'] = CreationDate
				tempDict['Score'] = Score
				tempDict['ViewCount'] = ViewCount
				tempDict['Body'] = Body
				tempDict['OwnerUserId'] = OwnerUserId
				tempDict['LastEditorUserId'] = LastEditorUserId
				tempDict['LastEditorDisplayName'] = LastEditorDisplayName
				tempDict['LastEditDate'] = LastEditDate
				tempDict['LastActivityDate'] = LastActivityDate
				tempDict['Title'] = Title
				tempDict['Tags'] = Tags
				tempDict['AnswerCount'] = AnswerCount
				tempDict['CommentCount'] = CommentCount
				tempDict['FavoriteCount'] = FavoriteCount
				entrycnt += 1
				out.append(tempDict)
				
				# postInfoOutputFile.write(postTypeId + ' ' + ownerUserId + ' ' + postId + ' ' + parentId + ' ' + tags + '\n')
				# print str(tempDict)
				# sys.stdout.flush()
			if entrycnt > 25000:
				break
			if entrycnt%500 == 0:
				print entrycnt
				sys.stdout.flush()

				
	pickle.dump( out, open(fileout, "wb") )


def main():
	genValidationAndTestSet(sys.argv[1],sys.argv[3])

if __name__ == '__main__':
	main()