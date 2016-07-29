"""
Convert Daily data set into an object, so the daily data can be accessed easily.
Useful for weekly, monthly, annually Analysis. 
"""

import pandas as pd
import csv


class Daily():
	def __init__(self,path = None):
		self.path = path
		self.identity_dict = dict()

		self.identity_dict['identity_id'] = []
		self.identity_dict['time'] = []
		self.identity_dict['ip_add'] = []
		self.identity_dict['item_id'] = []
		self.identity_dict['source'] = []
		self.identity_dict['sessionid'] = []
		self.identity_dict['user_agent'] = []
		

		self.extract()
		
		self.Days_counter = 1

	def __repr__(self):
		return "<Daily Object> {}".format(self.time[0].split(" ")[0])
	def __add__(self,other):
		total_identityid = self.identityid + other.identityid
		total_time = self.time + other.time
		total_sessionid = self.sessionid + other.sessionid	
		total_ip_add = self.ip_add + other.ip_add
		total_item_id = self.item_id + other.item_id
		total_source = self.source + other.source
		total_user_agent = self.user_agent + other.user_agent
		Days_counter = self.Days_counter + other.Days_counter
		return MultiDays(total_identityid,total_time,
							total_sessionid,
							total_ip_add,
							total_item_id,
							total_source,
							total_user_agent,
							Days_counter)


	def extract(self):
		try:
			df = pd.read_csv(self.path,header = 0,dtype = str)
			self.identity_dict['identity_id'] = list(map(str,df['identityid']))
			self.identity_dict['time'] = list(map(str,df['event_time']))
			self.identity_dict['sessionid'] = list(map(str,df['sessionid']))
			self.identity_dict['item_id'] = list(map(str,df['itemid']))
			self.identity_dict['ip_add'] = list(map(str,df['ipaddress']))
			self.identity_dict['source'] = list(map(str,df['source']))
			self.identity_dict['user_agent'] = list(map(str,df['useragent']))

		except:
			pass






if __name__ == "__main__":
	#pass
	a = Daily('dataset1/oecddaily20160401.csv')

	
