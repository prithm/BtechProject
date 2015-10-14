import sys
import pickle
import difflib
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
	print 'initialising'
	posts = pickle.load( open(sys.argv[1], "rb") )
	print 'initialised'
	out = set()
	cnt = 0;
	for post in posts:
		cnt += 1
		if cnt%10000 == 0:
			print cnt
		if int(post['postTypeId']) != 1:
			continue
		tags = post['tags'].replace('<', ' ').replace('>', ' ').strip().split()
		for tag in tags:
			out.add(tag)
	print len(out)	
	pickle.dump( list(out), open(sys.argv[2], "wb") )
