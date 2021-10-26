from urllib.request import Request, urlopen
import ssl

import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

from bs4 import BeautifulSoup
import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(["copyright", "cookies"])
from gensim.summarization import summarize, keywords
from gensim.summarization import mz_keywords

"""
Command to install:
pip install gensim==3.6.0 --user
pip install bs4
pip install requests_html
pip install requests==2.23.0 --user
pip install nltk==3.2.5 --user
pip install urllib3==1.25.11 --user
"""

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

def filter_text(txt):
    stop_words = ["inbox","©",":","=","@","[","#", "copyright", "premium content", "cookies","..","\xa0","min","Redirecting…","seconds…"]
    for x in stop_words:
        if x in txt.lower():
            return False
    return True

def remove_stopwords(sen):
    sen = sen.split(" ")
    sen_new = [i for i in sen if i not in stop_words]
    return sen_new
def filter_link(link, company):
    filters = ["watch","advertisement",".pdf","finance.yahoo","facebook","bloomberg"]
    if company not in link.lower():
        return True
    for x in filters:
        if x in link:
            return True
    return False
def get_summary(company):
    results = scrape(company + " esg")
    dfs = []
    url = []
    for x in results:
      if filter_link(x, company):
        continue
      else:
        url.append(x)

    url.sort()
    links = []
    text = []
    for x in url:
      try:
        page = requests.get(x)
        soup = BeautifulSoup(page.content, "html.parser")
        soup = str(soup.find_all('div')).split('>')
        main = x.split('/')
        text.extend(list(set(filter(lambda x:"<br" in x or "</p" in x, soup))))
      except:
        continue

    text = list(filter(lambda x:filter_text(x), text))
    res = ""
    for sent in text:
      sent = remove_stopwords(sent)
      for x in range(len(sent)):
        sent[x] = sent[x].split("</p")[0]
        sent[x] = sent[x].split("<br")[0]
        sent[x] = sent[x].split("/n")[0]
      for x in sent:
        res += (x.lower() + " ")

    #print(len(res))
    #print(res)
    clean_sentences = res
    return summarize(clean_sentences, ratio=0.1, word_count = 50)
