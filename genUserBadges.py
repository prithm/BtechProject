import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup             
import sys

def printOwnerBadges(input, fileout):		
	tree = ET.parse(input)
	rawBadges = tree.getroot()
	ownerBadgesOutputFile = open(fileout, 'w')
	for rawBadge in rawBadges:
		badge = rawBadge.attrib
		userId = badge.get('UserId')
		badgeName = badge.get('Name')
		if userId is not None and badgeName is not None:
			ownerBadgesOutputFile.write(userId + ' ' + badgeName + '\n')		



def main():
	printOwnerBadges(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
	main()

