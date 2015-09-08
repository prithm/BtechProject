import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import sys
import re

#commentIdInfo - owner commentId postId score 
#commentBodyInfo - commentId Body
#commentMention - commentId <mention1> <mention2> ...
def genCommentsInfo(input, commentIdInfo, commentBodyInfo, commentMention):
	tree = ET.parse(input)
	rawComments = tree.getroot()
	commentIdInfoOutputFile = open(commentIdInfo, 'w')
	commentBodyInfoOutputFile = open(commentBodyInfo, 'w')
	commentMentionOutputFile = open(commentMention, 'w')
	userMentionRegex = re.compile('@(\w*)')
	
	for rawComment in rawComments:
		comment = rawComment.attrib
		commentId = comment.get('Id')
		commentOnId = comment.get('PostId')
		commenterId = comment.get('UserId')
		commentScore = comment.get('Score')
		commentBody = BeautifulSoup(comment.get('Text')).get_text().encode('utf-8')

		if commentId is not None and commentOnId is not None and commenterId is not None and commentScore is not None and commentBody is not None:
			commentIdInfoOutputFile.write(commenterId + ' ' + commentId + ' ' + commentOnId + ' ' + commentScore + '\n')
			commentBodyInfoOutputFile.write(commentId + ' ' + commentBody + '\n')
			
			userMentions = userMentionRegex.findall(commentBody)
			if len(userMentions) > 0:
				for userMention in userMentions:
					if userMention.strip() != '':
						commentMentionOutputFile.write(commentId + ' ' + userMention.strip() + '\n')	
	

	commentIdInfoOutputFile.close()
	commentBodyInfoOutputFile.close()
	commentMentionOutputFile.close()


def main():
	genCommentsInfo(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


if __name__ == '__main__':
	main()