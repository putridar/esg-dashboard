'''  
   File used to extract members of ICMA. From the extracted list, this file will determine whether a company is a member of ICMA
'''

# Install Relevant Libraries
# pip install openpyxl --upgrade --pre
# pip install fuzzywuzzy

# Import Libraries and ICMA
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

url = 'https://www.icmagroup.org/sustainable-finance/membership-governance-and-working-groups/membership/'
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
icma_lst = soup.find_all("td")
icma_membership_lst = []
for x in range(len(icma_lst)):
   if x%5 == 0:
     curr = icma_lst[x].text.rstrip()
     icma_membership_lst.append(curr)

## name = input("Input the company name: ")

# Function to detect UNEP FI members

def is_member_icma(name):
   '''  
   Function used to check whether a company is member of ICMA

   Parameters
   ----------
   arg1 : name
       Name of company

   Returns
   -------
   boolean
       True if a company is member of ICMA, False otherwise
   '''
  for x in icma_membership_lst:
    if fuzz.partial_ratio(x.lower(), name.lower()) >= 90:
        return True
  return False

# Output
## is_member(name)
