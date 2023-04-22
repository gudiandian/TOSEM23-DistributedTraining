import json
import os
import sys

if __name__ == '__main__':
	path1 = sys.argv[1]
	path2 = sys.argv[2]
	url_list = []
	with open(path1, 'r') as file:
		data = json.load(file)
		for i in data['items']:
			url_list.append(i['html_url'])
	print("numbers:", len(url_list))
	with open(path2, 'a+') as f:
		for i in url_list:
			f.write(i)
			f.write('\n')