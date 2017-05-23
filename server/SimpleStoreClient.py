##########################################
# The real Spider impl. 
# This is a sinple spider implementation that support:
#  a) Auto pagination
#  b) Auto text extraction.
###########################################
import requests
from bs4 import BeautifulSoup
import pdb
from fake_useragent import UserAgent
ua = UserAgent()

class SimpleSoreClient:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, unique_key):
      self.name = name
      self.unique_key = unique_key
   
   def get(self):
     pass

   def post(self):
      print "Name : ", self.name,  ", Salary: ", self.salary

import requests
URL ='http://52.89.112.230/api/banglagossip'
r = requests.post(URL, json={"url": d.url,"_cmd":"search"})
if r.status_code ==200 and len(r.json()['out']):
    print 'adding'
    d['_cmd'] ='post'
    r = requests.post(URL, json=d)
else:
    print 'duplicate found'
print r.json()