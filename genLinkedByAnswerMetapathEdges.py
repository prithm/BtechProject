import sys

def printEdgesLinkedByAnswer(postTypeOwnerAndIdInput, edgesLinkedByAnswerOutput):

	postOwnerUserId = {}
	answerOwnerUserId = {}
	answerQuestionId = {}
	postTypeOwnerAndIdInputFile = open(postTypeOwnerAndIdInput, 'r')
	for line in postTypeOwnerAndIdInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		postTypeId = int(lineParts[0])
		ownerUserId = lineParts[1]
		postId = lineParts[2]
		if postTypeId == 1:
			postOwnerUserId[postId] = ownerUserId
		elif postTypeId == 2:
			parentId = lineParts[3]
			answerOwnerUserId[postId] = ownerUserId
			answerQuestionId[postId] = parentId

	postTypeOwnerAndIdInputFile.close()
			
	edgesLinkedByAnswerOutputFile = open(edgesLinkedByAnswerOutput, 'w')

	for answerId, answerer in answerOwnerUserId.items():
		questionId = answerQuestionId[answerId]	
		if questionId in postOwnerUserId.keys():
			ownerUserId = postOwnerUserId[questionId]
			edgesLinkedByAnswerOutputFile.write(answerer + ' ' + ownerUserId + '\n')

	edgesLinkedByAnswerOutputFile.close()

def main():
	printEdgesLinkedByAnswer(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()
