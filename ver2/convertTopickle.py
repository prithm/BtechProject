import sys
import pickle

if __name__ == '__main__':
	b = []
	with open(sys.argv[1], 'r') as f:
		for line in f:
			b.append( eval(line.strip('\n')) )
	pickle.dump( b, open(sys.argv[2], 'wb') )
