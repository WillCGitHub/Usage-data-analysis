from User import *
from statistics import mean
import pickle
from operator import itemgetter
import gc
from datetime import date

class UserAnalysis():

	def __init__(self,user,analysis_interval = None, a_range = (15,16), **kwargs):
		self.user = user
		self.analysis_interval = analysis_interval
		if analysis_interval == "month":
			self.visit_freq = dict(user.sort_visit(sort_by = "month"))
			current_month = int(str(date.today()).split("-")[1])
			current_year = int(str(date.today()).split("-")[0][-2:])
			for yy in range(a_range[0],a_range[1]+1):
				for mm in range(1,13):
					if (yy == current_year) and (mm > current_month):
						break
					if mm < 10:
						mm = ''.join(['0',str(mm)])
					exp = '{}/{}'.format(yy,mm)
					#if there is no visit, then set visit time to 0
					if self.visit_freq.get(exp) is None:
						self.visit_freq[exp] = 0

			rl = []
			append = rl.append
			for d,f in self.visit_freq.items():
				y = int(d.split("/")[0])
				if (y >= a_range[0]) and (y <= a_range[1]):
					append((d,f))
			self.visit_freq = sorted(rl,key = itemgetter(0))

		elif analysis_interval is None:
			self.visit_freq = user.sort_visit()
		else:
			self.visit_freq = user.sort_visit(sort_by = analysis_interval)

		gc.collect()

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
				time_label = moving_means[idx].time_label
				analysis_label = "centered_moving_means"
				data = mean([AF.data,moving_means[idx+1].data])
				centered_moving_means.append(AnalysisFrame(time_label,analysis_label,data))
				if idx == len(moving_means)-2:
					break
			return centered_moving_means
		else:
			return None

	def ISE(self, year_analysis = False, **kwargs):
		visit_freq = dict(self.visit_freq)
		cmm = self.centered_moving_means()
		ISE = []
		if cmm is not None:
			if year_analysis == False:
				for idx, cmm_AF in enumerate(cmm):
					ISE.append(visit_freq[idx+1][1]-cmm_AF.data)
				return mean(ISE)
			elif year_analysis == True:
				year_analysis_ISE = dict()
				for cmm_AF in cmm:
					ise = visit_freq.get(cmm_AF.time_label) - cmm_AF.data
					if year_analysis_ISE.get(cmm_AF.time_label) is None:
						year_analysis_ISE[cmm_AF.time_label] = AnalysisFrame(cmm_AF.time_label,'ISE',ise)
				return year_analysis_ISE
		else:
			return None

	def average_month_effect(self,ISE_dict):
		ave_month_effect = dict()
		for t, d in ISE_dict.items():
			ym = t.split("/")
			year = ym[0]
			month = ym[1]
			if year == '14':
				continue
			
			if ave_month_effect.get(month) is None:
				ave_month_effect[month] = [d.data]
			else:
				ave_month_effect.get(month).append(d.data)
		for mon, d in ave_month_effect.items():
			ave_month_effect[mon] = mean(ave_month_effect.get(mon))
		return ave_month_effect




	def usage_expectation(self, ave_m_e, ave_v):
		p = dict()
		for m, d in ave_m_e.items():
			if (d == 0) or (ave_v == 0):
				percentage = 0
			else:
				percentage = round((d/ave_v)*100,3)
			p[m] = percentage
		return sorted(p.items(),key = itemgetter(0))



	def average_visit(self):
		visit_freq = dict(self.visit_freq)
		if len(visit_freq) < 1:
			return None
		freq = []
		freq = map(float,visit_freq.values())

		return mean(freq)



class AnalysisFrame():
	def __init__(self,time_label,analysis_label,data):
		if type(time_label) == TimeCell:
			if time_label.month < 10:
				self.time_label = "".join([str(time_label.year),"/0",str(time_label.month)])
			else:
				self.time_label = "".join([str(time_label.year),"/",str(time_label.month)])
		else:
			self.time_label = time_label
		self.analysis_label = analysis_label
		self.data = data
	def __repr__(self):
		return "".join([self.analysis_label," of ", self.time_label, ": ", str(self.data)])

		


if __name__ =="__main__":
	def load_obj(name):
	    with open('userdb/' + name + '.pkl', 'rb') as f:
	        return pickle.load(f)

	print("Computing...")
	ud = load_obj('user_dict')
	for idx, (u, d) in enumerate(ud.items()):
		ua = UserAnalysis(d,analysis_interval = 'month' )
		ise = ua.ISE(year_analysis = True)
		ave_m_e = ua.average_month_effect(ise)
		ave_v = ua.average_visit()
		u_exp = ua.usage_expectation(ave_m_e,ave_v)
		print(u_exp)
		break









