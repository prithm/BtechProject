import sys

if __name__ == '__main__':
	initset = set()
	with open(sys.argv[1], 'r') as f:
		for line in f:
			initset.add( int(line.strip('\n')) )
	print 'Init Done' , len(initset)
	sys.stdout.flush()

	wfile = open(sys.argv[3], 'w')
	cnt = 0
	with open(sys.argv[2], 'r') as f:
		for line in f:
			lineParts = line.strip('\n').split(' ')
			postType = int(lineParts[0])
			postId = int(lineParts[2])
			parentId = int(lineParts[3])
			if cnt % 1000:
				print cnt
				sys.stdout.flush()
			if postType == 1:
				cnt += 1
				if postId in initset:
					wfile.write( str (postId) + '\n')
			elif postType == 2:
				cnt += 1
				if parentId in initset:
					wfile.write( str (postId) + '\n')
	wfile.flush()
	wfile.close()