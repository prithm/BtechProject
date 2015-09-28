import sys

def main():
	tagOccur = {}
	tagTagCoOccur = {}
	cnt = 0
	with open(sys.argv[1], 'r') as f:
		for line in f:
			cnt += 1
			if cnt % 1000 == 0:
				print cnt
			lineParts = line.strip().strip('\n').split(' ')
			postTypeId = int(lineParts[0])
			ownerUserId = lineParts[1]
			postId = lineParts[2]
			if postTypeId == 1:
				tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()
				for tag in tags:
					if tag not in tagOccur.keys():
						tagOccur[tag] = 0
						tagTagCoOccur[tag] = {}
					tagOccur[tag] += 1
				for tag1 in tags:
					for tag2 in tags:
						if tag2 not in tagTagCoOccur[tag1].keys():
							tagTagCoOccur[tag1][tag2] = 0
						tagTagCoOccur[tag1][tag2] += 1


	with open(sys.argv[2], 'w') as f:					
		for tag1 in tagTagCoOccur.keys():
			for tag2,val in tagTagCoOccur[tag1].items():
				f.write(tag2 + ' ' + tag1 + ' ' + str(float(val)/tagOccur[tag1]) + '\n')


if __name__ == '__main__':
	main()