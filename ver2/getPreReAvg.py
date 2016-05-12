import sys

if __name__ == '__main__':
	tot_prec = {}
	tot_rec = {}
	cnt_prec = {}
	cnt_rec = {}
	with open(sys.argv[1], 'r') as f:
		for line in f:
			body = eval(line.strip('\n'))
			for key,prec in body['precision_by_combined_meta'].items():
				if key <= 3:
					key = 3
				elif key > 3 and key <= 5:
					key = 5
				elif key > 5:
					key = 10

				if key not in tot_prec:
					tot_prec[key] = 0.0
					cnt_prec[key] = 0.0
				tot_prec[key] += prec
				cnt_prec[key] += 1.0
			for key,rec in body['recall_by_combined_meta'].items():
				if key <= 3:
					key = 3
				elif key > 3 and key <= 5:
					key = 5
				elif key > 5:
					key = 10

				if key not in tot_rec:
					tot_rec[key] = 0.0
					cnt_rec[key] = 0.0
				tot_rec[key] += rec
				cnt_rec[key] += 1.0

	print 'Prec:',
	for key,val in tot_prec.items():
		print key,':',tot_prec[key]/cnt_prec[key],

	print 

	print 'Rec:',
	for key,val in tot_rec.items():
		print key,':',tot_rec[key]/cnt_rec[key],

	print 



# prithwish@PRITHWISH:~/Desktop/iitsem7/BTP/sem7$ python code/BtechProject/ver2/getPreReAvg.py stackOverflowData/train_results/surveyQAHybridMatchesEval.txt
# Prec: 10 : 0.154 3 : 0.266666666667 5 : 0.212
# Rec: 10 : 0.505333333333 3 : 0.273 5 : 0.353666666667
# prithwish@PRITHWISH:~/Desktop/iitsem7/BTP/sem7$ python code/BtechProject/ver2/getPreReAvg.py stackOverflowData/train_results/surveyQAStringMatchesEval.txt
# Prec: 10 : 0.16330749354 3 : 0.274509803922 5 : 0.23137254902
# Rec: 10 : 0.504263565891 3 : 0.277450980392 5 : 0.361437908497
# prithwish@PRITHWISH:~/Desktop/iitsem7/BTP/sem7$ python code/BtechProject/ver2/getPreReAvg.py stackOverflowData/train_results/surveyQAEval.txt
# Prec: 10 : 0.11 3 : 0.26 5 : 0.168
# Rec: 10 : 0.417333333333 3 : 0.285666666667 5 : 0.309
