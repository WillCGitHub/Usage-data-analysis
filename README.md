# Usage-data-analysis
- Analyze.py: data cleaning
- UserAnalysis.py: data analysis
- [Daily.py, MultiDays.py](https://github.com/WillCGitHub/OECD-Daily-analysis) 
- User.py: new data structures for handling the data
- UserDict.py: creat a user hashmap for easy lookup 
- Main.py: manage all above

##Sample Usage
```terminal
>>> python3 Main.py -a month -y true
optional arguments
-a pass in the arguments of analysis interval
    possible arguments:
    - month
    - 16/7 (year/month)
    - None 
-y pass in a boolean type argument, whether conduct year_analysis or not
```
The program will ask you whether you'd like to update the user database. Enter y to update. 

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
us.ISE(year_analysis = False) #year_analysis is an optional argument, boolean type
ua.average_visit() #return a float number 

```
##3 New Data Structures
User.py includes User() and TimeCell(), UserAnalysis.py includes AnalysisFrame()
###User
Each user has several attributes
- Identity ID
- IP address
- Session ID
- User agent
- Items downloaded
- Visit time
- Referral source
User class can handle them all easily. 
```python
#instantiate a new User class
user1 = User('idXXX') 

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

#Add user agent
user_agent = "XXXX"
user1.add_user_agent(user_agent)

#Add source
source = "XXXXX"
user1.add_source(source)

#Duplicate removal
user1.duplicate_removal() # remove duplicate entries

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
