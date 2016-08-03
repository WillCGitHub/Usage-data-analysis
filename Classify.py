from User import *
import pickle
from UserAnalysis import UserAnalysis
from openpyxl import load_workbook
import copy
import sys
import csv
import string
from collections import Counter
import pandas as pd



def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('userdb/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

category_dict = {'100':'No Profile',
					'101':'Trade Partner',
					'102':'Think Tank',
					'103':'Consortia',
					'104':'Industry',
					'105':'Parliament',
					'106':'End Client',
					'107':'Government',
					'108':'International Organisation',
					'109':'Library',
					'110':'Academic',
					'111':'Dataseller',
					'112':'NGOs & Civil Soc Org & Trade Uni',
					'114':'Financial & Legal Services'}
cu_profile = 'TurpinFiles/xpslite_customer_profile.csv'
df = pd.read_csv(cu_profile,header = 0,dtype = str)
cu_profile_code_dict = dict()
for row in df.itertuples():
	if category_dict.get(row[3]) is not None:
		cu_profile_code_dict[row[1].lower()] = row[3]
print(len(cu_profile_code_dict))

print('load userdb')
user_dict = load_obj('user_dict')

for u,d in user_dict.items():
	cu = d.identity_dict.get('CU_number')
	profile_code = cu_profile_code_dict.get(cu)
	d.identity_dict['category'] = profile_code


save_obj(user_dict,'user_dict')







