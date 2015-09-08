import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def genLinkedByPostLinksMetapathCount(input, fileout):
	postLinkInfoFile = open(input, 'r')
	linkedByPostLinksMetapathCount = {}
	for line in postLinkInfoFile:
		linkType = line.strip().split(' ')[2]
		if linkType not in linkedByPostLinksMetapathCount.keys():
			linkedByPostLinksMetapathCount[linkType] = 0
		linkedByPostLinksMetapathCount[linkType] += 1
	
	linkedByPostLinksMetapathCountFile = open(fileout, 'w')		
	for linkType,count in linkedByPostLinksMetapathCount.items():
		linkedByPostLinksMetapathCountFile.write(linkType + ' ' + str(count) + '\n') 

	linkedByPostLinksMetapathCountFile.close()

def main():
	genLinkedByPostLinksMetapathCount(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()