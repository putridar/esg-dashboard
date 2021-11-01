import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.realpath("group18---natwest-firebase-adminsdk-r6242-f0f0ebcfbf.json")
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from urllib.request import Request, urlopen
import ssl

import nltk; nltk.download('stopwords')

# NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stop_words.extend(["copyright", "cookies"])

import pandas as pd
import numpy as np

import re
import string

import spacy

from PIL import __version__
from imp import reload

import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession

from bs4 import BeautifulSoup
import pdfplumber

import gensim
from gensim import corpora

from gensim.summarization import summarize, keywords
from gensim.summarization import mz_keywords

# libraries for visualization
import pyLDAvis
import pyLDAvis.gensim_models as gn
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
lda_model_tfidf2 = gensim.models.LdaMulticore.load("lda_model_tfidf0.h5")
lda_model_tfidf = gensim.models.LdaMulticore.load("lda_model_tfidf0 (1).h5")
def getPdfFromFirebase(company): #Will return a list pdf name
  #Configure connection with Firebase
  cred = credentials.Certificate("group18---natwest-firebase.json")
  try:
    firebase_admin.initialize_app(cred)
  except:
    pass
  db = firestore.client()
  doc_ref = list(db.collection("asian bank").get())
  ids = []
  for x in doc_ref:
    ids.append(x.id)
  data = {}
  for x in ids:
    doc = db.collection("asian bank").document(x).get()
    if doc.exists:
      curr = doc.to_dict()
      data[curr['company']] = curr['link']
  
  #Find Report
  pdf_name = []
  def download_file(pdf_name, download_url, filename):
    req = Request(download_url, headers={'User-Agent': 'Mozilla/5.0'})
    gcontext = ssl.SSLContext()
    try:
      webpage = urlopen(req, context=gcontext).read()
      file = open(filename + ".pdf", 'wb')
      file.write(webpage)
      file.close()
    except:
      pass
  for x in data.keys():
    if company in x.lower():
      train = data[x]
      break
  count = 1
  for x in list(train)[:1]:
    if company+'.pdf' in pdf_name:
      while company+str(count)+'.pdf' in pdf_name:
        count += 1
      company += str(count)
    pdf_name.append(company+str(count)+'.pdf')
    download_file(pdf_name, x, company+str(count))
    print(company+str(count)+'.pdf has been successfully downloaded')
  return pdf_name

def extract_pdf(pdf): #To extract pdf report
  x = len(pdf.pages)
  file_text = ""
  for i in range(x):
    page_text = pdf.pages[i].extract_text()
    if (page_text is not None):
      page_cleaned = " ".join(page_text.split())
      file_text += page_cleaned
  return file_text

# Cleaning
def sent_to_words(sentences):
  for sentence in sentences:
    yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc = True removes punctuations

# Define functions for stopwords, bigrams, and lemmatization
def remove_stopwords(texts):
  return [[word for word in gensim.utils.simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
  bigram = gensim.models.Phrases(texts, min_count=5, threshold=100)
  bigram_mod = gensim.models.phrases.Phraser(bigram)
  return [bigram_mod[doc] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
    for sent in texts:
      doc = nlp(" ".join(sent)) 
      texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out

def createCorpus(pdf_name): #receive input as the list
  # Read pdf and create corpus
  pdf_report = pdfplumber.open(pdf_name[0])
  pdf_report_text = extract_pdf(pdf_report)

  #Processing
  data_words = list(sent_to_words([pdf_report_text]))

  def make_bigrams(texts):
    bigram = gensim.models.Phrases(data_words, min_count=5, threshold=100)
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    return [bigram_mod[doc] for doc in texts]

  # Remove Stop Words
  data_words_nostops = remove_stopwords(data_words)

  # Form Bigrams
  data_words_bigrams = make_bigrams(data_words_nostops)

  # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
  # python3 -m spacy download en
  nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

  # Do lemmatization keeping only noun, adj, vb, adv
  data_lemmatized_input = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB'])
  id2word = corpora.Dictionary(data_lemmatized_input)
  inputCorpus = [id2word.doc2bow(text) for text in data_lemmatized_input]

  return inputCorpus #to be fed into the topic modelling

def get_topic_model(company):
  pdf_name = getPdfFromFirebase(company)
  inputCorpus = createCorpus(pdf_name)
  topic_dist = lda_model_tfidf[inputCorpus[0]]
  return topic_dist # Contains topic -> percentage in the form of a list of tuple

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
  stop_words = ["free newsletter","inbox","©",":","=","@", "copyright", "cookies","..","\xa0","min","redirecting…","seconds…"]
  for x in stop_words:
    if x in txt.lower():
      return False
  return True

def filter_txt(txt):
  stop_words = ["ii","&amp","{","deliver news","one-month","login","sign up","access to the news","captcha","sign in","?","free one-month trial","inbox","©",":","=","@", "copyright", "cookies","..","\xa0","min","redirecting…","seconds…"]
  for x in stop_words:
    if x in txt.lower():
      return False
  return True

def filter_link(link, company):
    filters = ["msci","watch","advertisement",".pdf","finance.yahoo","facebook","bloomberg"]
    curr = company.split(" ")
    parsed = ""
    for x in range(len(curr)):
        if x == 0:
            parsed += curr[x]
        else:
            parsed += "-" + curr[x]
    if company not in link.lower()and parsed not in link.lower():
        return True
    for x in filters:
        if x in link:
            return True
    return False

def make_corpus(text):
  #Processing
  data_words = list(sent_to_words([text]))
  # Remove Stop Words
  data_words_nostops = remove_stopwords(data_words)
  # Form Bigrams
  data_words_bigrams = make_bigrams(data_words_nostops)
  # Initialize spacy 'en' model, keeping only tagger component (for efficiency)
  # python3 -m spacy download en
  nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
  # Do lemmatization keeping only noun, adj, vb, adv
  data_lemmatized_input = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB'])
  id2word = corpora.Dictionary(data_lemmatized_input)
  inputCorpus = [id2word.doc2bow(text) for text in data_lemmatized_input]
  return inputCorpus

def get_summary(company):
  results = scrape(company + " esg")
  pdfs = []
  url = []
  for x in results:
    if filter_link(x, company):
        continue
    else:
      url.append(x)

  url.sort()
  links = []
  text = []
  final_list = []
  scores = []
  count = 0
  for x in url:
    try:
      page = requests.get(x)
      soup = BeautifulSoup(page.content, "html.parser")
      soup = str(soup.find_all('div')).split('>')
      main = x.split('/')
      text = list(set(filter(lambda x:"<br" in x or "</p" in x, soup)))
    except:
      continue

    text = list(filter(lambda x:filter_text(x), text))
    res = ""
    for sent in text:
      sent = sent.split("</p")[0]
      sent = sent.split("<br")[0]
      sent = sent.split("/n")[0]
      res += (sent.lower() + " ")
    corp = make_corpus(res)
    topic_result = lda_model_tfidf[corp[0]]
    topic_result.sort(key = lambda x:x[1], reverse = True)
    for x in topic_result:
      if (x[0] == 0 or x[0] == 2 or x[0] == 3 or x[0] == 7 or x[0] == 8) and x[1] >= 0.5:
        scores.append((topic_result[0][1],count))
        count += 1
        final_list.append(res)
        break
      elif (x[0]==5 and x[1] >= 0.2):
        scores.append((topic_result[0][1],count))
        count += 1
        final_list.append(res)
        break
      elif (x[0]==6 and x[1] >= 0.2):
        scores.append((topic_result[0][1],count))
        count += 1
        final_list.append(res)
        break
    #print(topic_result)
    #print(len(res))
  summ = []
  curr = 0
  scores.sort(key = lambda x:x[0], reverse = True)
  print(scores)
  final_list = list(set(final_list))
  final_res = final_list.copy()
  while final_list and len(summ) < 3:
    print(final_res[scores[curr][1]])
    try:
      summary_result = summarize(final_res[scores[curr][1]], ratio=0.1, word_count = 40)
    except:
      pass
    else:
      summ.append(summary_result)
    curr += 1
    final_list.pop(0)
  final_summary = ""
  for x in summ:
    temp = x.split("\n")
    temp_text = ""
    for y in temp:
      if not filter_txt(y):
        continue
      temp_text += y +"\n"
    final_summary = final_summary + (temp_text)
  print("Result:")
  print(final_summary)
  return final_summary
