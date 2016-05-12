import sys
import pickle


if __name__ == '__main__':
	temp = {}
	prefix = sys.argv[1]
	end = int(sys.argv[2])
	cnt  = 0
	for i in xrange(0, end):
		file_name = prefix + '_' + str(i) + '.txt'
		print file_name
		with open(file_name, 'r') as f:
			for line in f:
				temp_d = eval(line.strip('\n'))
				key = temp_d.keys()[0]
				#print key
				val = temp_d[key]
				temp[key] = val
				cnt += 1
				if cnt%100 == 0:
					print cnt
				#break
		#break
	pickle.dump(temp, open(sys.argv[3], 'wb'))
