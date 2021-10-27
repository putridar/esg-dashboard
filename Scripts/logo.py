from urllib.request import Request, urlopen
import ssl

import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

from bs4 import BeautifulSoup

def get_source(url):
    try:
        session = HTMLSession()
        response = session.get(url)
        return response
    except requests.exceptions.RequestException as e:
        print(e)

def scrape(q):
    q = urllib.parse.quote_plus(q)
    result = get_source("https://www.google.com/search?q=" + q)
    lst = list(result.html.absolute_links)
    exclude_domains = ('https://www.google.', 'https://google.', 'https://webcache.googleusercontent.', 'http://webcache.googleusercontent.', 'https://policies.google.',
                       'https://support.google.','https://maps.google.','https://www.instagram.','https://www.youtube.','https://translate.google.com','linkedin.com')
    links = lst.copy()
    for url in lst:
        for domain in exclude_domains:
            if domain in url:
                links.remove(url)
                break

    return links

def filter_link(link, company):
    filters = ["advertisement",".pdf","finance.yahoo","www."+company,company+".com"]
    if company not in link.lower():
        return True
    for x in filters:
        if x in link:
            return True
    return False


def get_logo(company):
    results = scrape(company + " logo")
    links = []
    text = []
    res = ""
    logo_list = []
    for x in results:
      if company not in x:
          continue
      try:
        page = requests.get(x)
        soup = BeautifulSoup(page.content, "html.parser")
        soup = str(soup.find_all('div')).split('>')
        main = x.split('/')
        res = list(set(filter(lambda x:company in x.lower() and "img" in x.lower(), soup)))[0]
        res = res.split('src="')[1]
        res = res.split('"')[0]
      except:
        continue
      if res[0] == "/":
        res = main[2] + res
    logo_list.append(res)
    print(logo_list)
    return logo_list
