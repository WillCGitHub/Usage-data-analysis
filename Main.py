from User import *
import pickle
from collections import Counter
from operator import itemgetter
from UserAnalysis import UserAnalysis
import csv

update = input("Would you like to update user database? (y/n) ")
if update == 'y':
	import UserDict


def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

print("Computing...")
ud = load_obj('user_dict')
result = []
for u,d in ud.items():
	ua = UserAnalysis(d)
	if len(ua.visit_freq) < 3 :
		result.append((u,(ua.average_visit(),'visit too few to show result')))
	else:
		mm = ua.moving_means()
		cmm = ua.centered_moving_means()
		ise = ua.ISE()
		ave_v = ua.average_visit()
		percentage = round((ise/ave_v)*100,3)
		result.append((u,(ave_v,percentage)))

print("Writing result")

with open ('result/analysis.csv','w') as f:
	writer = csv.writer(f,delimiter=',')
	writer.writerow(['Registered user id','average visit per day','expecation'])
	for r in result:
		try:
			writer.writerow([r[0],'{0:.1f}'.format(float(r[1][0])),'{0:.3f}%'.format(float(r[1][1]))])
		except:
			writer.writerow([r[0],'{0:.1f}'.format(float(r[1][0])), r[1][1]])






