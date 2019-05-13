#from textblob.classifiers import NaiveBayesClassifier
# Make sure this stuff is imported beforehand, python should warn you
from bs4.element import Comment
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from bs4 import BeautifulSoup
import pandas as pd
import requests 
from nltk.corpus import wordnet
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import csv
import urllib
import html2text
import requests 
#Author: Weiqin Wang 
#Date May 01 2019 


# Using NLTK Named entity extraction to extract name 
# Compared with a name datababse to finally return the name 
def get_continuous_chunks(text):
    new =[]
    newlist = []
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []
    new = []
    new_last =[]

    sf = pd.read_csv("CSV_Database_of_First_Names.csv", header = None)
    gf = pd.read_csv("CSV_Database_of_Last_Names.csv", header = None)
    for i in range(len(sf)):
       new.append(sf[0][i])
       
    for j in range(len(gf)):
        new_last.append(gf[0][j])

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue

    if continuous_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            continuous_chunk.append(named_entity)
    person_list = continuous_chunk
    for person in person_list:
        person_split = person.split(" ")
        a = ''
        b = 0
        c = 0 
        for name in person_split:
            d = 1
            if len(name) == 0:
                continue 
            if wordnet.synsets(name):
                
                if name in new:
                    d = 0
                    
                if name in new_last:
                    d = 0
                            
                if name in new and b == 0:
                    b = 1
                if name in new_last:
                    c = 1 

                if d == 0 and b == 1 :
                    a += str(name) + ' '
                    b += 1
                    continue 
                if d == 0 and b ==2:
                    if 0< c <= 2 :
                        if name not in a:
                    
                            a += str(name) + ' '
                            c +=1

            elif any(x for x in name if x.isdigit()):
                continue
            elif name.isupper():
                continue 
            else:
                if name not in a :
                    a += str(name) +' '
        
        newlist.append(a)
    new_list = [] 
    for i in newlist:
        split = i.split(" ")
        if len(split) > 2 and i not in new_list:
            new_list.append(i)

    return ('& ').join(new_list)
# Uses regex for phone numbers
def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return (" & ").join([re.sub(r'\D', '', number) for number in phone_numbers])
# Uses regex for email addresses
def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    a = r.findall(string)
    b = []
    for i in a:
        if i not in b:
            b.append(i)
    return (" & ").join(b)


# Uses some simple string manipulation to get the domain name
# After the switch to conferencefinder which goes to the professor personal websites, another method needs to be found
def domain_finder(row):
    row = str(row)
    loc = row.find(".edu")
    row = row[:loc]
    doc = row.rfind(".")
    row = row[doc+1:]
    dashdoc = row.rfind("/")
    row = row[dashdoc+1:]
    row = row.upper()
    return str(row)

# Finding year with regex
def year_finder(text):
    m = re.compile('(Fall|Spring|Summer)\s20(0|1)\d{1}')
    fina = m.search(text)
    if fina is None:
        m = re.compile('(20(0|1)\d{1}\s(Fall|Spring|Summer))')
        m.search(text)
    if fina is None:
        m = re.compile('20\d{2}-20(0|1)\d{1}')
        finados = m.search(text)
        if finados is None:
            m = re.compile('20(0|1)\d{1}')
            finatres = m.search(text)
            if finatres is None:
                return "None"
            else:
                return finatres.group(0)               
        else:
            return finados.group(0)
    else:
        return fina.group(0)

# parses out the unimportant words from a doc
def get_doc(data):
    new_list = []
    data = data.split()
    stopword_set = set(stopwords.words('english'))
    mystemmer = PorterStemmer()
    mylmtzr = WordNetLemmatizer()
    for d in data:      
        d = d.lower()
        if d not in stopword_set:
            d = mylmtzr.lemmatize(d)
            d = mystemmer.stem(d)
            new_list.append(d)
    return " ".join(new_list)
# Regex for title
def get_title(url):    
    soup =  BeautifulSoup(url,'html.parser')
    title = soup.find('title').text
    return title
# Regex for textbook
def get_textbook(text):
    tb = re.compile('.*ISBN.*|.*Edition.*|.*edition.*|.*, [A-Z]\..*')
    textbooks = ""
    if tb.search(text) != None:
        li = tb.findall(text)
        for textbook in li:
            textbooks += '\n'+ textbook
    return textbooks
# Regex to see if the professor has these elements listed for the course
def get_tests(text):
    fe = re.compile('Final Exam|Final exam')
    mid = re.compile('Midterm|Mid-term')
    proj = re.compile('Project')
    quiz = re.compile('Quiz|quiz')
    pres = [False, False, False, False]
    if fe.search(text) != None:
        pres[0] = True
    if mid.search(text) != None:
        pres[1] = True
    if proj.search(text) != None:
        pres[2] = True
    if quiz.search(text) != None:
        pres[3] = True
    return pres

# Read csv of links to the coursepages. Then, use html2text and requests modules to get the no-HTML markdown text of the website.
# Then use the above functions to place the information into a dataframe (pandas module), and then write to whatever csv
# Recommend that the end csv is dated to avoid confusion with multiple versions.

df = pd.read_csv("Final.csv",error_bad_lines=False,encoding='utf-8')
i = 0
while i <len(df):

    try:
        #row[0] = row[0].replace(' ','')
        print(i)
        url = str(df.URL[i])
        url = url.replace(' ','')
        
        req = requests.get(url,  headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
        
        t = html2text.HTML2Text()
        t.ignore_links=True
        t.ignore_images=True
        text = t.handle(req.text)
        
        df.DOMAIN[i] = (domain_finder(url))
        
        df.TITLE[i]= (get_title(req.text))
        df.YEAR[i]=(year_finder(text))
        df.PROF[i]=(get_continuous_chunks(text))
        df.PHONE[i]=(extract_phone_numbers(text))
        df.EMAIL[i]=(extract_email_addresses(text))
        df.CONTENT[i]=([text])
        
        df.TEXTBOOK[i]=(get_textbook(text))
        
        df.TEST[i]=(get_tests(text))
        
        print(df.TITLE[i])
        print('_____________')
        i+=1
    
    except Exception as e:
        i+=1
        print(e)
        continue
    
df.to_csv('mar1819courses.csv', index = False)
