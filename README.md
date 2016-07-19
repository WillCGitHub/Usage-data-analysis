# Usage-data-analysis

##2 New Data Structure
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
To easily handle this expression, I use TimeCell. It automatically decopose the expression and make it hashable. 

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
TimeCell is hashable but it's based on same day
"""
visit_time_list = [a,b,c,d,e,f,g] # a list of TimeCell objects 
#a,b,c are from July 18 but different hours, e,f,g from July 19 but different hours
from collections import Counter
Counter(visit_time_list)
>>> Counter({7/18/16: 3, 7/19/16: 3})
```
