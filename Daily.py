"""
Convert Daily data set into an object, so the daily data can be accessed easily.
Useful for weekly, monthly, annually Analysis. 
"""
import csv
from MultiDays import MultiDays
class Daily():
	def __init__(self,path):
		self.path = path
		self.convert()
		self.Days_counter = 1

	def __str__(self):
		return "{} | {} records".format(self.day[0], len(self.day))
	def __repr__(self):
		return self.day
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


	def convert(self):
		self.identityid = []
		self.time = []
		self.sessionid = []	
		self.ip_add = []
		self.item_id = [] 
		self.source = []
		self.user_agent = []

		with open(self.path,newline='',encoding='utf-8') as csvfile:
			reader = csv.reader(csvfile,delimiter=',')
			for row in reader:
				#avoid decoding error
				try:
					self.identityid.append(row[1])
				except:
					pass
				try:
					self.time.append(row[2])
				except:
					pass
				try:
					self.sessionid.append(row[3])
				except:
					pass
				try:
					self.ip_add.append(row[4])
				except:
					pass
				try:
					self.item_id.append(row[6])
				except:
					pass
				try:
					self.source.append(row[9])
				except:
					pass
				try:
					self.user_agent.append(row[5])
				except:
					pass
		
		#get rid of the labels
		self.time.pop(0)
		self.identityid.pop(0)
		self.sessionid.pop(0)
		self.ip_add.pop(0)
		self.item_id.pop(0)
		self.source.pop(0)
		self.user_agent.pop(0)

		#Split time experssion. 
		self.day = []
		self.hour = []
		self.period = []
		for a in self.time:
			divide = a.split(" ")
			self.day.append(divide[0])
			self.hour.append(int(divide[1].split(".")[0])) #disregard minutes and seconds
			self.period.append(divide[2])



if __name__ == "__main__":
	pass

	
