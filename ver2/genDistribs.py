import pickle
import sys

if __name__ == '__main__':
	posts = pickle.load(open(sys.argv[1], 'rb'))
	wfile = open(sys.argv[2], 'w')
	key = sys.argv[3]

	for post in posts:
		if key in post.keys() and post[key] != None:
			wfile.write(str(post[key])+'\n')
		else:
			wfile.write('-1\n')
			print 'Error'

	wfile.flush()
	wfile.close()	
		