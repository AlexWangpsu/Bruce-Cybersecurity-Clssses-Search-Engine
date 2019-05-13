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
from interruptingcow import timeout

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

def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return (" & ").join([re.sub(r'\D', '', number) for number in phone_numbers])

def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    a = r.findall(string)
    b = []
    for i in a:
        if i not in b:
            b.append(i)
    return (" & ").join(b)

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

def get_title(url):    
    soup =  BeautifulSoup(url,'html.parser')
    title = soup.find('title').text
    return title




j = 0
i=1
train = []
j = []
df = pd.read_csv("download_dir.csv", header = None,error_bad_lines=False,encoding='utf-8')
tf = pd.read_csv("FORAY.csv", error_bad_lines=False,encoding='utf-8')
new1 =[]
af  = pd.read_csv("OMG.csv", error_bad_lines = False,  encoding = 'utf-8')

while i < len(df):
    try:
        
        if df[0][i] != '':
            html = re.sub(r'[\W_]+', ' ',str(df[2][i]))
            after =  get_doc(html)
        if df[1][i] != 'Y':
            if df[1][i] != 'N':
                i+=1
                continue
        print(after)
        if isinstance(df[1][i], float):
            i +=1
            j +=1
            continue
        print(df[1][i], df[2][i])
        train.append((after,df[1][i]))
        i += 1
    except:
        print(i,'this is failed')
        i+=1 
        pass
    
i  = 0
#df.to_csv("TRAINEDCONTENT.csv",encoding='utf-8',mode = 'w', index=False)


while i <len(af):
    try:
        print(af.URL[i])
        html = af.TITLE[i]
        if af.URL[i] != '':
            html = re.sub(r'[\W_]+', ' ',str( html))
            after =  get_doc(html)
        print(after)
        train.append((after,af.CLASS[i]))
        i +=1
    except:
        i += 1
        print(i)
print(j)
what =  NaiveBayesClassifier(train)
i= 0
while i < 10:
    try:
        if 'pdf' in tf.URL[i]:
            i += 1
            continue
        if 'doc' in tf.URL[i]:
            i += 1
            continue
        if 'docs'in tf.URL[i]:
            i += 1
            continue
        if 'ppt' in tf.URL[i]:
            i+= 1
            continue
        if 'pptm' in tf.URL[i]:
            i+=1
            continue
        with timeout(3, exception=RuntimeError):

            print(  tf.URL[i])
            tf.URL[i] = tf.URL[i].replace(' ','')
            tf.DOMAIN[i] = domain_finder(tf.URL[i])
            req = requests.get(tf.URL[i],  headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'})
            content_type = req.headers.get('content-type')
            if 'text/html' not in content_type :
                i += 1
                print('this is passed')
                tf.CLASS[i] = "FAILED"
                continue
            print(content_type)
            tf.TITLE[i] = get_title(req.text)
            print(tf.TITLE[i])
            html = html2text.html2text(req.text)
            tf.YEAR[i] = year_finder(html)
            tf.NAME[i] = get_continuous_chunks(html)
            tf.PHONE[i] = extract_phone_numbers(html)
            tf.EMAIL[i] =extract_email_addresses(html)
            html = get_title(req.text)
            html = re.sub(r'[\W_]+', ' ',str( html))
            after =  get_doc(html)
            print('trying to classify')
        tf.CLASS[i]  = what.classify(after)
        print(i,what.classify(after))
        print('this is case',i)
        i+=1
    except:
        j.append(i)
        tf.CLASS[i] = "FAILED"
        i+=1
        print(i,'failed')
        pass
   
    
  
tf.to_csv('new.csv',encoding='utf-8',mode = 'w', index=False)
print(j)
 

