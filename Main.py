from User import *
import pickle
from collections import Counter
from operator import itemgetter
from UserAnalysis import UserAnalysis
import csv
import argparse
import gc
import sys
import multiprocessing as mp

ap = argparse.ArgumentParser()
ap.add_argument("-a", "--analysis_interval", help="analysis_interval")
ap.add_argument("-y","--year_analysis", help="year_analysis")
args = ap.parse_args()
if args.analysis_interval:
	analysis_interval = args.analysis_interval
else:
	analysis_interval = 'month'
if args.year_analysis:
	if args.year_analysis == "true" or args.year_analysis == "True":
		year_analysis = True
	elif args.year_analysis == "false" or args.year_analysis == "False":
		year_analysis = False
else:
	year_analysis = True

"""Update userdb """
update = input("Would you like to update user database? (y/n) ")
if update == 'y':
	import DataManagement
""" end """

def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def proceed_analysis(user,d,f):
	f = open ('result/analysis.csv','a')
	ua = UserAnalysis(d,analysis_interval = analysis_interval)
	ise = ua.ISE(year_analysis=year_analysis)
	ave_m_e = ua.average_month_effect(ise)
	ave_v = ua.average_visit()
	u_exp = ua.usage_expectation(ave_m_e,ave_v)
	name = d.identity_dict.get('user_name')
	email = d.identity_dict.get('email')
	cu_number = d.identity_dict.get('CU_number')
	geo = d.identity_dict.get('geo')

	#r[user] = (ave_v,u_exp)
	_writer(csv.writer(f,delimiter=','),
			user,
			(ave_v,u_exp),
			name,
			email,
			cu_number,
			geo)
	f.close()


def _writer(w,u,r,name,email,cun,geo):
	"""pass in args: 
		csv writer, 
		user id, 
		data,
		user name,
		email,
		cu_number,
		geo location """
	w.writerow([u,
				'{0:.1f}'.format(float(r[0])),
				'{}'.format(name),
				'{}'.format(email),
				'{}'.format(cun),
				'{}'.format(geo),
				'{0:.3f}%'.format(float(r[1][0][1])),
				'{0:.3f}%'.format(float(r[1][1][1])),
				'{0:.3f}%'.format(float(r[1][2][1])),
				'{0:.3f}%'.format(float(r[1][3][1])),
				'{0:.3f}%'.format(float(r[1][4][1])),
				'{0:.3f}%'.format(float(r[1][5][1])),
				'{0:.3f}%'.format(float(r[1][6][1])),
				'{0:.3f}%'.format(float(r[1][7][1])),
				'{0:.3f}%'.format(float(r[1][8][1])),
				'{0:.3f}%'.format(float(r[1][9][1])),
				'{0:.3f}%'.format(float(r[1][10][1])),
				'{0:.3f}%'.format(float(r[1][11][1])),])


"""INITIALIZE WRITER """
f = open ('result/analysis.csv','w')
writer = csv.writer(f,delimiter=',')
if analysis_interval == "month":
	time_interval = "monthly"
else:
	if year_analysis is True:
		time_interval = "monthly"
	elif year_analysis is False:
		time_interval = "daily"
writer.writerow(['Registered user id',
					'{} average visit'.format(time_interval),
					'Name',
					'Email',
					'CU_number',
					'Country',
					'JAN','FEB','MAR','APR',
					'MAY','JUN','JUL','AUG',
					'SEP','OCT','NOV','DEC'])
f.close()
"""------------------ """

"""START ANALYZING """
print("Computing...")
ud = load_obj('user_dict')
#result = mp.Manager().dict()


jobs = []
append = jobs.append
c = 0
for idx, (u, d) in enumerate(ud.items()):
	if d.identity_dict.get('CU_number') is not None:
		p = mp.Process(target = proceed_analysis, args = (u,d,f))
		p.start()
		append(p)
		
		c+=1 
		if c >= 8 :
			jobs[0].join()
			jobs.pop(0)
			c -=1 

	print("{0:.1f}%\r".format(float((idx+1)/len(ud)*100)), end='')
	sys.stdout.flush()

for j in jobs:
	j.join()

f.close()



