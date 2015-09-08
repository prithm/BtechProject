import sys

def printRWWeightsLinkedByPostLinks(edgesLinkedByPostLinks, postTagWeightsInput, rwWeightsLinkedByPostLinksOuput, postLinkType):

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

	edgesLinkedByPostLinksFile = open(edgesLinkedByPostLinks, 'r')
	rwWeightsLinkedByPostLinksOuputFile = open(rwWeightsLinkedByPostLinksOuput, 'w')

	for line in edgesLinkedByPostLinksFile:

		lineParts = line.strip('\n').strip().split(' ')
		postId1 = lineParts[0]
		postId2 = lineParts[1]
		linkType = int(lineParts[2])
		if linkType == postLinkType:
			if postId1 in postTagWeights.keys() and postId2 in postTagWeights.keys():
				for tag1,weight1 in postTagWeights[postId1].items():
					for tag2,weight2 in postTagWeights[postId2].items():
						rwWeightsLinkedByPostLinksOuputFile.write( \
							str(postId1) + ' ' + \
							str(postId2) + ' ' + \
							str(tag1) + ' ' + \
							str(tag2) + ' ' + \
							str(weight1) + ' ' + \
							str(weight2) + ' ' + \
							str(weight1*weight2) + '\n' \
						)
		

	edgesLinkedByPostLinksFile.close()
	rwWeightsLinkedByPostLinksOuputFile.close()
					

def main():
	printRWWeightsLinkedByPostLinks(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))

if __name__ == '__main__':
	main()
