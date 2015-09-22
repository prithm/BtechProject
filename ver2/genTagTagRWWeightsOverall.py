import sys

def main():
	tagTagProb = {}
	cnt = 0
	with open(sys.argv[1], 'r') as f:
		for line in f:
			cnt += 1
			if cnt%1000 == 0:
				print cnt
			lineParts = line.strip().strip('\n').strip().split()
			tag1 = lineParts[0]
			tag2 = lineParts[1]
			if tag1 == tag2:
				continue
			prob = float(lineParts[2])
			s = tag1+'$$$'+tag2
			if tag1 not in tagTagProb.keys():
				tagTagProb[tag1] = {}
			if tag2 not in tagTagProb[tag1].keys():
				tagTagProb[tag1][tag2] = 0
			tagTagProb[tag1][tag2] += prob


	with open(sys.argv[2], 'w') as f:
		for tag1,valDict in tagTagProb.items():
			for tag2,val in valDict.items():
				f.write(tag1 + ' ' + tag2 + ' ' + str(val) + '\n')


if __name__ == '__main__':
	main()