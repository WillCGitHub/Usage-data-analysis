from User import *
import pickle
from UserAnalysis import UserAnalysis
from openpyxl import load_workbook
import copy
import sys
import csv
import string
from collections import Counter



def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('userdb/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def classify_category(name):
	classify_dict = dict()
	university = ["university","universidad","college","universidade","school",
					"education","uniwersytet","daigaku","sciences","hochschule",
					"universite","academy", "univ", "université", "universität",
					"universiti","universita","studi","studies","institut",
					"universitäts","universitaet","Üniversitesi","Institutt",
					"Universiteit","institute","Universitesi","Universities",
					"Universitat","universitet"]
	gov = ["administration","government","ministry","federal","association",
			"public","national"]
	think_tank = ["accenture"]
	library = ["biblioteca",
				"bibliotek",
				"bibliothek",
				"bibliotheque",
				"bibliothèque",
				"libraries",
				"library"]
	private_industry = ["ltd", "inc","consortium","corporation", "co"]
	media = ["new york times"]
	bank = ["bank","banco", "bnp paribas","morgan stanley"]
	int_org = ["un", "oecd", "int", "international","unicef"]
	consulting_company = ["ernst", "kpmg","bain and company",
							"mckinsey & company inc","deloitte"]
	for u in university:
		classify_dict[u.lower()] = 0
	for g in gov:
		classify_dict[g] = 1
	for p in private_industry:
		classify_dict[p] = 2
	for m in media:
		classify_dict[m] = 3
	for th in think_tank:
		classify_dict[th] = 4
	for l in library:
		classify_dict[l] = 5
	for b in bank:
		classify_dict[b] = 6
	for io in int_org:
		classify_dict[io] = 7
	for cc in consulting_company:
		classify_dict[cc] = 8

	t = dict()
	for p in string.punctuation:
		t[p] = " "
	#translate punctuation to space
	table = str.maketrans(t)
	name = name.translate(table)
	r = classify_dict.get(name.lower())

	if r is not None:
		return r

	average_result = []

	for n in reversed(name.split(" ")):
		temp = classify_dict.get(n)
		if temp == 0:
			return temp
		if temp is not None:
			average_result.append(temp)

	if len(average_result) > 0:
		if len(average_result) == 1:
			return average_result[0]
		c = Counter(average_result).most_common(10)

		if len(c) ==1:
			return c[0][0]
		elif len(c) > 1:
			if c[0][1] != c[1][0]:
				return c[0][0]
			else:
				return average_result[0]

	else:
		return 9







print("load db")
ud = load_obj('user_dict')

wb = load_workbook(filename = 'registrations/iLibrary_registrations_21jul2016.xlsx',read_only=True)
ws = wb['Sheet1']

id_info = dict()

for idx, row in enumerate(ws.rows):
	if id_info.get(row[1].value) is None:
		"""
		0 - name
		3 - e-mail
		9 - country
		10 - CU number 
		"""
		id_info[row[1].value] = (row[0].value,
								row[3].value,
								row[9].value,
								row[10].value)
	print("Loading {0:.1f}% ... \r".format((idx/(ws.max_row-1))*100), end="")
	sys.stdout.flush()

print("\n")
r = []
for u, d in ud.items():
	d.user_name = id_info.get(u)[0]
	d.email = id_info.get(u)[1]
	d.geo = id_info.get(u)[2]
	d.CU_number = id_info.get(u)[3]
	n = copy.deepcopy(d.user_name)
	n = n.lower()
	d.category = classify_category(n)
	r.append((d.user_name,d.category))
	#print("name: {}, category: {}".format(d.user_name,d.category))
def getkey(item):
	return item[1]
save_obj(ud,'user_dict')
r = sorted(r,key=getkey)
with open("category_result.csv", 'w') as f:
	writer = csv.writer(f, delimiter = ",")
	writer.writerow(["name","category"])
	for a in r:
		writer.writerow([a[0],a[1]])









