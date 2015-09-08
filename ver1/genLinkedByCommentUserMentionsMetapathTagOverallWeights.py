import sys

def printRWWeightsLinkedByCommentsUserMentions(rwWeightsLinkedByCommentsUserMentionsInput, tagRWWeightsLinkedByCommentsUserMentionsOutput):

	tagWeights = {}
	rwWeightsLinkedByCommentsUserMentionsInputFile = open(rwWeightsLinkedByCommentsUserMentionsInput, 'r')
	cnt = 0
	for line in rwWeightsLinkedByCommentsUserMentionsInputFile:
		
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
	
	rwWeightsLinkedByCommentsUserMentionsInputFile.close()
	
	tagRWWeightsLinkedByCommentsUserMentionsOutputFile = open(tagRWWeightsLinkedByCommentsUserMentionsOutput, 'w')
	for tag12, weight in tagWeights.items():
		tags = tag12.split('$$$')
		tagRWWeightsLinkedByCommentsUserMentionsOutputFile.write(tags[0] + ' ' + tags[1] + ' ' + str(weight) + '\n') 	

	tagRWWeightsLinkedByCommentsUserMentionsOutputFile.close()
		
def main():
	printRWWeightsLinkedByCommentsUserMentions(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()
