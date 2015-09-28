import pickle
import sys
from sklearn import linear_model

def main():
	tagtagRWR = {}
	with open(sys.argv[1], 'r') as f:
		for line in f:
			lineParts = line.strip().strip('\n').strip().split()
			tag1 = lineParts[1]
			tag2 = lineParts[0]
			prob = float(lineParts[2])
			if tag1 not in tagtagRWR:
				tagtagRWR[tag1] = {}
			if tag2 not in tagtagRWR[tag1]:
				tagtagRWR[tag2] = 0
			tagtagRWR[tag1][tag2] = prob


	tagtagRWR2 = {}
	with open(sys.argv[2], 'r') as f:
		for line in f:
			lineParts = line.strip().strip('\n').strip().split()
			tag1 = lineParts[1]
			tag2 = lineParts[0]
			prob = float(lineParts[2])
			if tag1 not in tagtagRWR:
				continue
			if tag2 not in tagtagRWR[tag1]:
				continue
			if tag1 not in tagtagRWR2:
				tagtagRWR2[tag1] = {}
			if tag2 not in tagtagRWR2[tag1]:
				tagtagRWR2[tag2] = 0
			tagtagRWR2[tag1][tag2] = prob

	tagtagCoOccur = {}
	with open(sys.argv[3], 'r') as f:
		for line in f:
			lineParts = line.strip().strip('\n').strip().split()
			tag1 = lineParts[1]
			tag2 = lineParts[0]
			prob = float(lineParts[2])
			if tag1 not in tagtagRWR2:
				continue
			if tag2 not in tagtagRWR2[tag1]:
				continue
			if tag1 not in tagtagCoOccur:
				tagtagCoOccur[tag1] = {}
			if tag2 not in tagtagCoOccur[tag1]:
				tagtagCoOccur[tag2] = 0
			tagtagCoOccur[tag1][tag2] = prob	


	train = []
	y = []
	for tag1 in tagtagCoOccur:
		for tag2 in tagtagCoOccur[tag1]:
			train.append([tagtagRWR[tag1][tag2], tagtagRWR2[tag1][tag2]])
			y.append(tagtagCoOccur[tag1][tag2])

			
	model = linear_model.LinearRegression()
	model.fit(train, y)
	print model.coef_
	print model.score(train, y)
	pickle.dump( model, open( "LinearRegression.pickle", "wb" ) )


if __name__ == '__main__':
	main()