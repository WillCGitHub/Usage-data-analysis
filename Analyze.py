""" 
Analyze data 
Daily object or MultiDays object
"""

from collections import Counter
import requests

class Analyze(object):
	"""docstring for Analyze"""
	def __init__(self, dataPackage):
		self.dataPackage = dataPackage

	"""Return a dictionary that link between IP and 
		identity id {"IP":"identity id"} """
	def identity(self):
		idDict = dict()
		for idx in range(0,len(self.dataPackage.ip_add)):		
			if idDict.get(self.dataPackage.ip_add[idx])is None:
				idDict[self.dataPackage.ip_add[idx]] = [self.dataPackage.identityid[idx]]
			else:
				if self.dataPackage.identityid[idx] not in set(idDict.get(self.dataPackage.ip_add[idx])):
					idDict.get(self.dataPackage.ip_add[idx]).append(self.dataPackage.identityid[idx])
		return idDict

	"""Return a dictionary that link between identity id and IPs """
	def reg_ip_check(self):
		reg_ip = dict()
		regs = self.dataPackage.identityid
		ips = self.dataPackage.ip_add
		for idx,reg in enumerate(regs):
			if reg != 'guest':
				if reg_ip.get(reg) is None:
					reg_ip[reg] = [ips[idx]]
				else:
					if ips[idx] not in set(reg_ip.get(reg)):
						reg_ip.get(reg).append(ips[idx])
		return reg_ip

	def reg_time(self):
		reg_time = dict()
		regs = self.dataPackage.identityid
		times = self.dataPackage.time
		for idx,reg in enumerate(regs):
			if reg != 'guest':
				if reg_time.get(reg) is None:
					reg_time[reg] = [times[idx]]
				else:
					reg_time.get(reg).append(times[idx])
		return reg_time

	def time_freq(self):
		#convert to 24 H format
		for idx in range(0,len(self.period)):
			if (self.period[idx] == "AM") and (self.hour[idx]==12):
				self.hour[idx]-=12
			if (self.period[idx] == "PM") and (self.hour[idx]!=12):
				self.hour[idx]+=12
		h_list = Counter(self.hour).most_common(24) #showing how many results
		for h in h_list:
			print("Time: {}:00 (GMT+2), page view: {} \n".format(h[0],h[1]))
		print("\n\n\n")


	#how many session ids per IP address {"IPs":"session ids"}
	def session(self):
		session = dict()
		for idx in range(0,len(self.dataPackage.ip_add)):
			if session.get(self.dataPackage.ip_add[idx]) is None:
				session[self.dataPackage.ip_add[idx]] = [self.dataPackage.sessionid[idx]]
			else:
				if self.dataPackage.sessionid[idx] not in set(session.get(self.dataPackage.ip_add[idx])):
					session.get(self.dataPackage.ip_add[idx]).append(self.dataPackage.sessionid[idx])
		return session

	#how many IPs per session ids
	def Analyze_by_session(self,num_of_item):
		IPs = dict()

		for idx in range(0,len(self.dataPackage.sessionid)):
			if IPs.get(self.dataPackage.sessionid[idx]) is None:
				IPs[self.dataPackage.sessionid[idx]] = [self.dataPackage.ip_add[idx]]
			else:
				if self.dataPackage.ip_add[idx] not in set(IPs.get(self.dataPackage.sessionid[idx])):
					IPs.get(self.dataPackage.sessionid[idx]).append(self.dataPackage.ip_add[idx])

		
		session_Download = dict()

		for idx in range(0,len(self.dataPackage.sessionid)):
			if session_Download.get(self.dataPackage.sessionid[idx]) is None:
				session_Download[self.dataPackage.sessionid[idx]] = [self.dataPackage.item_id[idx]]
			else:
				if self.dataPackage.item_id[idx] not in set(IPs.get(self.dataPackage.sessionid[idx])):
					session_Download.get(self.dataPackage.sessionid[idx]).append(self.dataPackage.item_id[idx])


		most_freq_sessionid = Counter(self.dataPackage.sessionid).most_common(num_of_item)
		print("Most frequently visited session ids: \n")
		for s in most_freq_sessionid:
			print("Session ID: {}, visited {} time(s).".format(s[0],s[1]))
			print("IP: {}".format(IPs.get(s[0])))
			#detail list of downloaded content
			print("The session downloaded {} items. \n Deatils: \n ... \n\n".format(len(session_Download.get(s[0]))))#,session_Download.get(s[0])))

	def ip_freq(self,num_of_item):
		ip_freq = Counter(self.dataPackage.ip_add)
		#self.most_frequent used in self.detail()
		self.most_frequent = ip_freq.most_common(num_of_item)

	#IP correspond to item
	def item(self):
		item = dict()
		for idx in range(0,len(self.dataPackage.ip_add)):
			if item.get(self.dataPackage.ip_add[idx]) is None:
				item[self.dataPackage.ip_add[idx]] = [self.dataPackage.item_id[idx]]
			else:
				if self.dataPackage.item_id[idx] not in set(item.get(self.dataPackage.ip_add[idx])):
					item.get(self.dataPackage.ip_add[idx]).append(self.dataPackage.item_id[idx])
		return item

	#how many items a user has downloaded
	def id_item(self):
		item = dict()
		for idx, u in enumerate(self.dataPackage.identityid):
			if u != 'guest':
				if item.get(self.dataPackage.identityid[idx]) is None:
					item[self.dataPackage.identityid[idx]] = [(self.dataPackage.item_id[idx],self.dataPackage.time[idx])]
				else:
					if (self.dataPackage.item_id[idx],self.dataPackage.time[idx]) not in set(item.get(self.dataPackage.identityid[idx])):
						item.get(self.dataPackage.identityid[idx]).append((self.dataPackage.item_id[idx],self.dataPackage.time[idx]))
		return item


	def item_count(self,num_of_item):
		c = Counter (self.dataPackage.item_id)
		item_list = c.most_common(num_of_item)
		print("Top {} download".format(num_of_item))
		for i in item_list:
			print("Content: {} | Download volume: {} \n".format(i[0],i[1]))
		print("\n\n\n")

	#print out the detail information
	def classify(self):
		identityDict = self.identity()
		#print("Top {} most frequently visited IPs".format(len(self.most_frequent)))
		self.registered_user = [ip for ip in self.most_frequent if identityDict.get(ip[0])[0] != 'guest']
		self.unregistered_user =[ip for ip in self.most_frequent if identityDict.get(ip[0])[0] == 'guest']
		

	def GeoIP(self,IP):
		result = requests.get('http://ipinfo.io/{}'.format(IP)).json()
		try:
			print("Organization: {} ".format(result.get('org')))
		except:
			org = result.get('org').encode('utf-8').decode('ascii','ignore')
			result['org'] = org
			print("Organization: {} ".format(result.get('org')))
		try:
			print("City: {}".format(result.get('city')))
		except:
			city = result.get('city').encode('utf-8').decode('ascii','ignore')
			result['city'] = city
			print("City: {}".format(result.get('city')))
		try:
			print("Country: {}".format(result.get('country')))
		except:
			country = result.get('country').encode('utf-8').decode('ascii','ignore')
			result['country'] = country
			print("Country: {}".format(result.get('country')))

		return result

	def print_registered_user(self, num_of_result):
		itemDict = self.item()
		sessionDict = self.session()
		identityDict = self.identity()
		num = 1
		print("Registered user\n")
		for ip in self.registered_user:
			print("#{} ".format(num))
			print("IP: {} visited the sites {} times. ".format(ip[0],ip[1]))
			print("IP details:")
			try:
				r = self.GeoIP(ip[0])
			except:
				print("Unable to load geographical information...")
				print("Try to access the information through a browser manually...")
				print("http://ipinfo.io/{}".format(ip[0]))
			print("Identity ID: {}".format(identityDict.get(ip[0])[0]))
			print("This IP address downloaded {} contents".format(len(itemDict.get(ip[0]))))
			#print(itemDict.get(ip[0]))
			print("Number of session ID: {}".format(len(sessionDict.get(ip[0]))))
			#print out for details
			#print("Session ID: ... ")#.format(sessionDict.get(ip[0])))
			print("\n \n \n")
			if num == num_of_result:
				break
			num+=1

	def print_unregistered_user(self, num_of_result):
		itemDict = self.item()
		sessionDict = self.session()
		identityDict = self.identity()
		num = 1
		print("Unregistered user\n")
		for ip in self.unregistered_user:
			print("#{} ".format(num))
			print("IP: {} visited the sites {} times. ".format(ip[0],ip[1]))
			print("IP details:")
			try:
				r = self.GeoIP(ip[0])
			except:
				print("Unable to load geographical information...")
				print("Try to access the information through a browser manually...")
				print("http://ipinfo.io/{}".format(ip[0]))
			print("Identity ID: {}".format(identityDict.get(ip[0])[0]))
			print("This IP address downloaded {} contents".format(len(itemDict.get(ip[0]))))
			#print(itemDict.get(ip[0]))
			print("Number of session ID: {}".format(len(sessionDict.get(ip[0]))))
			#print out for details
			#print("Session ID: ... ")#.format(sessionDict.get(ip[0])))
			print("\n \n \n")
			if num == num_of_result:
				break
			num+=1

if __name__ =="__main__":
	pass
