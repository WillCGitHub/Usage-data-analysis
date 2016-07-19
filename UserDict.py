"""Create Users' Map"""
from User import *
from Daily import Daily
from Analyze import Analyze 
import os
from os import listdir
from os.path import isfile,join
import sys
from functools import reduce
import pickle




#do not read in hidden files
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def save_obj(obj, name):
    with open('userdb/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

filePath ="dataset"
fileList = listdir_nohidden(filePath)
process_list = []
pre_process = [f for f in fileList]

print("Updating users data")

for idx, file in enumerate(pre_process):
	#get file path name
	file = join(filePath,file)
	process_list.append(Daily(file))
	print("{0:.1f}% \r".format(float((idx+1)/len(pre_process)*100)), end='')
	sys.stdout.flush()


multi = reduce(lambda x,y: x+y, process_list)
print('')
print(multi)

"""CREATE USER MAP"""
print("Creating user map")
an = Analyze(multi)
user_ip = an.reg_ip_check() 
user_visit_record = an.reg_time()
user_download_rec = an.id_item()
print("Load")
try:
	user_dict = load_obj('user_dict')
except:
	user_dict = dict()

#Create user -- ip dictionary
for idx, (u, ip) in enumerate(user_ip.items()):
	if user_dict.get(u) is None:
		temp = User(u)
		temp.ip_add = ip
		user_dict[u] = temp
	else:
		user_dict.get(u).ip_add+= ip
	print("{0:.1f}% \r".format(float((idx+1)/len(user_ip))*100), end='')
	sys.stdout.flush()
print('')
#user visit time
for idx, (u,t) in enumerate(user_visit_record.items()):
	for point in t:
		user_dict.get(u).add_visit(point)
	print("{0:.1f}% \r".format(float((idx+1)/len(user_visit_record))*100), end='')
	sys.stdout.flush()
print('')
#contents that a user has downloaded
for idx, (u, item) in enumerate(user_download_rec.items()):
	for i in item:
		user_dict.get(u).add_item(i) #i is a tuple (item,downlaod time)
	print("{0:.1f}% \r".format(float((idx+1)/len(user_download_rec))*100), end='')
	sys.stdout.flush()
print('')

print("clean up")
for idx, (u,d) in enumerate(user_dict.items()):
	user_dict.get(u).duplicate_removal()
	print("{0:.1f}% \r".format(float((idx+1)/len(user_dict))*100), end='')
	sys.stdout.flush()

print("Save data")
save_obj(user_dict,'user_dict')

print("Finish updating user database")




