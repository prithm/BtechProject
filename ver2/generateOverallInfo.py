import pickle
import sys

if __name__ == '__main__':
	allinfo = {}
	indmap = {}
	cnt = 0
	with open(sys.argv[1], 'r') as f:
		for line in f:
			l = line.strip('\n').strip()
			post_id = l.split(';')[0]
			indmap[cnt] = post_id
			cnt += 1
			vec = l.split(';')[1].strip().split()
			tfidf = {}
			for v in vec:
				ind = int(v.split(':')[0])
				score = float(v.split(':')[1])
				tfidf[ind] = score
			allinfo[post_id] = {}
			allinfo[post_id]['tfidf'] = tfidf

	cnt = 0		
	with open(sys.argv[2], 'r') as f:
		for line in f:
			l = line.strip('\n').strip()
			post_id = indmap[cnt]
			allinfo[post_id]['terms'] = l
			cnt += 1			


	pickle.dump(allinfo, open(sys.argv[3], 'wb'))