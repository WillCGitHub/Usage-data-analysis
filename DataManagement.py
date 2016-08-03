"""Manage and update data"""
from User import *
import os
import csv
import sys
import gc
import numpy as np
import pandas as pd
import pickle
from User import *


def listdir_nohidden_file(path):
	for f in os.listdir(path):
		if not f.startswith('.'):
			yield f

def save_obj(obj, file_name, folder_name ):
	path_name = "".join([folder_name,'/',file_name,'.pkl'])
	with open(path_name, 'wb') as f:
		pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(file_name,folder_name):
	path_name = "".join([folder_name,'/',file_name,'.pkl'])
	with open(path_name, 'rb') as f:
		return pickle.load(f)

def initial_setup():
	"""Only need to be used in the inital set up """
	dataset = os.path.join(script_dir,'dataset')
	all_files = listdir_nohidden_file(dataset)

	list_of_files = np.array([f for f in all_files])
	save_obj(list_of_files,'list_of_files',data_manage_folder)

def check_new_files(file_name,file_folder):
	list_of_all_files = load_obj(file_name,file_folder)
	set_of_all_files = set(list_of_all_files)
	files_gen = listdir_nohidden_file('dataset')
	unprocessed = []
	for f in files_gen:
		if f not in set_of_all_files:
			unprocessed.append(f)
	return unprocessed,list_of_all_files

def update_userdb(new_files_list,entire_list):
	print('Updating user database...')
	if len(new_files_list) == 0:
		print('No new file needs to be updated.')
	else:
		print('Loading...')
		user_dict = load_obj('user_dict','userdb')
		print('Updating...')
		for idx,f in enumerate(new_files_list):
			f_path = "".join(['dataset/',f])
			df = pd.read_csv(f_path,header = 0)
			df.dropna()
			if len(df.columns) != 10:
				continue
			for row in df.itertuples():
				if row[2] != 'guest':
					userObj = user_dict.get(row[2])
					if userObj is not None:
						userObj.add_ip(row[5])
						userObj.add_visit(row[3])
						userObj.add_item(row[7])
						userObj.add_source(row[10])
					else:
						userObj = User(row[2])
						userObj.add_ip(row[5])
						userObj.add_visit(row[3])
						userObj.add_item(row[7])
						userObj.add_source(row[10])
						user_dict[row[2]] = userObj
			print("{0:.3f}%\r".format((idx+1)*100/len(new_files_list)),end='')
			sys.stdout.flush()
			entire_list = np.append(entire_list,f)
		print('\nFinish updating...\nSaving...')
		save_obj(user_dict,'user_dict','userdb')
		save_obj(entire_list,'list_of_files',data_manage_folder)
		gc.collect()
		print('Done')





script_dir = os.path.dirname("__file__")
data_manage_folder = '.data_manage'
abs_file_path = os.path.join(script_dir,data_manage_folder)

"""If the directory does not exist, create it """
if not os.path.isdir(abs_file_path):
	try:
		os.makedirs(abs_file_path)
	except OSError as e:
		if e.errno != 17:
			raise
		pass

new_files_list, entire_list = check_new_files('list_of_files',data_manage_folder)
update_userdb(new_files_list,entire_list)

if __name__ == '__main__':
	pass





