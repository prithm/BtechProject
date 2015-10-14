import pickle
import sys
import random

def main():

	tagSet = set()
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
				tagtagRWR[tag1][tag2] = 0
			tagtagRWR[tag1][tag2] = prob
			tagSet.add(tag1)
			tagSet.add(tag2)

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
				tagtagRWR2[tag1][tag2] = 0
			tagtagRWR2[tag1][tag2] = prob
			tagSet.add(tag1)
			tagSet.add(tag2)
	

	w = [0.5,  0.5]		
	with open(sys.argv[3], 'r') as postInfo:		
		for line in postInfo:
			lineParts = line.strip().strip('\n').strip().split()
			tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()
			if len(tags) < 3:
				continue
			train = random.sample(tags, len(tags)-1)
			test = []
			for tag in tags:
				if tag not in train:
					test.append(tag)
			maxprob = -100.0
			maxTag = ""

			for tag2 in tagSet:
				totProb = 1.0
				for tag1 in train:
					prob = 0.0
					if tag1 in tagtagRWR:
						if tag2  in tagtagRWR[tag1]:
							prob += w[0]*tagtagRWR[tag1][tag2]
					if tag1 in tagtagRWR2:
						if tag2  in tagtagRWR2[tag1]:
							prob += w[1]*tagtagRWR2[tag1][tag2]
					totProb *= (prob + 0.00000000000001)		
				if totProb > maxprob:
					maxprob = totProb
					maxTag = tag2

			if maxTag == "":
				continue

			if tag2 != test[0]:
				f_o = [0.0, 0.0]
				f_star = [0.0, 0.0]
				for tag1 in train:
					if tag1 in tagtagRWR:
						if maxTag in tagtagRWR[tag1]:
							f_star[0] += tagtagRWR[tag1][maxTag]
					if tag1 in tagtagRWR2:
						if maxTag in tagtagRWR2[tag1]:
							f_star[1] += w[1]*tagtagRWR2[tag1][maxTag]
				for tag1 in train:
					if tag1 in tagtagRWR:
						if test[0] in tagtagRWR[tag1]:
							f_o[0] += tagtagRWR[tag1][test[0]]
					if tag1 in tagtagRWR2:
						if test[0] in tagtagRWR2[tag1]:
							f_o[1] += w[1]*tagtagRWR2[tag1][test[0]]
				
				w[0] += f_o[0] - f_star[0]
				w[1] += f_o[1] - f_star[1]				

			break

	print w

if __name__ == '__main__':
	main()