"""User data strucutre"""
from collections import Counter
from operator import itemgetter
import requests


class User():
	def __init__(self,identity_id):
		"""
		100	No Profile
		101	Trade Partner
		102	Think Tank
		103	Consortia
		104	Industry
		105	Parliament
		106	End Client
		107	Government
		108	International Organisation
		109	Library
		110	Academic
		111	Dataseller
		112	NGOs & Civil Soc Org & Trade Uni
		114	Financial & Legal Services
		"""
		self.identity_dict = dict()
		self.identity_dict['user_name'] = None
		self.identity_dict['email'] = None
		self.identity_dict['CU_number'] = None
		self.identity_dict['identity_id'] = identity_id
		self.identity_dict['ip_add'] = []
		self.identity_dict['items'] = []
		self.identity_dict['source'] = []
		self.identity_dict['event_time'] = []
		self.identity_dict['geo'] = None
		self.identity_dict['category'] = None


	def __str__(self):
		return "<User Object>"
	def __repr__(self):
		return self.identity_id

	def add_ip(self,IP):
		if IP not in set(self.identity_dict['ip_add']):
			self.identity_dict['ip_add'].append(IP)

	def add_visit(self,t_exp):
		self.identity_dict['event_time'].append(TimeCell(t_exp))


	def add_item(self,items):
		if items not in set(self.identity_dict['items']):
			self.identity_dict['items'].append(items)

	def add_source(self,s):
		self.identity_dict['source'].append(s)


	def sort_visit(self,sort_by = "day", **kwarg):
		"""
		Deafult sort by day interval
		sort_visit(sort_by = "month")
		sort_visit(sort_by = "year")
		Or user customized sort
		sort_visit(sort_by = "16/7") 
		use the formmat Year/Month
		"""
		event_time = self.identity_dict.get('event_time')
		if sort_by == "day":
			c = Counter(event_time)
			return sorted(c.items(),key=itemgetter(0))
		elif sort_by == "month":
			month_visit_list = []
			for visit in event_time:
				month_visit_list.append(visit.check_month())
			c = Counter(month_visit_list)
			return sorted(c.items(),key=itemgetter(1))
		else:
			"""Customized sort"""
			month_visit_list = []
			for visit in event_time:
				if visit.check_month() == sort_by:
					month_visit_list.append(visit)
			c = Counter(month_visit_list)
			return sorted(c.items(),key=itemgetter(0))

	def geo_info(self):
		IP = self.ip_add[0]
		result = requests.get('http://ipinfo.io/{}'.format(IP)).json()
		return result.get('country')




"""TimeCell data structure	"""

class TimeCell():
	def __init__(self,expression):
		try:
			split_exp = self.split_time_exp(expression)
		except:
			print("error expression: {}".format(expression))
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
		if self.month < 10:
			return "".join([str(self.year), "/0",str(self.month)])
		else:
			return "".join([str(self.year), "/",str(self.month)])


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
	expre = "01-OCT-15 12.01.09.000000 AM"
	t = TimeCell(expre)
	print(t.year)









