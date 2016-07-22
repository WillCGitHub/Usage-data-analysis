"""User data strucutre"""
from collections import Counter
from operator import itemgetter
import requests

class User():
	def __init__(self,identity_id):
		"""
		User category:
		0 - University 
		1 - Gov
		2 - Private industry
		3 - Media
		4 - Think tank
		5 - Library
		6 - Bank
		7 - International Organization
		8 - Unkown
		"""
		self.user_name = None
		self.email = None
		self.CU_number = None
		self.identity_id = identity_id
		self.ip_add = []
		self.session_id = []
		self.user_agent = []
		self.items = []
		self.source = []
		self.event_time = [] #len(event_time) is how many times the user has visited 
		if ip_add is not None:
			self.geo = self.geo_info()
		else:
			self.geo = None
		self.category = None

	def __str__(self):
		return "<User Object>"
	def __repr__(self):
		return self.identity_id

	def add_ip(self,IP):
		if IP not in set(self.ip_add):
			self.ip_add.append(IP)

	def add_session_id(self,session_id):
		if session_id not in set(self.session_id):
			self.session_id.append(session_id)

	def add_user_agent(self,user_agent):
		if user_agent not in set(self.user_agent):
			self.user_agent.append(user_agent)

	def add_visit(self,t_exp):
		self.event_time.append(TimeCell(t_exp))

	def add_item(self,items):
		if items not in set(self.items):
			self.items.append(items)

	def add_source(self,s):
		self.source.append(s)

	def duplicate_removal(self):
		seen = set()
		clean_event_time = []
		for t in self.event_time:
			if t.check_identity() not in seen:
				clean_event_time.append(t)
				seen.add(t.check_identity())
		self.event_time = clean_event_time



	def sort_visit(self,sort_by = "day", **kwarg):
		"""
		Deafult sort by day interval
		sort_visit(sort_by = "month")
		sort_visit(sort_by = "year")
		Or user customized sort
		sort_visit(sort_by = "16/7") 
		use the formmat Year/Month
		"""
		if sort_by == "day":
			c = Counter(self.event_time)
			return sorted(c.items(),key=itemgetter(0))
		elif sort_by == "month":
			month_visit_list = []
			for visit in self.event_time:
				month_visit_list.append(visit.check_month())
			c = Counter(month_visit_list)
			return sorted(c.items(),key=itemgetter(0))
		else:
			"""Customized sort"""
			month_visit_list = []
			for visit in self.event_time:
				if visit.check_month() == sort_by:
					month_visit_list.append(visit)
			c = Counter(month_visit_list)
			return sorted(c.items(),key=itemgetter(0))

	def geo_info(self):
		IP = ip_add[0]
		result = requests.get('http://ipinfo.io/{}'.format(IP)).json()
		return result.get('country')




"""TimeCell data structure	"""

class TimeCell():
	def __init__(self,expression):
		split_exp = self.split_time_exp(expression)
		self.year = int(split_exp[0])
		self.month = self.convert_month_exp(split_exp[1])
		self.day = int(split_exp[2])
		self.hour = int(split_exp[3])
		self.minute = int(split_exp[4])
		self.second = int(split_exp[5])

	def __repr__(self):
		return "{}/{}/{}".format(self.year,self.month,self.day,) #YYYY#MM#DD

	def _key(self):
		return (self.year,self.month,self.day)

	def __lt__(self,other):
		return self._key() < other._key()

	def __eq__(self,other):
		return self._key() == other._key()

	def __gt__(self,other):
		return self.key() > other._key()

	def __hash__(self):
		return hash(self._key())

	def check_identity(self):
		return (self.year,self.month,self.day,self.hour,self.minute,self.second)

	def check_month(self):
		return "".join([str(self.year), "/",str(self.month)])

	def check_for_range(self,target, year = None, month = None, **kwarg):
		"""
		a = TimeCell(" time experssion here ")
		check_for_range(a, year = 16, month = 7)
		return boolean
		"""
		if year is not None:
			if target.year == year:
				if month is not None:
					if target.month == month:
						return True
					else:
						return False
				else:
					return True
			else:
				return False
		else:
			return False




	def split_time_exp(self,time_exp):
		divide_time = time_exp.split(" ")
		ymd = divide_time[0].split("-")
		year = ymd[2]
		month = ymd[1]
		day = ymd[0]
		hour = divide_time[1].split(".")[0]
		minute = divide_time[1].split(".")[1]
		second = divide_time[1].split(".")[2]
		if (divide_time[2] == "AM") and (hour == "12"):
			hour = str(0)
		if (divide_time[2] == "PM") and (hour != "12"):
			hour = str(int(hour)+12)

		splited_time_exp = [year,month,day,hour,minute,second]

		return splited_time_exp

	def convert_month_exp(self,expr):
		if expr == 'JAN':
			return 1
		elif expr == 'FEB':
			return 2
		elif expr == 'MAR':
			return 3
		elif expr == 'APR':
			return 4
		elif expr == 'MAY':
			return 5
		elif expr == 'JUN':
			return 6
		elif expr == 'JUL':
			return 7
		elif expr == 'AUG':
			return 8
		elif expr == 'SEP':
			return 9
		elif expr == 'OCT':
			return 10
		elif expr == 'NOV':
			return 11
		elif expr == 'DEC':
			return 12
		else:
			return 0





if __name__ == "__main__":
	pass









