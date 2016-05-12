import sys

if __name__ == '__main__':
	prec_rec = {}
	postAtrr = []
	postAtrrCount = {}
	cnt = -1
	with open(sys.argv[1],'r') as f:
		for line in f:
			cnt += 1	
			if cnt <= 0:
				continue
			attrs = line.strip('\n').strip(',').split(',')
			for attr in attrs:
				postAtrrCount[attr] = 0.0
				if attr not in prec_rec.keys():
					prec_rec[attr] = [0.0,0.0,0.0,0.0,0.0,0.0] 
			postAtrr.append(attrs)

	print len(postAtrr)
	# print postAtrr[0]
	# print postAtrr[-1]
	# print prec_rec

	cnt = -1
	with open(sys.argv[2],'r') as f:
		for line in f:
			cnt += 1
			l = line.strip('\n').split(',')
			values = [float(i) for i in l]
			for attr in postAtrr[cnt]:
				postAtrrCount[attr] += 1.0
				for i in xrange(0,6):
					prec_rec[attr][i] += values[i]


	for attr in prec_rec.keys():
		out = attr
		for i in xrange(0,6):
			prec_rec[attr][i] /= postAtrrCount[attr]
			out += ',' + str(prec_rec[attr][i])
		print out



