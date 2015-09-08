import sys

def printPostTagEdgeWeights(postTagInput,postTagEdgeWeightOutput):

	lastPostId = '-1'
	tags = []
	postTagInputFile = open(postTagInput, 'r')
	postTagEdgeWeightOutputFile = open(postTagEdgeWeightOutput, 'w')
	for line in postTagInputFile:
		lineParts = line.strip('\n').strip().split(' ')
		postId = lineParts[0]
		tag = lineParts[1]
		if lastPostId != postId:
			if lastPostId != '-1':
				weight = 1.0/float(len(tags))
				for tag in tags:
					postTagEdgeWeightOutputFile.write(lastPostId + ' ' + tag + ' ' + str(weight) + '\n') 

			lastPostId = postId
			tags = []
			tags.append(tag)
			
		else:
			tags.append(tag)

	weight = 1.0/float(len(tags))
	for tag in tags:
		postTagEdgeWeightOutputFile.write(lastPostId + ' ' + tag + ' ' + str(weight) + '\n') 				

	postTagInputFile.close()
	postTagEdgeWeightOutputFile.close()

def main():
	printPostTagEdgeWeights(sys.argv[1],sys.argv[2])

if __name__ == '__main__':
	main()
