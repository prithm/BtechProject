import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genLinkedByTagsMetapathCount(input, fileout):
	questionTagCountFile = open(input, 'r')
	linkedByTagsMetapathCount = 0
	for line in questionTagCountFile:
		temp = int(line.strip().split(' ')[1])
		linkedByTagsMetapathCount += (temp*(temp-1))/2
	
	linkedByTagsMetapathCountFile = open(fileout, 'w')		
	linkedByTagsMetapathCountFile.write(str(linkedByTagsMetapathCount) + '\n')
	linkedByTagsMetapathCountFile.close()

def main():
	genLinkedByTagsMetapathCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()