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

