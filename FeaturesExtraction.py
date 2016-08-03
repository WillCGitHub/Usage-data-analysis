from User import *
import pickle
from collections import Counter
import re
import sys
from statistics import mean
import os
import pandas as pd
from ua_parser import user_agent_parser
import csv
import numpy as np




def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('userdb/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def listdir_nohidden(path):
	    for f in os.listdir(path):
	        if not f.startswith('.'):
	            yield f


def user_agent_parse_dict():
	filePath = "dataset"
	fileList = list(listdir_nohidden(filePath))
	browser_dict = dict()
	os_dict = dict()

	browser_c = 0
	os_c = 0
	seen = set()
	for idx, f in enumerate(fileList):
		f = "".join([filePath,'/',f])
		try:
			df = pd.read_csv(f,header = 0,dtype = str)
			if len(df.columns) == 10:
				for row in df.itertuples():
					ua = row[6]
					if ua not in seen:
						parsed_browser = user_agent_parser.ParseUserAgent(ua)['family']
						parsed_os = user_agent_parser.ParseOS(ua)['family']
						if browser_dict.get(parsed_browser) is None:
							browser_dict[parsed_browser] = browser_c
							browser_c+=1

						if os_dict.get(parsed_os) is None:
							os_dict[parsed_os] = os_c
							os_c+=1

						seen.add(ua)

		except:
			pass
		print("{0:.3f}%\r".format((idx+1)*100/len(fileList)),end='')
		sys.stdout.flush()

	print(len(browser_dict))
	print(len(os_dict))
	save_obj(browser_dict,'browser_dict')
	save_obj(os_dict,'os_dict')

def parse_user_agent(ua):
	parsed_browser = user_agent_parser.ParseUserAgent(ua)['family']
	parsed_os = user_agent_parser.ParseOS(ua)['family']
	return (parsed_browser,parsed_os)

def feature_hash(filePath, list_of_file, feature_dict, 
				dict_name, column):
	counter = 0
	seen = set()
	for idx, f in enumerate(list_of_file):
		f = "".join([filePath,'/',f])
		try:
			df = pd.read_csv(f,header = 0,dtype = str)
			if len(df.columns) == 10:
				for row in df.itertuples():
					feature = row[column]
					if feature not in seen:
						if feature_dict.get(feature) is None:
							feature_dict[feature] = counter
							counter+=1

						seen.add(feature)

		except:
			pass
		print("{0:.3f}%\r".format((idx+1)*100/len(fileList)),end='')
		sys.stdout.flush()

	print('')
	print(len(feature_dict))
	print('')

	save_obj(feature_dict,dict_name)

def export_feature():
	print("load db")
	ud = load_obj('user_dict')
	item_cate_dict = load_obj('item_cate_dict')
	browser_dict = load_obj('browser_dict')
	os_dict = load_obj('os_dict')
	unique_ip_dict = load_obj('unique_ip_dict')
	source_dict = load_obj('source_dict')
	licence_type_dict = load_obj('licence_type_dict')
	features = []
	labels = []

	output_f = open ('result/cleaned_data.csv','w')
	writer = csv.writer(output_f,delimiter=',')
	writer.writerow(['profile code',
						'ip',
						'item code',
						'browser type',
						'OS type',
						'source',
						'licence_type'])
	output_f.close()

	filePath = "dataset"
	fileList = list(listdir_nohidden(filePath))

	for idx, f in enumerate(fileList):
		f = "".join([filePath,'/',f])
		try:
			df = pd.read_csv(f,header = 0,dtype = str)
			if len(df.columns) == 10:
				for row in df.itertuples():
					uid = row[2]
					if uid != 'guest':
						profile = ud.get(uid)
						profileC = profile.identity_dict.get('category')
						if (profileC is not None) and (profileC != '100'):
							if (uid != 'guest') and profileC is not None:
								ua_info = parse_user_agent(row[6])
								output_f = open ('result/cleaned_data.csv','a')
								writer = csv.writer(output_f,delimiter=',')
								writer.writerow([profileC, 
												unique_ip_dict.get(row[5]),
												item_cate_dict.get(row[7].split('-')[0]),
												browser_dict.get(ua_info[0]),
												os_dict.get(ua_info[1]),
												source_dict.get(row[10]),
												licence_type_dict.get(row[9])])
								output_f.close()
		except:
			pass


		print("{0:.3f}%\r".format((idx+1)*100/len(fileList)),end='')
		sys.stdout.flush()
	
	output_f.close()


if __name__ == '__main__':

	"""
	filePath = "dataset"
	fileList = list(listdir_nohidden(filePath))
	source_dict = dict()
	licence_type_dict = dict()
	feature_hash(filePath,fileList,source_dict,'source_dict',10)
	feature_hash(filePath,fileList,licence_type_dict,'licence_type_dict',9)
	"""


	df = pd.read_csv('result/cleaned_data.csv',header = 0)
	df = df.dropna()
	X = df.ix[:,[1,3,4]]
	
	y = df['profile code'] #labels
	print('')


	print('train')
	
	from sklearn.cross_validation import train_test_split
	X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = .5)

	from sklearn.neighbors import KNeighborsClassifier

	clf = KNeighborsClassifier(n_neighbors = 10, algorithm = 'ball_tree',weights='distance' )
	clf.fit(X_train,y_train)
	predictions = clf.predict(X_test)

	from sklearn.metrics import accuracy_score
	print(accuracy_score(y_test,predictions))
	




