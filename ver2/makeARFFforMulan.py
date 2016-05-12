import sys
import pickle

if __name__ == '__main__':
	posts = pickle.load( open(sys.argv[1],'rb') )
	overall = pickle.load( open(sys.argv[2],'rb') )
	tagset = pickle.load( open(sys.argv[3],'rb') )
	wordset = set()
	with open(sys.argv[4], 'r') as f:
		for line in f:
			wordset.add(line.strip('\n'))

	wfile = open(sys.argv[5],'w')
	wfile.write('@relation tagcombine\n\n')		
	wfile.flush()
	
	cnt = 0
	for word in wordset:
		wfile.write('@attribute ' + 'Term' + str(cnt) + ' numeric\n')
		wfile.flush()
		cnt += 1

	for tag in tagset:
		wfile.write('@attribute ' + tag + ' {0,1}\n')
		wfile.flush()

	wfile.write('\n')
	wfile.write('@data\n')
	wfile.flush()

	cnt = 0
	for post in posts:
		if cnt % 1000 == 0:
			print cnt
			sys.stdout.flush()
		tags = post['tags'].strip('<').strip('>').split('><')
		terms = overall[post['Id']]['terms'].split()
		out = ''
		for word in wordset:
			if word in terms:
				out += '1.0,'
			else:
				out += '0.0,'
		for tag in tagset:
			if tag in tags:
				out += '1,'
			else:
				out += '0,'
		wfile.write(out[:-1]+'\n')
		wfile.flush()
		cnt += 1

	wfile.close()		