import sys

def printEdgesLinkedByCommentUserMentions(userInfoInput, commentIdInfoInput, commentUserMentionsInput, edgesLinkedByCommentUserMentionsOutput):

	userInfoInputFile = open(userInfoInput, 'r')
	displayNameUserId = {}
	for line in userInfoInputFile:
		lineParts = line.strip('\n').strip().split(' ', 7)
		userId = lineParts[0]
		displayName = lineParts[-1]
		displayNameUserId[displayName] = userId

	userInfoInputFile.close()


	commentIdInfoInputFile = open(commentIdInfoInput, 'r')
	commenterIds = {}
	for line in commentIdInfoInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		commenterId = lineParts[0]
		commentId = lineParts[1]
		commenterIds[commentId] = commenterId

	commentIdInfoInputFile.close()	
	

	commentUserMentionsInputFile = open(commentUserMentionsInput, 'r')
	edgesLinkedByCommentUserMentionsOutputFile = open(edgesLinkedByCommentUserMentionsOutput, 'w')
	
	for line in commentUserMentionsInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		commentId = lineParts[0]
		displayName = lineParts[1]
		if commentId in commenterIds.keys() and displayName in displayNameUserId.keys():
			commenterId = commenterIds[commentId]
			userMentionedId = displayNameUserId[displayName]
			edgesLinkedByCommentUserMentionsOutputFile.write(commenterId + ' ' + userMentionedId + ' ' + commentId + '\n')

	commentUserMentionsInputFile.close()
	edgesLinkedByCommentUserMentionsOutputFile.close()

def main():
	printEdgesLinkedByCommentUserMentions(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
