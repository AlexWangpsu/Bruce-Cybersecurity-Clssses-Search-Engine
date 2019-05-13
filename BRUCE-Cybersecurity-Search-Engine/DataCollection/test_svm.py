import re

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
import pandas as pd
import numpy as np
from sklearn.model_selection import learning_curve

'''
This script accept input as csv file with url , label, content, title columns'
'''

def create_tfidf_training_data(docs):
    """
    Creates a document corpus list (by stripping out the
    class labels), then applies the TF-IDF transform to this
    list. 

    The function returns both the class label vector (y) and 
    the corpus token/feature matrix (X).
    """
    # Create the training data class labels
    y = [d[0] for d in docs]
    print(y)  
    
    # Create the document corpus list
    corpus = [d[1] for d in docs]

    # Create the TF-IDF vectoriser and transform the corpus
    vectorizer = TfidfVectorizer(ngram_range=(1,1))
    X = vectorizer.fit_transform(corpus)
    return X, y

def train_svm(X, y):
    """
    Create and train the Support Vector Machine.
    """
    #1000000
    svm = SVC(C =5000000, gamma='auto', kernel='rbf')
    svm.fit(X, y)
    return svm


if __name__ == "__main__":

    df = pd.read_csv("reparied_trained1.csv",error_bad_lines=False,encoding='utf-8')
    tf =pd.read_csv("TRAINEDCONTENT.csv",header = None,error_bad_lines=False,encoding='utf-8')
    '''
    # Create the list of Reuters data and create the parser
    files = ["data/reut2-%03d.sgm" % r for r in range(0, 22)]
    parser = ReutersParser()

    # Parse the document and force all generated docs into
    # a list so that it can be printed out to the console
    docs = []
    for fn in files:
        for d in parser.parse(open(fn, 'rb')):
            docs.append(d)
    '''
    docs  = []
    i = 0
    topics = []
    ref_docs =[]
    '''
    while i < len(df):
        try:

            docs.append(str(df.CONTENT[i]))
            topics.append(df.CLASS[i])
            ref_docs.append((str(df.CLASS[i]),str(df.CONTENT[i])))
            i+=1
        except:
            print(i)
            i+=1
            pass
    '''

    i = 1
    new = [] 
    while i < 600:
        try:
            if tf[1][i] == '':
                i +=1
                continue
            if tf[2][i] == 'No':
                i+=1
                continue
            ref_docs.append((str(tf[2][i]),str(tf[1][i])))
            new .append((str(tf[2][i]),str(tf[1][i])))

            i+=1
        except:
            print(i)
            i+=1
            pass
            

    X, y = create_tfidf_training_data(ref_docs)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.03, random_state=42
    )
    d = y_test.count('Y')
    e = y_test.count('N')
    svm = train_svm(X_train, y_train)

    pred = svm.predict(X_test)
    
    print(svm.score(X_test, y_test))
    a = np.flatnonzero(y_test != pred)
    b = 0
    c = 0
    
    for i in a:
       if y_test[i] == 'Y':
           b  += 1
       else:
           c +=1
    print('FAILED YES CASE ' , b, '--- WITH ',d,'CASES --- ACCURACY FOR YES: ', (d-b)/d)
    print('FAILED NO CASE ' , c, '--- WITH ',e,'CASES --- ACCURACY FOR NO: ', (e-c)/e)
    misclassified_samples = X_test[y_test != pred]
    print(confusion_matrix(pred, y_test))
'''
import cPickle
with open('my_dumped_classifier.pkl', 'wb') as fid:
    cPickle.dump(svm, fid)
with open('my_dumped_classifier.pkl', 'rb') as fid:
    load = cPickle.load(fid)
'''
from sklearn.externals import joblib
joblib.dump(svm, 'filename.pkl') 
clf = joblib.load('filename.pkl')
a = ['Students are cast as participants of the policymaking process, in most cases as a trusted member of the NSC reporting to the President or National Security Advisor, where they are required to devise strategies and write “Strategic Options Memos.” Strategic Options Memos combine careful analysis and strategic imagination, on the one hand, with the necessity to communicate to major constituencies in order to sustain public support, on the other. Students will write four memos: Responding to Stuxnet, Cybersecurity Authorities, Cybersecurity Strategy, and Preparing for an Attack.']
vectorizer = TfidfVectorizer(ngram_range=(1,1))
b = vectorizer.transform(a)
print(b)
clf.predict(b)
    
        

