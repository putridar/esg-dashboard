'''  
   File used to extract members of IIGCC. From the extracted list, this file will determine whether a company is a member of IIGCC
'''

# Install Relevant Libraries
# pip install openpyxl --upgrade --pre
# pip install fuzzywuzzy

# Import Libraries and UNEP FI data
import json
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
import browser_cookie3

def is_member_iigcc(name):
   '''  
   Function used to check whether a company is member of IIGCC

   Parameters
   ----------
   arg1 : name
       Name of company

   Returns
   -------
   boolean
       True if a company is member of IIGCC, False otherwise
   '''
  url = 'https://www.iigcc.org/about-us/our-members/'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  for x in soup.find_all("a"):
    if len(x.contents) == 0 or isinstance(x.contents[0], str) == False:
      continue
    if fuzz.partial_ratio(x.contents[0].lower(), name.lower()) >= 90:
      print(x.contents[0].lower())
      return True
  return False

