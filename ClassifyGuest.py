import pandas as pd
import numpy as np
from FeaturesExtraction import parse_user_agent
import sys
import operator
import pickle
from sklearn.neighbors import KNeighborsClassifier
from collections import Counter
from CategoryDict import category_dict
import os



class ClassifyGuest():
	def __init__(self,file_name,):
		print("load db")
		self.file_name = file_name
		#self.num_of_results = num_of_results
		self.browser_dict = self.load_obj('browser_dict')
		self.browser_dict_len = len(self.browser_dict)
		self.os_dict = self.load_obj('os_dict')
		self.os_dict_len = len(self.os_dict)
		self.unique_ip_dict = self.load_obj('unique_ip_dict')
		self.unique_ip_dict_len = len(self.unique_ip_dict)
		self.script_dir = os.path.dirname("__file__")

	def load_obj(self, name):
	    with open('userdb/' + name + '.pkl', 'rb') as f:
	        return pickle.load(f)
	def save_obj(self,obj, name):
	    with open('userdb/'+ name + '.pkl', 'wb') as f:
	        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

	def extract_features(self,row):
		ip = row[5]
		user_agent = parse_user_agent(row[6])
		browser_type = user_agent[0]
		os_type = user_agent[1]
		num_ip = self.unique_ip_dict.get(ip)
		if num_ip is None:
			self.unique_ip_dict_len+=1
			num_ip = self.unique_ip_dict_len 
			
		num_browser = self.browser_dict.get(browser_type)
		if num_browser is None:
			self.browser_dict_len+=1
			num_browser = self.browser_dict_len

		num_os = self.os_dict.get(os_type)
		if num_os is None:
			self.os_dict_len +=1 
			num_os = self.os_dict_len

		return np.array([num_ip,num_browser,num_os])

	def weight(self,list_of_result):
		co = Counter(list_of_result).most_common(1)
		return str(co[0][0])

	def train(self):
		train_data_folder = 'TrainData'
		train_data_path = os.path.join(self.script_dir,train_data_folder,'cleaned_data.csv')
		df = pd.read_csv(train_data_path,header = 0)
		df = df.dropna()
		X_model = df.ix[:,[1,3,4]]

		y = df['profile code'] #labels

		print('train')
		self.clf = KNeighborsClassifier(n_neighbors = 10, algorithm = 'ball_tree',weights='distance' )
		self.clf.fit(X_model,y)
		self.save_obj(self.clf,'fitted_KNN')


	def predict(self):
		X_guest = []
		X_append = X_guest.append

		guest_ip = []
		ip_append = guest_ip.append

		"""Read in data """
		for f in self.file_name:
			f_name = str(f).split("/")[-1]
			df = pd.read_csv(f,header=0)
			df.dropna()
			num_of_rows = df.shape[0]

			
			for idx, row in enumerate(df.itertuples()):
				if row[2] == 'guest':
					f = self.extract_features(row)
					X_append(f)
					ip_append(row[5])

				print("Loading {0}: {1:.3f}%\r".format(f_name,((idx+1)*100/num_of_rows)),end='')
				sys.stdout.flush()
			print('')

		"""Convert to DataFrame """
		X_guest = np.array(X_guest)
		guest_ip = np.array(guest_ip)
		X_guest = pd.DataFrame(X_guest, columns = ['ip','browser','os'])
		print("\npredict")
		predictions = self.clf.predict(X_guest)
		
		"""clear up results """
		result = np.vstack((guest_ip,predictions))
		result = np.transpose(result)
		result = pd.DataFrame(result,columns = ['IP','Prediction'])
		
		"""Save results in a dictionary """
		ip_type_dict = dict()
		for row in result.itertuples():
			if ip_type_dict.get(row[1]) is None:
				ip_type_dict[row[1]] = [row[2]]
			else:
				ip_type_dict.get(row[1]).append(row[2])

		"""Output certain number of results """
		c = pd.Series(result['IP'])
		freq = c.value_counts()
		target = []
		append = target.append
		for idx ,f in enumerate(freq.iteritems()):

			r = ip_type_dict.get(f[0])

			category = category_dict.get(self.weight(r)) #get the category
			append([f[0],f[1],category])
			if idx > self.num_of_results:
				break

		target = pd.DataFrame(target,columns = ['IP','Download time','Prediction'])

		"""CHECK DIRECTORY """
		result_dir = 'result'
		result_path = os.path.join(self.script_dir,result_dir)
		if not os.path.isdir(result_path):
			try:
				os.makedirs(result_path)
			except OSError as e:
				if e.errno != 17:
					raise
				pass
		file_abs_dir = os.path.join(result_path,'result.csv')
		"""SAVE """
		target.to_csv(path_or_buf= file_abs_dir,index = False)

		print('Done')

if __name__ == "__main__":
	cg = ClassifyGuest(['dataset/oecddaily20160801.csv'])
	cg.train()
	#cg.predict()
