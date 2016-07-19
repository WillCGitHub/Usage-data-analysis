"""
MultiDays class
Store multiple Daily class
"""
class MultiDays(object):
	"""MultiDays"""
	def __init__(self, identityid,time,sessionid,ip_add,item_id,source,Days_counter):
		self.identityid = identityid
		self.time = time
		self.sessionid = sessionid
		self.ip_add = ip_add
		self.item_id = item_id
		self.source = source
		self.Days_counter = Days_counter
		self.interval = "{} -- {} ".format(self.Days_counter,self.time[0],self.time[-1])
	def __str__(self):
		return "Data for {} days. {} -- {} ".format(self.Days_counter,self.time[0],self.time[-1])
	def __repr__(self):
		return self.interval
	def __add__(self,other):
		total_identityid = self.identityid + other.identityid
		total_time = self.time + other.time
		total_sessionid = self.sessionid + other.sessionid	
		total_ip_add = self.ip_add + other.ip_add
		total_item_id = self.item_id + other.item_id
		total_source = self.source + other.source
		self.Days_counter +=1
		return MultiDays(total_identityid,total_time,total_sessionid,total_ip_add,total_item_id, total_source,self.Days_counter)

		
