import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genTagPostCount(postInfo, postType, fileout):
	tagPostCount = {}
	postInfoFile = open(postInfo, 'r')
	cnt = 0
	for line in postInfoFile:
		cnt += 1
		if cnt % 1000 == 0:
			print cnt
		lineParts = line.strip().strip('\n').split(' ')
		postTypeId = int(lineParts[0])
		tags = lineParts[4].replace('<', ' ').replace('>', ' ').strip().split()
		if postTypeId == postType:
			for tag in tags:
				if tag not in tagPostCount.keys():
					tagPostCount[tag] = 1
				else: 
					tagPostCount[tag] += 1
	postInfoFile.close()

	tagPostCountOutputFile = open(fileout, 'w')
	for tag, count in tagPostCount.items():
		tagPostCountOutputFile.write(tag + ' ' + str(count) + '\n')

	tagPostCountOutputFile.close()

def main():
	genTagPostCount(sys.argv[1], int(sys.argv[2]), sys.argv[3])
	
if __name__ == '__main__':
	main()