import sys

def printRWWeightsLinkedByAnswer(ownerUserIdPostsInput, postTagWeightsInput, edgesLinkedByAnswer, rwWeightsLinkedByAnswerOutput):

	postTagWeights = {}
	postTagWeightsInputFile = open(postTagWeightsInput, 'r')
	for line in postTagWeightsInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		postId = lineParts[0]
		tag = lineParts[1]
		weight = float(lineParts[2])
		if postId not in postTagWeights.keys():
			postTagWeights[postId] = {}
		postTagWeights[postId][tag] = weight	

	postTagWeightsInputFile.close()

	ownerUserIdPostsInputFile = open(ownerUserIdPostsInput, 'r')
	ownerUserIdPosts = {}

	for line in ownerUserIdPostsInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		ownerUserId = lineParts[0]
		postIds = lineParts[1:]
		ownerUserIdPosts[ownerUserId] = postIds

	ownerUserIdPostsInputFile.close()

	edgesLinkedByAnswerFile = open(edgesLinkedByAnswer, 'r')
	rwWeightsLinkedByAnswerOutputFile = open(rwWeightsLinkedByAnswerOutput, 'w')

	for line in edgesLinkedByAnswerFile:
		lineParts = line.strip('\n').strip().split(' ')
		user1 = lineParts[0]
		user2 = lineParts[1]
		if user1 in ownerUserIdPosts.keys() and user2 in ownerUserIdPosts.keys():
			postIds1 = ownerUserIdPosts[user1]
			postIds2 = ownerUserIdPosts[user2]
			for i in xrange(0,len(postIds1)):
				postId1 = postIds1[i]
				for j in xrange(0,len(postIds2)):
					postId2 = postIds2[j]
					if postId1 in postTagWeights.keys() and postId2 in postTagWeights.keys():
						for tag1,weight1 in postTagWeights[postId1].items():
							for tag2,weight2 in postTagWeights[postId2].items():
								rwWeightsLinkedByAnswerOutputFile.write( \
									str(postId1) + ' ' + \
									str(postId2) + ' ' + \
									str(tag1) + ' ' + \
									str(tag2) + ' ' + \
									str(weight1) + ' ' + \
									str(weight2) + ' ' + \
									str(weight1*weight2) + '\n' \
								)

	edgesLinkedByAnswerFile.close()						
	rwWeightsLinkedByAnswerOutputFile.close()


def main():
	printRWWeightsLinkedByAnswer(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
	main()
