import sys


def genTopKTags(overallWeights, k, topKOutput):
	overallWeightsFile = open(overallWeights, 'r')
	
	topKListValue =[0 for i in xrange(0,k)]
	topKListPair  =["" for i in xrange(0,k)]

	for line in overallWeightsFile:
		lineParts = line.strip('\n').strip().split(' ')
		value = float(lineParts[2])

		flag = -1
		for i in xrange(0,k):
			if value > topKListValue[i]:
				flag = i
				break

		if flag >= 0:
			flag = 0
			for i in xrange(1,k):
				if topKListValue[flag] > topKListValue[i]:
					flag = i
			
			topKListValue[flag] = value
			topKListPair[flag] = lineParts[0] + '$$$' + lineParts[1]

			

	overallWeightsFile.close()

	topKOutputFile = open(topKOutput, 'w')
	for i in xrange(0,k-1):
		for j in xrange(i,k-1):
			if topKListValue[j] > topKListValue[j+1] :
				temp = topKListValue[j]
				topKListValue[j] = topKListValue[j+1]
				topKListValue[j+1] = temp
				tempString = topKListPair[j]
				topKListPair[j] = topKListPair[j+1]
				topKListPair[j+1] = tempString


	maxValue = topKListValue[k-1]
	for i in xrange(0,k):
		topKOutputFile.write\
		(topKListPair[k-1-i].split('$$$')[0] + ' ' + topKListPair[k-1-i].split('$$$')[1] + ' ' + str(topKListValue[k-1-i]/maxValue) + '\n')

	topKOutputFile.close()	



def main():
	genTopKTags(sys.argv[1],int(sys.argv[2]),sys.argv[3])


if __name__ == '__main__':
	main()