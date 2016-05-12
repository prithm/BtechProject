import sys
from calcPrecisionRecall import calcPrecision_2, calcRecall_2

if __name__ == '__main__':
	wfile = open(sys.argv[2],'w')
	
	with open(sys.argv[1], 'r') as f:
		for line in f:
			post = eval(line.strip('\n'))
			expectedTags = post['expected']
			predictedTags = [item[0] for item in post['predicted_by_Hybrid_Matching']]
			prec = calcPrecision_2(expectedTags, predictedTags)
			rec = calcRecall_2(expectedTags, predictedTags)
			out = ''
			for i in prec:
				out += str(i) + ' ,'
			for i in rec:
				out += str(i) + ' ,'
			wfile.write(out+'\n')
			wfile.flush()
	wfile.close()