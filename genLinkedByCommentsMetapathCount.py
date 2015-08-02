import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genLinkedByCommentsMetapathCount(input, fileout):
	commentsIdInfoFile = open(input, 'r')
	linkedByCommentsMetapathCount = 0
	for line in commentsIdInfoFile:
		linkedByCommentsMetapathCount += 1
	
	linkedByCommentsMetapathCountFile = open(fileout, 'w')		
	linkedByCommentsMetapathCountFile.write(str(linkedByCommentsMetapathCount) + '\n') 
	linkedByCommentsMetapathCountFile.close()

def main():
	genLinkedByCommentsMetapathCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()