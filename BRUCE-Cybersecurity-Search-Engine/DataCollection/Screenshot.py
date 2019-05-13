from selenium import webdriver
from textblob.classifiers import NaiveBayesClassifier
from bs4.element import Comment
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from bs4 import BeautifulSoup
import pandas as pd
import requests 
from nltk.corpus import wordnet
import re
import html2text
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import lxml.html

DRIVER = '/usr/local/bin/chromedriver'
df = pd.read_csv(open('result3.csv','rU'),error_bad_lines=False,encoding='utf-8')

driver = webdriver.Chrome(DRIVER)
i = 0
while i < len(df):
	try:
	    df.URL[i] = df.URL[i].replace(' ','')
	    driver.get(df.URL[i])
	    screenshot = driver.save_screenshot(str(i)+'my_screenshot.png')
	    df.IMAGE[i] = '/scraping/'+str(i)+'my_screenshot.png'
	    i +=1
	except:
		df.IMAGE[i] = '/scraping/'+ 'failed'
		print(i)
		i +=1
df.to_csv('result2.csv', index = False)
driver.quit()
