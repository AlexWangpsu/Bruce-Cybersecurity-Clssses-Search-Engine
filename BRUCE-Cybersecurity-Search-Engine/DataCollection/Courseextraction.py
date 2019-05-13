from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import tldextract
import sys
import requests
import hashlib
from datetime import datetime
import pandas as pd    
from interruptingcow import timeout
import html2text
#This scripit take input from professor peronsal website url csv. 






'''
function accept raw links and checked status of the link and  return request obj 
'''
def get_soup(link):
    try:
        #page not found 
        error_code = requests.get(link).status_code
        if error_code != 200:
            return 'failed','failed'

        with timeout(6, exception=RuntimeError):

            request_object = requests.get(link)
            soup = BeautifulSoup(requests.get(link).content,"html")
            return soup,request_object
    except:

        return 'failed','failed'

'''
This version of the code is using key words matching to classify iif the webpages if a course page
'''
def classificatoin(request_object):

    #classificaiton step
    addto =[]
    checkcourse = ['midterm', 'Midterm', 'instructor','Instructor','Grade','grade','TAs ','Exams ','HW','Prerequisite','Lecture','lecture']
    check = False
    try:
        html = html2text.html2text(request_object.text)
    except:
        return ['ps zip'],[]

    if any(x in html for x in checkcourse):
        check = True

    if(check):
   # return ['www'],addto
        return  'True'
    else:
        return 'NONE'

'''
Some keywords filtering 

Notice it should changed to if any for clarity 
''' 
def checkcase(link):
    if ".pdf" in link:
        return 'failedpdf'
    if ".jpg" in link:
        return 'failedjpg'
    if "@" in link:
        return 'failed@'
    if ".mp4" in link:
        return 'failedmp4'
    if ".mov" in link:
        return 'failedmov'
    if ".avi" in link:
        return 'failedavi'
    if ".zip" in link:
        return 'failedzip'
    if ".png" in link:
        return 'failedpng'
    if "pptx" in link:
        return 'failedpptx'
    if ".txt" in link:
        return 'failedtxt'
    if ".mp3" in link:
        return 'failedmp3'
    if "facebook" in link:
        return 'failedfacebook'
    if "linkedin" in link:
        return 'failedlinkedin'
    if "twitter" in  link:
        return 'failedtwitter'
    if "youtube"in  link:
        return 'failedyoutube'
    if "instgram"in  link:
        return 'failedinstgram'
    if ".html#"in  link:
        return 'failedhtml'
    if "email"in  link:
        return 'failedeamil'
    return 'nnn'


'''
Parsing the hyperlnks
Runnning as DFS to find the webpage 
'''

def find_internal_urls(link, depth):

    ext= tldextract.extract(link)
    base_url = ('http://'.join(ext[:2]))+ '.' +ext[2]

    if 'http' not in link:
        return ['failed from failed'],[]
    #print(link,'here')

    all_urls_info = []
    All_links = []

    soup,request_object = get_soup(link)
    if soup == 'failed':
        return ['failed from soup'],[]
    if depth > 0:
        result = classificatoin(request_object)
        if result == 'NONE':
            if depth == 3:
                return ['failed'],[]
        else:
            #print(link,'here to be added now ................')
            return ['failed'], [str(link)]
    a_tags = soup.findAll("a", href=True)

    for a_tag in a_tags:
        try:

            spamde = checkcase(a_tag["href"])
            if 'fail' in spamde:
                continue
            

            if depth == 0:
  
                test1 = ['teach','Teach','course','Course','Fall','Spring']
                test2 = ['Fall','Spring']
                if not any(x in a_tag["href"] for x in test1 ):
                    if not any(y in str(a_tag) for y in test2 ):
                        continue


            if (("https" not in a_tag["href"]) and("http" not in a_tag["href"] )):
                #url = urljoin(base_url, a_tag["href"])
                url = base_url+ a_tag["href"]

                soup,request_object = get_soup(url)
                if soup == 'failed':
                    url = link + a_tag["href"]
                

            if "http" in a_tag["href"]:
                url = a_tag['href']

            All_links.append(url)
    

        except:
            continue

    return All_links,[]

'''
Read CSV from professor personal websites
Runninig DFS to extract course pages
'''

if __name__ == "__main__":
    pwebsites  = pd.read_csv('codaspyppl.csv',header = None)
    depth = 0
    allcourses = []
    k =0
    for pwebsite in pwebsites[0]:
        try:

            print(k,'iter')
            k +=1
            allcourseshistory = []
            links_fromcurrentpages =[]
            alllinkscollected = []
            detectedcourse = []
            links_fromcurrentpages,detectedcourse = find_internal_urls(pwebsite, depth)
            depth +=1
            allcourseshistory += links_fromcurrentpages
            alllinkscollected += links_fromcurrentpages
            temp_holdpages =[]
            allcourses+= detectedcourse
            while depth < 3: 
                for status_dict in alllinkscollected:
                   #print(depth)

                   #print(status_dict)
                   links_fromcurrentpages,detectedcourse =  find_internal_urls(status_dict,depth)
                   allcourses += detectedcourse
                   for i in links_fromcurrentpages:
                        if i not in allcourseshistory:
                            allcourseshistory.append(i)
                            temp_holdpages.append(i)

                alllinkscollected = []
                alllinkscollected += temp_holdpages
                temp_holdpages = []
                depth += 1
                print(depth)
      
            depth = 0
        except:
            print('errror')
            continue



    df = pd.DataFrame(allcourses, columns=["URL"])

    #This line save the result to csv
    df.to_csv('30moree.csv', index=False)


