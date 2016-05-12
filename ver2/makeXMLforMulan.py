import sys
import pickle

if __name__ == '__main__':
	posts = pickle.load( open(sys.argv[1],'rb') )
	# overall = pickle.load( open(sys.argv[2],'rb') )
	# wordlist = set()
	# with open(sys.argv[3], 'r') as f:
	# 	for line in f:
	# 		wordlist.add(line.strip('\n'))

	tagset = set()
	cnt = 0
	for post in posts:
		if cnt % 1000 == 0:
			print cnt
			sys.stdout.flush()
		tags = post['tags'].strip('<').strip('>').split('><')
		for tag in tags:
			tagset.add(tag)
		cnt += 1	

	pickle.dump(tagset, open(sys.argv[2],'wb')) 


	wfile = open(sys.argv[3],'w')
	wfile.write('<?xml version="1.0" encoding="utf-8"?>\n<labels xmlns="http://mulan.sourceforge.net/labels">\n')
	wfile.flush()

	for tag in tagset:
		wfile.write('<label name="' + tag + '"></label>\n')
		wfile.flush()

	wfile.write('</labels>\n')
	wfile.flush()
	wfile.close()
