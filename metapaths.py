import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             

import sys

class Posts:
	def __init__(self,_postJson):
		self.postJson = postJson

def parsePostXML(input):
	postList = []
	tree = ET.parse(input)
	posts = tree.getroot()
	cnt = 0
	for post in posts:
		postJson = post.attrib
		print postJson
		postList.append(postJson)
		cnt += 1
		if cnt == 2:
			break
	return postList

def main():
	parsePostXML(sys.argv[1])

if __name__ == '__main__':
	main()