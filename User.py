"""User data strucutre"""
from collections import Counter
from operator import itemgetter

class User():
	def __init__(self,identity_id):
		self.identity_id = identity_id
		self.ip_add = []
		self.session_id = []
		self.user_agent = []
		self.items = []
		self.source = None
		self.event_time = [] #len(event_time) is how many times the user has visited 

	def __str__(self):
		return "<User Object>"
	def __repr__(self):
		return self.identity_id

	def add_visit(self,t_exp):
		self.event_time.append(TimeCell(t_exp))

	def add_item(self,items):
		self.items.append((items[0],TimeCell(items[1])))


	def duplicate_removal(self):
		self.ip_add = list(set(self.ip_add))
		seen = set()
		clean_event_time = []
		for t in self.event_time:
			if t.check_identity() not in seen:
				clean_event_time.append(t)
				seen.add(t.check_identity())
		self.event_time = clean_event_time
		#TO DO item list duplicate removal 



	def sort_visit(self):
		c = Counter(self.event_time)
		return sorted(c.items(),key=itemgetter(0))


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
		return "{}/{}/{}".format(self.month,self.day,self.year) #MM#DD#YYYY

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









