import sys

def main():
	tagTagProb = {}
	with open(sys.argv[1], 'r') as f:
		for line in f:
			lineParts = line.strip().strip('\n').strip().split()
			tag1 = lineParts[0]
			tag2 = lineParts[1]
			if tag1 == tag2:
				continue
			prob = float(lineParts[2])
			s = tag1+'$$$'+tag2
			if s not in tagTagProb.keys():
				tagTagProb[s] = 0
			tagTagProb[s] += prob


	with open(sys.argv[2], 'w') as f:
		for s,val in tagTagProb.items():
			tag1 = s.split('$$$')[0]
			tag2 = s.split('$$$')[1]
			f.write(tag1 + ' ' + tag2 + ' ' + str(val) + '\n')


if __name__ == '__main__':
	main()