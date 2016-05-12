import sys
import operator
import random

if __name__ == '__main__':
	cnt = -1
	
	low = []
	high = []

	with open(sys.argv[1],'r') as f:
		for line in f:
			if cnt >= 0:
				vc = line.strip('\n').strip().strip(',').split(',')[-1]
				if vc == "LowerViewCount":
					low.append(cnt)
				elif vc == "HigherViewCount":
					high.append(cnt)
			cnt += 1

	# print len(low)
	# print len(high)

	cntLow = 0
	while cntLow < 50:
		ind = low.pop(random.randint(0, len(low)-1))
		print ind
		cntLow += 1
	
	cntHi = 0
	while cntHi < 50:
		ind = high.pop(random.randint(0, len(high)-1))
		print ind
		cntHi += 1

	# sorted_x = sorted(tempDict.items(), key=operator.itemgetter(1), reverse=True)
	# sorted_y = sorted_x[:100]
	# sorted_z = sorted_x[300:340]
	# for i in sorted_y:
	# 	print i[0]
	# for i in sorted_z:
	# 	print i[0]