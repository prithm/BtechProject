import sys
import pickle
from calcPrecisionRecall import calcPrecision_2,calcRecall_2

if __name__ == '__main__':
	FIC_tags = []
	LDA_tags = []

	alpha = float(sys.argv[4])
	beta = float(sys.argv[5])
	num = 47691
	part = int(sys.argv[6])
	start = int(0.1*(part)*num)
	end = int(0.1*(part+1)*num)

	i = -1
	with open(sys.argv[1], 'r') as f:
		for line in f:
			i += 1
			if i < start or i >= end:
					continue
			FIC_tags.append(eval(line.strip('\n')))

	i = -1		
	with open(sys.argv[2], 'r') as f:
		for line in f:
			i += 1
			if i < start or i >= end:
					continue
			LDA_tags.append(eval(line.strip('\n')))
	
	print len(FIC_tags),len(LDA_tags),start,end
	
	wfile = open(sys.argv[3],'w')
		
	for i in xrange(0,num):
		

		if i < start or i >= end:
			continue
			
		expectedTags = FIC_tags[i]['expected']
		tags = {}
		

		for tag,tag_prob in LDA_tags[i]['predicted']:
			if tag not in tags:
				tags[tag] = 0.0
			tags[tag] += alpha*tag_prob
		
		for tag,tag_prob in FIC_tags[i]['predicted']:
			if tag not in tags:
				tags[tag] = 0.0
			tags[tag] += beta*tag_prob
		
		sorted_x = sorted(tags.items(), key=lambda x:x[1], reverse= True)
		sorted_x = sorted_x[:20]
		tempu = {}
		tempu['expected'] = expectedTags
		tempu['predicted_By_EnTagRec'] = sorted_x
		wfile.write(str(tempu)+'\n')
		wfile.flush()
			
	wfile.flush()
	wfile.close()	

