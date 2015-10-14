import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import pickle


#tag
def genTags(input, picklefile):
	cnt = 0
	tags = []
	with open(input,'r') as f:
		for line in f: 
			cnt += 1
			if cnt < 3:
				continue
			try:
				post = ET.fromstring(line.strip().strip('\n').strip())
			except Exception as e:
				continue
			tagName = post.get('TagName')
			tags.append(tagName)
			if cnt % 1000 == 0:
				print cnt
	pickle.dump( tags, open(picklefile, "wb") )

def main():
	genTags(sys.argv[1], sys.argv[3])

if __name__ == '__main__':
	main()
