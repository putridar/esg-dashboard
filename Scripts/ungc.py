'''  
   File used to extract members of UNGC. From the extracted list, this file will determine whether a company is a member of UNGC
'''

# Install Relevant Libraries
# pip install openpyxl --upgrade --pre
# pip install fuzzywuzzy

# Import Libraries and UNEP FI data
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

'''  
   Function used to check whether a company is member of UNGC

   Parameters
   ----------
   arg1 : name
       Name of company

   Returns
   -------
   boolean
       True if a company is member of UNGC, False otherwise
'''

def is_member_ungc(name):
  name = name.replace(' ', '+').lower()
  url = 'https://www.unglobalcompact.org/what-is-gc/participants/search?utf8=%E2%9C%93&search%5Bkeywords%5D=' + name + '&button=&search%5Bper_page%5D=50&search%5Bsort_field%5D=&search%5Bsort_direction%5D=asc'
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  lst = soup.find_all("th", {"class": "name"})[1:]
  for x in lst:
    a = x.findChild("a")['href'][32:].lower()
    a = a.replace('-', ' ')
    if fuzz.partial_ratio(a, name) >= 90:
      return True
  return False

# Output
## is_member(name)
