import sys

def printEdgesLinkedByOwnerUserID(postTypeOwnerAndIdInput,postType,edgesLinkedByOwnerUserIDOutput):

	ownerUserIdPosts = {}
	postTypeOwnerAndIdInputFile = open(postTypeOwnerAndIdInput, 'r')
	for line in postTypeOwnerAndIdInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		postId = lineParts[2]
		if postTypeId == postType:
			if ownerUserId not in ownerUserIdPosts.keys():
				ownerUserIdPosts[ownerUserId] = []
			ownerUserIdPosts[ownerUserId].append(postId)

	postTypeOwnerAndIdInputFile.close()
			
	edgesLinkedByOwnerUserIDOutputFile = open(edgesLinkedByOwnerUserIDOutput, 'w')
	for key,postIds in ownerUserIdPosts.items():
		out = key
		for postId in postIds:
			out += ' ' + postId
		edgesLinkedByOwnerUserIDOutputFile.write(out+'\n')

	edgesLinkedByOwnerUserIDOutputFile.close()


	

def main():
	printEdgesLinkedByOwnerUserID(sys.argv[1],int(sys.argv[2]),sys.argv[3])

if __name__ == '__main__':
	main()
