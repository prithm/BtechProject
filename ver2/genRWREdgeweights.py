import networkx as nx
import sys

def main():

	G = nx.DiGraph()
	tags = set()
	zeroDict = {}
	with open(sys.argv[1], 'r') as f:
		for line in f:
			lineParts = line.strip('\n').strip().split(' ')
			v = lineParts[0]
			u = lineParts[1]
			wt = float(lineParts[2])
			G.add_edge(u, v, weight=wt)
			tags.add(u)
			tags.add(v)
			zeroDict[u] = 0
			zeroDict[v] = 0

	nx.write_gml(G,sys.argv[2])

	f = open(sys.argv[3], 'w')
	print len(tags)
	cnt = 0
	for tag in tags:
		cnt += 1
		if cnt%100 == 0:
			print cnt
		tempDict = zeroDict
		tempDict[tag] = 1
		out = nx.pagerank_scipy(G, personalization = tempDict)
		for tag2 in out.keys():
			out2 = tag2 + ' ' + tag + ' ' + str(out[tag2]) + '\n'
			f.write(out2)
		tempDict[tag] = 0
		#break


if __name__ == '__main__':
	main()	

