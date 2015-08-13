import sys

def printRWWeightsLinkedByAnswer(rwWeightsLinkedByAnswerInput, tagRWWeightsLinkedByAnswerOutput):

	tagWeights = {}
	rwWeightsLinkedByAnswerInputFile = open(rwWeightsLinkedByAnswerInput, 'r')
	cnt = 0
	for line in rwWeightsLinkedByAnswerInputFile:
		
		lineParts = line.strip('\n').strip().split(' ')
		tag1 = lineParts[2]
		tag2 = lineParts[3]
		weight = float(lineParts[-1])
		tag12 = tag1 + '$$$' + tag2
		if tag12  in tagWeights.keys():
			tagWeights[tag12] += weight
		tag21 = tag2 + '$$$' + tag1
		if tag21  in tagWeights.keys():
			tagWeights[tag21] += weight
		tagWeights[tag12] = weight

		cnt += 1
		if cnt%10000 == 0:
			print cnt
	
	rwWeightsLinkedByAnswerInputFile.close()
	
	tagRWWeightsLinkedByAnswerOutputFile = open(tagRWWeightsLinkedByAnswerOutput, 'w')
	for tag12, weight in tagWeights.items():
		tags = tag12.split('$$$')
		tagRWWeightsLinkedByAnswerOutputFile.write(tags[0] + ' ' + tags[1] + ' ' + str(weight) + '\n') 	

	tagRWWeightsLinkedByAnswerOutputFile.close()
		
def main():
	printRWWeightsLinkedByAnswer(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()
