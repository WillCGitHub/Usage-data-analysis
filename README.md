# Usage-data-analysis

######Note:
```
These scripts are built and work under Python3.5 MacOSX/Linux. Some of the scripts use the moldel 
Multiprocessing which does not support Windows. 
To use this scripts, Anaconda is probably the best option because of the scripts' dependency on 
many other packages and Anaconda includes all of them. 

All used pakages are listed here:
- Numpy
- Scipy
- Pandans
- User
- openpyxl
- ua_parser
- requests
```

Main.py and ClassifyGuest.py are two top level scripts,
which calls on other scripts to conduct analysis.

- CategoryDict.py : Profile code dictionary
- Classify.py : Classify registered users
- ClassifyGuest.py : Use KNN to Classify guest users
- DataManagement.py : automaticaly update data
- FeatureExtraction.py : Extract features from strings
- Main.py: Conducting yearly analysis
- User.py: new data structures for handling the data
- UserAnalysis.py: data analysis
- UserProfile.py : link registered ID with CU_number

######Note:
Main.py needs the following:
- dataset: Daily data
- result: A folder contains results
- userdb: A folder contains pkl files


##Sample Usage
```terminal
>>> python3 Main.py -a month -y true
#This command will conduct monthly analysis between different years
optional arguments
-a pass in the arguments of analysis interval
    possible arguments:
    - month
    - 16/7 (year/month)
    - None 
-y pass in a boolean type argument, whether conduct year_analysis or not
```
The program will ask you whether you'd like to update the user database. Enter y and then hit enter to update. 


ClassifyGuest Class
```python
from ClassifyGuest import ClassifyGuest
daily_file_path = "XXX/XXX.csv"
gc = ClassifyGuest(daily_file_path)
gc.train()
gc.predict()#automaticaly produce result.csv 
```


UserAnalysis.py
```python

"""
UserAnalysis() class could pass in key word arguments 
optional argument analysis_interval, and it could be customized using the format(Year/month)
for example, ua = UserAnalysis(user1, analysis_interval = "16/6") this will proceed a month analysis on the data 
in 2016 june.
user1 is a User object, see below to check out User() class
"""
ua = UserAnalysis(user1, analysis_interval = "month")  

ua.moving_means() #return a list of AnalysisFrame object

ua.centered_moving_means() #return a list of AnalysisFrame object

ise_dict = us.ISE(year_analysis = False) #year_analysis is an optional argument, boolean type
#ise_dict is a dictionary {"time label":<AnalysisFrame Object>}

ave_m_e = ua.average_month_effect(ise_dict)
#this will return a dictionary {"month":average visit(dtype: float)}

ave_v = ua.average_visit() #average visit per month

u_exp = ua.usage_expectation(ave_m_e,ave_v) #expectation per month

```
##3 New Data Structures
User.py includes User() and TimeCell(), UserAnalysis.py includes AnalysisFrame()
###User
Each user has several attributes
- Identity ID
- IP address
- Session ID
- Useragent
- Items downloaded
- Visit time
- Referral source
- CU_number
- Geographical infomation
- Category


User class can handle them all easily. 
```python
#instantiate a new User class
user1 = User('idXXX') 

#all the attributes are holds in a dictionary

#to access
user1.identity_dict

#Add ip address 
IP = "192.168.1.1"
user1.ip_add += IP

#Add visit time
t = "19-JUL-16 12.00.02.888535 AM" 
user1.add_visit(t)

#Add items
item = ("item id", "19-JUL-16 12.00.02.888535 AM") # item has to be a tuple that keeps id and download time
user1.add_item(item)

#Add session id
session_id = "XXXXXX"
user1.add_session_id(session_id)



#sort visit
"""
sort_visit() method could pass in key word arguments
sort_by:
    -day
    -month
    -or a customized argument in the format of (Year/Month), for example 16/6 2016 June
"""
visit_frequency = user1.sort_visit()  #return a sorted list (with frequency)
```
###TimeCell
This data struecture is for time series analysis

Sample time expression "19-JUL-16 12.00.02.888535 AM" 

Use TimeCell to easily handle this expression. It automatically decoposes the expression and make it hashable. 

```python
t_expr = "19-JUL-16 12.00.02.888535 AM"
t = TimeCell(t_expr)
"""
Attribute to access:
- Year | t.year
- Month | t.month
- Day | t.day
- Hour | t.hour
- Minute | t.minute
- Second | t.second
"""
t.check_identity()
>>>(16, 7, 19, 0, 0, 2) #year,month,day,hour,minute,second

t.check_month() #return a year/month string (16/7)
"""
TimeCell is hashable but it's based on day range instead of accurate time point.
"""
from collections import Counter

visit_time_list = [a,b,c,d,e,f,g] # a list of TimeCell objects 
#a,b,c are from July 18 but different hours, e,f,g are from July 19 but different hours

Counter(visit_time_list)
>>> Counter({7/18/16: 3, 7/19/16: 3})
```
###AnalysisFrame
AnalysisFrame class holds the data with labels, analysis type and the data.Much easier to classify and analyze data

```python
#User needs to pass in 3 arguments(time_label, analysis_label, data)
#time_label could be TimeCell type
data = AnalysisFrame("16/7/21", "time series analysis", "0.05")
```
