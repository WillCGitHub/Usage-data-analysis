from User import *
import pickle
from collections import Counter
from operator import itemgetter
from UserAnalysis import UserAnalysis
import csv
import argparse

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

update = input("Would you like to update user database? (y/n) ")
if update == 'y':
	import UserDict


def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

print("Computing...")
ud = load_obj('user_dict')
result = []




for u, d in ud.items():
	ua = UserAnalysis(d,analysis_interval = analysis_interval )
	mm = ua.moving_means()
	cmm = ua.centered_moving_means()
	ise = ua.ISE(year_analysis=year_analysis)
	ave_v = ua.average_visit()
	if ise is not None:
		result.append((u,(ave_v,ua.usage_expectation(ise,ave_v))))
def getkey(item):
	return item[1][1]
result = sorted(result, key = getkey)


print("Writing result")

with open ('result/analysis.csv','w') as f:
	writer = csv.writer(f,delimiter=',')
	writer.writerow(['Registered user id','average visit per day','expecation'])
	for r in result:
		try:
			writer.writerow([r[0],'{0:.1f}'.format(float(r[1][0])),'{0:.3f}%'.format(float(r[1][1]))])
		except:
			writer.writerow([r[0],'{0:.1f}'.format(float(r[1][0])), r[1][1]])






