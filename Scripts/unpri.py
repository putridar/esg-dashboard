# Install Relevant Libraries
# pip install openpyxl --upgrade --pre
# pip install fuzzywuzzy

# Import Libraries and UNPRI data
import pandas as pd
import fuzzywuzzy as fw
from fuzzywuzzy import fuzz
unpri = pd.read_excel("signatorydirectoryupdate05082021_681089.xlsx")

## name = input("Input the company name: ")

# Function to detect UNPRI members
def is_member(name):
  for x in unpri['Account Name']:
    if fuzz.partial_ratio(x, name) >= 82:
      return 'Yes'
  return 'No'

# Output
## is_member(name)
