"""Create Users' Map"""
from User import *
from Daily import Daily
import os
from os import listdir
from os.path import isfile,join
import sys
import pickle
import gc
import multiprocessing as mp
from functools import reduce
import time


class UserDict():
	def __init__(self, filePath = "dataset"):
		self.filePath = filePath

	#do not read in hidden files
	def listdir_nohidden(self,path):
	    for f in os.listdir(path):
	        if not f.startswith('.'):
	            yield f

	def save_obj(self,obj, name):
	    with open('userdb/'+ name + '.pkl', 'wb') as f:
	        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	def load_obj(self,name):
	    with open('userdb/' + name + '.pkl', 'rb') as f:
	        return pickle.load(f)

	def pre_process(self):
		fileList = self.listdir_nohidden(self.filePath)
		pre_process = [f for f in fileList]
		return pre_process

	def process_list(self,pre_process_list,q):
		process_list = []
		append = process_list.append
		for idx, file in enumerate(pre_process_list):
			#get file path name
			file = join(self.filePath,file)
			append(Daily(file))
			print("{0:.1f}%\r ".format(float((idx+1)/len(pre_process_list)*100)),end='')
			sys.stdout.flush()
		q.put(process_list)
		gc.collect()


	def _add_attr(self,userObj):
		userObj.add_visit(event_time[idx])
		userObj.add_ip(ip_add[idx])
		userObj.add_item(item_id[idx])

	def _create_user_map(self,daily,user_dict):
		for idx, user_id in enumerate(daily.identity_dict.get('identity_id')):
			if user_id != 'guest':
				event_time = daily.identity_dict.get('time')
				ip_add = daily.identity_dict.get('ip_add')
				item_id = daily.identity_dict.get('item_id')
				try:
					temp = user_dict[user_id]
					try:
						temp.add_visit(event_time[idx])
						temp.add_ip(ip_add[idx])
						temp.add_item(item_id[idx])
					except IndexError:
						print('Index Error')
					except:
						print('Unkown Error')
				except KeyError:
					temp = User(user_id)
					try:
						temp.add_visit(event_time[idx])
						temp.add_ip(ip_add[idx])
						temp.add_item(item_id[idx])
						user_dict[user_id] = temp
					except IndexError:
						print('Index Error')
					except:
						print('Unkown Error')
			

		gc.collect()

	def create_user_map(self,daily_list):
		print("Creating user map")
		jobs = []
		append = jobs.append
		user_dict = mp.Manager().dict()
		c = 0
		for idx, d in enumerate(daily_list):
			p = mp.Process(target = self._create_user_map, args=(d,user_dict,))
			p.start()
			append(p)
			c+=1 
			if c >= 8 :
				jobs[0].join()
				jobs.pop(0)
				c -=1 
			print("{0:.1f}% \r".format(float((idx+1)/len(daily_list))*100), end='')
			sys.stdout.flush()

		for j in jobs:
			j.join()

		self.save_obj(user_dict,'user_dict')






	def main(self,num_of_thread):
		pre_process_list = self.pre_process()
		q = mp.Queue()
		daily_list=[]
		jobs = []
		jappend = jobs.append
		for idx in range(0,len(pre_process_list),num_of_thread):
			task = pre_process_list[idx:idx+num_of_thread]
			p = mp.Process(target = self.process_list, args = (task,q))
			p.start()
			jappend(p)
		
		for _ in jobs:
			daily_list+=q.get()

		for j in jobs:
			j.join()

		print('')
		del jobs
		gc.collect()


		self.create_user_map(daily_list)
		gc.collect()

		


	


if __name__ == '__main__':
	start_time = time.time()
	ud = UserDict("dataset")
	ud.main(8)
	gc.collect()
	print('')
	print("{0:.5f}s".format(time.time()-start_time))




