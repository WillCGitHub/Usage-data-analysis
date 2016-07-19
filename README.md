# Usage-data-analysis
- Analyze.py: data cleaning
- UserAnalysis.py: data analysis
- [Daily.py, MultiDays.py](https://github.com/WillCGitHub/OECD-Daily-analysis) 
- User.py: new data structures for handling the data
- UserDict.py: creat a user hashmap for easy lookup 
- Main.py: manage all above

##Sample Usage
```terminal
>>> python3 Main.py
```
The program will ask you whether you'd like to update the user database. Enter y to update. 

UserAnalysis.py
```python
ua = UserAnalysis(user1) #user1 is a User object, see below to check out User() class
ua.visit_freq  #returns a sorted list that show how frequent the user visits
if len(ua.visit_freq) > 3:  #only check users who visit the site at least in 3 different days
  mm = ua.moving_means() 
  cmm = ua.centered_moving_means()
  ise = ua.ISE()
  ave_v = ua.average_visit() #average visit per day
```
##2 New Data Structures
Both data structures are in User.py
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

#Duplicate removal
user1.duplicate_removal() # remove duplicate entries

#sort visit
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

"""
TimeCell is hashable but it's based on day range instead of accurate time point.
"""
from collections import Counter

visit_time_list = [a,b,c,d,e,f,g] # a list of TimeCell objects 
#a,b,c are from July 18 but different hours, e,f,g are from July 19 but different hours

Counter(visit_time_list)
>>> Counter({7/18/16: 3, 7/19/16: 3})
```
