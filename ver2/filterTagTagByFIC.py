import sys
import pickle

if __name__ == '__main__':
	tag_tag = pickle.load( open(sys.argv[1], 'rb') )
	tag_tag_filter = {}
	for tag1 in tag_tag.keys():
		temp = {}
		for tag2 in tag_tag[tag1].keys():
			if tag_tag[tag1][tag2] > 0.01:
				temp[tag2] = tag_tag[tag1][tag2]
		if len(temp.keys()) > 0:
			sorted_x = sorted(temp.items(), key=lambda x:x[1], reverse= True)
			sorted_x = sorted_x[:10]
			tag_tag_filter[tag1] = {}
			for tag2,prob in sorted_x:
				tag_tag_filter[tag1][tag2] = prob

	pickle.dump(tag_tag_filter, open('P_tag_tag_filtered.pickle','wb'))			
