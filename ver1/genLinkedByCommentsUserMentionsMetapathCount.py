import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genLinkedByCommentsUserMentionsMetapathCount(input, fileout):
	commentsUserMentionsFile = open(input, 'r')
	linkedByCommentsUserMentionsMetapathCount = 0
	for line in commentsUserMentionsFile:
		linkedByCommentsUserMentionsMetapathCount += 1
	
	linkedByCommentsUserMentionsMetapathCountFile = open(fileout, 'w')		
	linkedByCommentsUserMentionsMetapathCountFile.write(str(linkedByCommentsUserMentionsMetapathCount) + '\n') 
	linkedByCommentsUserMentionsMetapathCountFile.close()

def main():
	genLinkedByCommentsUserMentionsMetapathCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()