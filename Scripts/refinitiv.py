import json
import requests
from bs4 import BeautifulSoup

def name_to_ticker(name):
  try:
    url = 'https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&sortBy=&dateRange=&search=' + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return str(soup.find_all("td")[1])[4:-5]
  except:
    return 'NA'

def name_to_name(name):
  try:
    url = 'https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&sortBy=&dateRange=&search=' + name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return str(soup.find_all("td")[0])[4:-5]
  except:
    return 'NA'

def RefinitivOutput(company_name):
  # If we don't find the ticker, output NA
  if name_to_ticker(company_name) == 'NA':
    return 'NA'
  # If we find the ticker, output the ESG details
  else:
    URL = "https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode=" + name_to_ticker(company_name)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    dictionary = json.loads(str(soup))
    print("Company Name: " + name_to_name(company_name))
    print("Industry Type: " + str(dictionary['industryComparison']['industryType']))
    print("ESG Score: " + str(dictionary['esgScore']['TR.TRESG']['score']))
    print("Rank in Industry: " + str(dictionary['industryComparison']['rank']) + "/" + str(dictionary['industryComparison']['totalIndustries']))
    print("-----------------------------------")
    print("Environment Score: " + str(dictionary['esgScore']['TR.EnvironmentPillar']['score']))
    print("Emission Score: " + str(dictionary['esgScore']['TR.TRESGEmissions']['score']))
    print("Resource Use Score: " + str(dictionary['esgScore']['TR.TRESGResourceUse']['score']))
    print("Innovation Score: " + str(dictionary['esgScore']['TR.TRESGInnovation']['score']))
    print("-----------------------------------")
    print("Social Score: " + str(dictionary['esgScore']['TR.SocialPillar']['score']))
    print("Human Rights Score: " + str(dictionary['esgScore']['TR.TRESGHumanRights']['score']))
    print("Product Responsibility Score: " + str(dictionary['esgScore']['TR.TRESGProductResponsibility']['score']))
    print("Workforce Score: " + str(dictionary['esgScore']['TR.TRESGWorkforce']['score']))
    print("Commmunity Score: " + str(dictionary['esgScore']['TR.TRESGCommunity']['score']))
    print("-----------------------------------")
    print("Governance Score: " + str(dictionary['esgScore']['TR.GovernancePillar']['score']))
    print("Management Score: " + str(dictionary['esgScore']['TR.TRESGManagement']['score']))
    print("Shareholders Score: " + str(dictionary['esgScore']['TR.TRESGShareholders']['score']))
    print("CSR Strategy Score: " + str(dictionary['esgScore']['TR.TRESGCSRStrategy']['score']))
    return

def RefinitivList(company_name):
  # If we don't find the ticker, output NA
  if name_to_ticker(company_name) == 'NA':
    return 'NA'
  # If we find the ticker, output the ESG details
  else:
    URL = "https://www.refinitiv.com/bin/esg/esgsearchresult?ricCode=" + name_to_ticker(company_name)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    dictionary = json.loads(str(soup))
    result = []
    result.append("Company Name: " + name_to_name(company_name))
    result.append("Industry Type: " + str(dictionary['industryComparison']['industryType']))
    result.append("ESG Score: " + str(dictionary['esgScore']['TR.TRESG']['score']))
    result.append("Rank in Industry: " + str(dictionary['industryComparison']['rank']) + "/" + str(dictionary['industryComparison']['totalIndustries']))
    result.append("-----------------------------------")
    result.append("Environment Score: " + str(dictionary['esgScore']['TR.EnvironmentPillar']['score']))
    result.append("Emission Score: " + str(dictionary['esgScore']['TR.TRESGEmissions']['score']))
    result.append("Resource Use Score: " + str(dictionary['esgScore']['TR.TRESGResourceUse']['score']))
    result.append("Innovation Score: " + str(dictionary['esgScore']['TR.TRESGInnovation']['score']))
    result.append("-----------------------------------")
    result.append("Social Score: " + str(dictionary['esgScore']['TR.SocialPillar']['score']))
    result.append("Human Rights Score: " + str(dictionary['esgScore']['TR.TRESGHumanRights']['score']))
    result.append("Product Responsibility Score: " + str(dictionary['esgScore']['TR.TRESGProductResponsibility']['score']))
    result.append("Workforce Score: " + str(dictionary['esgScore']['TR.TRESGWorkforce']['score']))
    result.append("Commmunity Score: " + str(dictionary['esgScore']['TR.TRESGCommunity']['score']))
    result.append("-----------------------------------")
    result.append("Governance Score: " + str(dictionary['esgScore']['TR.GovernancePillar']['score']))
    result.append("Management Score: " + str(dictionary['esgScore']['TR.TRESGManagement']['score']))
    result.append("Shareholders Score: " + str(dictionary['esgScore']['TR.TRESGShareholders']['score']))
    result.append("CSR Strategy Score: " + str(dictionary['esgScore']['TR.TRESGCSRStrategy']['score']))
    return result

