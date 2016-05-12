import sys
import pickle
from calcPrecisionRecall import calcPrecision_2,calcRecall_2

if __name__ == '__main__':
	
	# FIC_tags = pickle.load( open('validationSeedTagsByLDA_2.pickle', 'rb') )
	# LDA_tags = pickle.load( open('validationSeedTagsByFIC.pickle', 'rb') )

	for part in xrange(0,1):
		FIC_tags = []
		LDA_tags = []
		
		num = 47691
		start = int(0.1*(part)*num)
		end = int(0.1*(part+1)*num)
		
		i = 0
		with open(sys.argv[1]+'_'+str(part)+'_.txt', 'r') as f:
			for line in f:
				if i < start or i >= end:
					continue
				post = eval(line.strip('\n'))
				FIC_tags.append(post)
		
		i = 0		
		with open(sys.argv[2], 'r') as f:
			for line in f:
				if i < start or i >= end:
					continue
				post = eval(line.strip('\n'))
				LDA_tags.append(post)


		
		alpha_max = 0.0
		beta_max = 0.0
		recall_max = 0.0
		
		for alpha_i in xrange(0,11):
			for beta_i in xrange(0,11):
				if alpha_i == 0 and beta_i == 0:
					continue
				
				alpha = 0.1*alpha_i
				beta = 0.1*beta_i
				recall = 0.0

				print alpha,beta
				
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
					predicted = [i[0] for i in sorted_x]
			
					recall += calcRecall_2(expectedTags, predicted)[-1]
				
				if 	recall > recall_max:
					recall_max = recall
					alpha_max = alpha
					beta_max = beta

		print alpha_max, beta_max, recall_max/((end-start))
		# wfile = open('../data/EnTagRecWeights_'+str(part)+'_.txt','w')
		# wfile.write(str(alpha_max) + ' ' + str(beta_max) + ' ' + str(recall_max/(num-(end-start))) + '\n' )
		# wfile.flush()
		# wfile.close()

