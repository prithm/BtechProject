import sys

def printEdgesLinkedByComments(postTypeOwnerAndIdInput, commentsInfoInput, edgesLinkedByCommentsOutput):

	postOwnerUserId = {}
	postTypeOwnerAndIdInputFile = open(postTypeOwnerAndIdInput, 'r')
	for line in postTypeOwnerAndIdInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		postId = lineParts[2]
		postOwnerUserId[postId] = ownerUserId

	postTypeOwnerAndIdInputFile.close()
			
	commentsInfoInputFile = open(commentsInfoInput, 'r')		
	edgesLinkedByCommentsOutputFile = open(edgesLinkedByCommentsOutput, 'w')
	for line in commentsInfoInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		commenterId = lineParts[0]
		commentId = lineParts[1]
		postId = lineParts[2]
		if postId in postOwnerUserId:
			ownerUserId = postOwnerUserId[postId]
			if commenterId != ownerUserId:
				edgesLinkedByCommentsOutputFile.write(commenterId + ' ' + ownerUserId + ' ' + commentId + '\n')

	commentsInfoInputFile.close()	
	edgesLinkedByCommentsOutputFile.close()


	

def main():
	printEdgesLinkedByComments(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	main()
