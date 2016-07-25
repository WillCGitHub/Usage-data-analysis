from User import *
import pickle
from collections import Counter
import re
import sys
from statistics import mean




def load_obj(name):
    with open('userdb/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def save_obj(obj, name):
    with open('userdb/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def deleteParenthesis(input_text):
	regEx = re.compile(r'([^\(]*)\([^\)]*\) *(.*)')
	m = regEx.match(input_text)
	while m:
	  input_text = m.group(1) + m.group(2)
	  m = regEx.match(input_text)
	return input_text

country_code = load_obj('country_dict')

def feature_extraction(userObj):
	"""
	features:
	[# of items downloaded, # of sources, # of session id, 
	visit time hour, visit time day, ]
	"""
	features = [0,0,0,0,0] 





	features[0] = len(userObj.items)

	features[1] = len(userObj.source)

	features[2] = len(userObj.session_id)

	mean_visit_time= mean([a.hour for a in userObj.event_time])
	features[3] = mean_visit_time

	mean_visit_day = mean([a.day for a in userObj.event_time])
	features[4] = mean_visit_day





	return features

	


print("load db")
ud = load_obj('user_dict')

features = []
labels = []


counter = 0
for u, d in ud.items():
	if d.category != 9:
		labels.append(d.category)
		features.append(feature_extraction(d))


X = features
y = labels
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = .5)

from sklearn.neighbors import KNeighborsClassifier

clf = KNeighborsClassifier(n_neighbors = 10, algorithm = 'auto' )
clf.fit(X_train,y_train)
predictions = clf.predict(X_test)

from sklearn.metrics import accuracy_score
print(accuracy_score(y_test,predictions))






