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
  for x in membership_lst:
    if fuzz.partial_ratio(x.lower(), name.lower()) >= 90:
        return True
  return False

# Output
## is_member(name)
