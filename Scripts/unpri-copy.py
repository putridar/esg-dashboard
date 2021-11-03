'''  
   File used to extract members of UNPRI. From the extracted list, this file will determine whether a company is a member of UNPRI
'''

# Install Relevant Libraries
# pip install openpyxl --upgrade --pre
# pip install fuzzywuzzy

# Import Libraries and UNPRI data
import pandas as pd
import fuzzywuzzy as fw
from fuzzywuzzy import fuzz
unpri = pd.read_excel("signatorydirectoryupdate05082021_681089.xlsx")

# Function to detect UNPRI members
def is_member(name):
   '''  
   Function used to check whether a company is member of UNPRI

   Parameters
   ----------
   arg1 : name
       Name of company

   Returns
   -------
   boolean
       True if a company is member of UNPRI, False otherwise
   '''
  for x in unpri['Account Name']:
    if fuzz.partial_ratio(x.lower(), name.lower()) >= 95:
      return True
  return False

# Output
## is_member(name)
