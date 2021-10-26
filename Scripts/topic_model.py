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

import pandas as pd
import numpy as np

import re
import string

import spacy

from PIL import __version__
from imp import reload


import pdfplumber

import gensim
from gensim import corpora

# libraries for visualization
import pyLDAvis
import pyLDAvis.gensim_models as gn
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline

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
  lda_model_tfidf = gensim.models.LdaMulticore.load("lda_model_tfidf0.h5")
  topic_dist = lda_model_tfidf[inputCorpus[0]]
  return topic_dist # Contains topic -> percentage in the form of a list of tuple
