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
	analysis_interval = None
if args.year_analysis:
	if args.year_analysis == "true" or args.year_analysis == "True":
		year_analysis = True
	else:
		year_analysis = False
else:
	year_analysis = False

"""Update userdb """
update = input("Would you like to update user database? (y/n) ")
if update == 'y':
	from UserDict import UserDict
	ud = UserDict("dataset")
	ud.main(8)
	gc.collect()
	print('')
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
	#r[user] = (ave_v,u_exp)
	_writer(csv.writer(f,delimiter=','),user,(ave_v,u_exp))
	f.close()


def _writer(w,u,r):
	"""pass in args: csv writer, user name, data """
	w.writerow([u,'{0:.1f}'.format(float(r[0])),
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

"""
print("Writing result")


with open ('result/analysis.csv','w') as f:
	writer = csv.writer(f,delimiter=',')
	if analysis_interval == "month":
		time_interval = "per month"
	else:
		if year_analysis is True:
			time_interval = "monthly"
		elif year_analysis is False:
			time_interval = "daily"
	writer.writerow(['Registered user id',
						'{} average visit'.format(time_interval),
						'JAN','FEB','MAR','APR',
						'MAY','JUN','JUL','AUG',
						'SEP','OCT','NOV','DEC'])
	for u,r in result.items():
		try:
			writer.writerow([u,'{0:.1f}'.format(float(r[0])),
							'{0:.3f}'.format(float(r[1][0])),
							'{0:.3f}'.format(float(r[1][1])),
							'{0:.3f}'.format(float(r[1][2])),
							'{0:.3f}'.format(float(r[1][3])),
							'{0:.3f}'.format(float(r[1][4])),
							'{0:.3f}'.format(float(r[1][5])),
							'{0:.3f}'.format(float(r[1][6])),
							'{0:.3f}'.format(float(r[1][7])),
							'{0:.3f}'.format(float(r[1][8])),
							'{0:.3f}'.format(float(r[1][9])),
							'{0:.3f}'.format(float(r[1][10])),
							'{0:.3f}'.format(float(r[1][11])),])
		except:
			pass

"""



