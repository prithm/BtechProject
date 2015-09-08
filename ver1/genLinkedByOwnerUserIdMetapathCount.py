import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genLinkedByOwnerUserIdMetapathCount(input, fileout):
	ownerQuestionCountFile = open(input, 'r')
	linkedByOwnerUserIdMetapathCount = 0
	for line in ownerQuestionCountFile:
		temp = int(line.strip().split(' ')[1])
		linkedByOwnerUserIdMetapathCount += (temp*(temp-1))/2
	
	linkedByOwnerUserIdMetapathCountFile = open(fileout, 'w')		
	linkedByOwnerUserIdMetapathCountFile.write(str(linkedByOwnerUserIdMetapathCount) + '\n')
	linkedByOwnerUserIdMetapathCountFile.close()


def main():
	genLinkedByOwnerUserIdMetapathCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()