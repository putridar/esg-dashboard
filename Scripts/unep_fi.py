'''  
   File used to extract members of UNEP FI. From the extracted list, this file will determine whether a company is a member of UNEP FI
'''


# Install Relevant Libraries
# pip install openpyxl --upgrade --pre
# pip install fuzzywuzzy

# Import Libraries and UNEP FI data
import requests
import fuzzywuzzy as fw
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup

url = 'https://www.unepfi.org/members/'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
lst = soup.find_all("td")
membership_lst = []

for x in range(len(lst)):
  if x%5 == 0:
    curr = str(lst[x]).split('/">')[1]
    curr = curr.split("</")[0]
    membership_lst.append(curr)

## name = input("Input the company name: ")

# Function to detect UNEP FI members

def is_member_unepfi(name):
  '''  
   Function used to check whether a company is member of UNEP FI

   Parameters
   ----------
   arg1 : name
       Name of company

   Returns
   -------
   boolean
       True if a company is member of UNEP FI, False otherwise
   '''
  for x in membership_lst:
    if fuzz.partial_ratio(x.lower(), name.lower()) >= 90:
      return True
  return False

   

# Output
## is_member(name)
