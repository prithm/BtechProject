import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genLinkedByAnswerMetapathCount(input, fileout):
	ownerAnswerCountFile = open(input, 'r')
	linkedByAnswerMetapathCount = 0
	for line in ownerAnswerCountFile:
		linkedByAnswerMetapathCount += int(line.strip().split(' ')[1])
	
	linkedByAnswerMetapathCountFile = open(fileout, 'w')		
	linkedByAnswerMetapathCountFile.write(str(linkedByAnswerMetapathCount) + '\n')
	linkedByAnswerMetapathCountFile.close()

def main():
	genLinkedByAnswerMetapathCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()