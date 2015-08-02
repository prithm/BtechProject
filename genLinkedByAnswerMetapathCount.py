import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genAnswerCount(input, fileout):
	postInfoFile = open(input, 'r')
	answerCount = 0
	for line in postInfoFile:
		if line.strip().split(' ')[0] == '2':
			answerCount += 1

	answerCountFile = open(fileout, 'w')		
	answerCountFile.write(str(answerCount) + '\n')
	answerCountFile.close()


def main():
	genAnswerCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()