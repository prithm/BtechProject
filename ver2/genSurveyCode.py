import sys
import pickle
from bs4 import BeautifulSoup
import re

if __name__ == '__main__':
	testPosts = pickle.load(open(sys.argv[1],'rb'))
	# wfile = open(sys.argv[2], 'w')
	cnt = 0
	out = "\
	function createForm() { \n "
	for post in testPosts:
		if cnt %10 == 0:
			out += "var title = 'Survey_vc_" + str(cnt/10 + 1) + "'; \n \
			var description = 'This is survey to evaluate the prediction of tags given the entry text such as in stackoverflow.com. Tick the tags which you think are most relevant to the question. Mark one or more tags.'; \n \
			var form = FormApp.create(title).setDescription(description).setConfirmationMessage('Thanks for responding!'); \n"
		# print post.keys()
		body =  BeautifulSoup(post['Body']).get_text()
		body = re.sub(r'\n','. ',body)
		body = re.sub(r"'","\\\\'",body)
		body = re.sub(r'"','\\\\"',body)
		body = body.encode("utf-8")
		post['Body'] = body
		post['expected'] = post['expected'][:5]
		post['predicted_by_Hybrid_Matching'] = post['predicted_by_Hybrid_Matching'][:5]
		post['final_Recommended_Tags'] = post['final_Recommended_Tags'][:5]
		tot = set()
		for tag in post['expected']:
			tot.add(tag.strip())
		for tag in post['predicted_by_Hybrid_Matching']:
			tot.add(tag.strip())
		for tag in post['final_Recommended_Tags']:
			tot.add(tag.strip())

		totList = list(tot)
		outQ = ""
		outQ += "var item = form.addCheckboxItem(); \n"
		outQ += "item.setTitle('"+ body + "') \n"
		outQ += ".setChoices([ \n "
		for tag in totList:
			outQ += "item.createChoice('" + tag + "'), \n"
		outQ += "]) \n" 
		out += outQ
		cnt += 1

	out += "} \n"
	print out

# "function createForm() { \
# 	for(var id=1; id<=1; id++){ \
# 		var title = 'Survey_'+id; \
# 		var description = 'This is survey to evaluate the prediction of tags given the entry text such as in stackoverflow.com. The entered text is provided along with the predicted tags by 3 methods. Each option represents the tags predicted by one method. Choose the method that predicts most relevant tags for each question.'; \
# 		var form = FormApp.create(title).setDescription(description).setConfirmationMessage('Thanks for responding!'); \
# 		var files = DriveApp.getFilesByName('TestSetPostsForUserSurvey.txt'); \
# 		if (files.hasNext()) Logger.log('YES'); \
# 		else Logger.log('NO'); \
# 		while (files.hasNext()) { \
# 			var file = files.next(); \
# 			var docContent = file.getAs('text/plain'); \
# 			var lines =  docContent.getDataAsString().split('\n'); \
# 			Logger.log(lines[0]); \
# 			for(var i = 10*(id-1); i<10*id; i++){ \
# 				var s = lines[i]; \
# 				var jsonObj = JSON.parse(s); \
# 				Logger.log(i); \
# 				form.addMultipleChoiceItem() \
# 				.setTitle(jsonObj['Body'])  \
# 				.setChoiceValues([jsonObj['expected'],jsonObj['predicted_by_Hybrid_Matching'],jsonObj['final_Recommended_Tags']]); \
# 			} \
# 			break; \
# 		} \
# 	} \
# }"