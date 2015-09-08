import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys

#Id Reputation Views UpVotes DownVotes Age AccountId DisplayName
def genUserInfo(input, fileout):

	tree = ET.parse(input)
	rawUsers = tree.getroot()
	userInfoOutputFile = open(fileout, 'w')
	
	for rawUser in rawUsers:
		user = rawUser.attrib
		userId = user.get('Id')
		userReputation = user.get('Reputation')
		userDisplayName = user.get('DisplayName').encode('utf-8')
		userViews = user.get('Views')
		userUpVotes = user.get('UpVotes')
		userDownVotes = user.get('DownVotes')
		userAge = user.get('Age')
		userAccountId = user.get('AccountId')
		if userId is not None and userId != '-1' and userReputation is not None \
		and userDisplayName is not None and userViews is not None and userUpVotes is not None \
		and userDownVotes is not None and userAge is not None and userAccountId is not None:

			userInfoOutputFile.write(\
			userId + ' ' + \
			userReputation + ' ' + \
			userViews + ' ' + \
			userUpVotes + ' ' + \
			userDownVotes + ' ' + \
			userAge + ' ' + \
			userAccountId + ' ' + \
			userDisplayName + '\n'			
			)

	userInfoOutputFile.close()


def main():
	genUserInfo(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
	main()
