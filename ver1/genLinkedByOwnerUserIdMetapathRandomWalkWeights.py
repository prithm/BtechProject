import sys

def printRWWeightsLinkedByOwnerUserID(edgesLinkedByOwnerUserId, postTagWeightsInput, rwWeightsLinkedByOwnerUserIDOuput):

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

	edgesLinkedByOwnerUserIdFile = open(edgesLinkedByOwnerUserId, 'r')
	rwWeightsLinkedByOwnerUserIDOuputFile = open(rwWeightsLinkedByOwnerUserIDOuput, 'w')

	for line in edgesLinkedByOwnerUserIdFile:
		lineParts = line.strip('\n').strip().split(' ')
		ownerUserId = lineParts[0]
		postIds = lineParts[1:]
		for i in xrange(0,len(postIds)):
			postId1 = postIds[i]
			for j in xrange(i+1,len(postIds)):
				postId2 = postIds[j]
				if postId1 in postTagWeights.keys() and postId2 in postTagWeights.keys():
					for tag1,weight1 in postTagWeights[postId1].items():
						for tag2,weight2 in postTagWeights[postId2].items():
							rwWeightsLinkedByOwnerUserIDOuputFile.write( \
								str(postId1) + ' ' + \
								str(postId2) + ' ' + \
								str(tag1) + ' ' + \
								str(tag2) + ' ' + \
								str(weight1) + ' ' + \
								str(weight2) + ' ' + \
								str(weight1*weight2) + '\n' \
							)

	edgesLinkedByOwnerUserIdFile.close()						
	rwWeightsLinkedByOwnerUserIDOuputFile.close()


def main():
	printRWWeightsLinkedByOwnerUserID(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	main()
