import pickle
import sys

if __name__ == '__main__':
	
	userIds = set()

	with open(sys.argv[1], 'r') as f:
		for line in f:
			userIds.add(line.strip('\n'))

	userCnt = 0
	userMaxCnt = len(userIds)

	with open(sys.argv[2], 'r') as f:
		cnt = 0
		for line in f:
			cnt += 1
			if cnt < 3:
				continue
			try:
				user = ET.fromstring(line.strip().strip('\n').strip())
			except Exception as e:
				continue

			userId = user.get('Id')
			if userId in userIds:
				tempDict['Id'] = user.get('Id')
				tempDict['Reputation'] = user.get('Reputation')
				tempDict['CreationDate'] = user.get('CreationDate')
				tempDict['DisplayName'] = user.get('DisplayName')
				tempDict['LastAccessDate'] = user.get('LastAccessDate')
				tempDict['WebsiteUrl'] = user.get('WebsiteUrl')
				tempDict['Location'] = user.get('Location')
				tempDict['AboutMe'] = user.get('AboutMe')
				tempDict['Views'] = user.get('Views')
				tempDict['UpVotes'] = user.get('UpVotes')
				tempDict['DownVotes'] = user.get('DownVotes')
				tempDict['EmailHash'] = user.get('EmailHash')
				tempDict['AccountId'] = user.get('AccountId')
				tempDict['Age'] = user.get('Age')
				userInfo[userId] = tempDict
				userCnt += 1
				if userCnt >= userMaxCnt:
					break

	pickle.dump(userInfo, open(sys.argv[3],'wb'))	