from User import *
from statistics import mean

class UserAnalysis():

	def __init__(self,user,analysis_interval = None, **kwargs):
		self.user = user
		self.analysis_interval = analysis_interval
		if analysis_interval == "month":
			self.visit_freq = user.sort_visit(sort_by = "month")
		elif analysis_interval is None:
			self.visit_freq = user.sort_visit()
		else:
			self.visit_freq = user.sort_visit(sort_by = analysis_interval)

	def __repr__(self):
		return self.user

	def moving_means(self):
		visit_freq = self.visit_freq
		if len(visit_freq) < 2:
			return None
		moving_means = []
		for idx, (date, freq) in enumerate(visit_freq):
			time_label = visit_freq[idx+1][0]
			analysis_label = "moving_means"
			data = mean([freq,visit_freq[idx+1][1]])
			moving_means.append(AnalysisFrame(time_label,analysis_label,data))
			if idx == len(visit_freq)-2:
				break
		return moving_means


	def centered_moving_means(self):
		moving_means = self.moving_means()
		centered_moving_means = []
		if moving_means is not None:
			if len(moving_means) < 2:
				return None
			for idx, AF in enumerate(moving_means):
				time_label = moving_means[idx+1].time_label
				analysis_label = "centered_moving_means"
				data = mean([AF.data,moving_means[idx+1].data])
				centered_moving_means.append(AnalysisFrame(time_label,analysis_label,data))
				if idx == len(moving_means)-2:
					break
			return centered_moving_means
		else:
			return None

	def ISE(self, year_analysis = False, **kwargs):
		visit_freq = self.visit_freq
		cmm = self.centered_moving_means()
		ISE = []
		if cmm is not None:
			if year_analysis == False:
				for idx, cmm_AF in enumerate(cmm):
					ISE.append(visit_freq[idx+1][1]-cmm_AF.data)
				return mean(ISE)
			elif year_analysis == True:
				analysis_dict = dict()
				for idx, cmm_AF in enumerate(cmm):
					if analysis_dict.get(cmm_AF.time_label[1]) is None:
						analysis_dict[cmm_AF.time_label[1]] = [cmm_AF.data]
					else:
						analysis_dict.get(cmm_AF.time_label[1]).append(cmm_AF.data)
				year_analysis_ISE = dict()
				for mo, ise in analysis_dict.items():
					if year_analysis_ISE.get(mo) is None:
						year_analysis_ISE[mo] = mean(ise)
				return year_analysis_ISE
		else:
			return None

	def usage_expectation(self, ise, ave_v):
		if type(ise) == float:
			visit_times = ise
		elif type(ise) == dict:
			visit_times = list(ise.values())[0]
		percentage = round((visit_times/ave_v)*100,3)
		return percentage



	def average_visit(self):
		visit_freq = self.visit_freq
		if len(visit_freq) < 1:
			return None
		freq = []
		for date,f in visit_freq:
			freq.append(f)
		return mean(freq)



class AnalysisFrame():
	def __init__(self,time_label,analysis_label,data):
		if type(time_label) == TimeCell:
			self.time_label = "".join([str(time_label.year),"/",str(time_label.month)])
		else:
			self.time_label = time_label
		self.analysis_label = analysis_label
		self.data = data
	def __repr__(self):
		#return "".join([self.analysis_label," of ",self.time_label])
		return "".join([self.analysis_label," of ", self.time_label, ": ", str(self.data)])

		


if __name__ =="__main__":
	pass









