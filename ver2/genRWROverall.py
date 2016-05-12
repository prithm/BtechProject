import sys
import os
import pickle

tags = set()
print "Initialising"
tagTagProb = pickle.load(open(sys.argv[2], 'rb'))
print 'Initialised'
print 'Graph making...'
for tag1,valueDict in tagTagProb.items():
	for tag2,wt in valueDict.items():
		tags.add(tag1)
		tags.add(tag2)
print 'Graph made'
tagList = list(tags)		



if __name__ == '__main__':
	tot = len(tags)
	mul = 2400
	fac = tot/mul
	for i in xrange(0,fac+1):
		if i*mul >= tot:
			break
		command = 'nohup python ' + sys.argv[1] + ' ' + sys.argv[2] + ' ' +  str(i) + ' ' + str(i*mul) + ' ' + str(min(i*mul+mul,len(tags))) + ' &'
		print command
		os.system(command)	

