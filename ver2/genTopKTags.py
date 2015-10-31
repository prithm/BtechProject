import sys
import numpy as np

def genTopKTags(overallWeights, k, topKOutput):
	overallWeightsFile = open(overallWeights, 'r')
	
	topKListValue =[]
	topKListPair  =[]

	for line in overallWeightsFile:
		lineParts = line.strip('\n').strip().split(' ')
		value = float(lineParts[2])
		topKListValue.append(-value)
		topKListPair.append((lineParts[0], lineParts[1]))

			

	overallWeightsFile.close()
	indices = np.argsort(topKListValue)
	topKOutputFile = open(topKOutput, 'w')

	maxValue = topKListValue[indices[0]]
	print maxValue
	for i in indices[0:50]:
		print topKListValue[i]
		topKOutputFile.write\
		(topKListPair[i][0] + ' ' + topKListPair[i][1] + ' ' + str(topKListValue[i]/maxValue) + '\n')

	topKOutputFile.close()	



def main():
	genTopKTags(sys.argv[1],int(sys.argv[2]),sys.argv[3])


if __name__ == '__main__':
	main()
