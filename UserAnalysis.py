from User import *
from statistics import mean

class UserAnalysis():

	def __init__(self,user):
		self.user = user
		self.visit_freq = self.user.sort_visit()

	def __repr__(self):
		return self.user

	def moving_means(self):
		visit_freq = self.visit_freq
		moving_means = []
		for idx, (date, freq) in enumerate(visit_freq):
			moving_means.append(mean([freq,visit_freq[idx+1][1]]))
			if idx == len(visit_freq)-2:
				break
		return moving_means


	def centered_moving_means(self):
		moving_means = self.moving_means()
		centered_moving_means = []
		for idx, mm in enumerate(moving_means):
			centered_moving_means.append(mean([mm,moving_means[idx+1]]))
			if idx == len(moving_means)-2:
				break
		return centered_moving_means

	def ISE(self):
		visit_freq = self.visit_freq
		cmm = self.centered_moving_means()
		ISE = []
		for idx, c in enumerate(cmm):
			ISE.append(visit_freq[idx+1][1]-c)
		return mean(ISE)

	def average_visit(self):
		visit_freq = self.visit_freq
		freq = []
		for date,f in visit_freq:
			freq.append(f)
		return mean(freq)

if __name__ =="__main__":
	pass