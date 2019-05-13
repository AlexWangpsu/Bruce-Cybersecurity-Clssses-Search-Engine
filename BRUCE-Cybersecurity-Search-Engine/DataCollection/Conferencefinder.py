# This script uses the Google-Search-API found at
# https://github.com/abenassi/Google-Search-API
from google import google
import csv
import re
import time
import random

#Opens the csv. Change the csv name each time you want to
#write into a new file for a different conference.

csvv = open('csfwebsites2019.csv','w')

#Opens the csv of names that have been manually gathered
#from the conference page. Can be done for any list of names, however.

with open('csfnames2019.csv', 'r') as csvfile:
    num_page = 1
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    # For each row in the csv you're reading from, make sure the format
    # is clean and then send it into the google.search() function.
    # search_results[0].link takes the link of only the first result,
    # which is most commonly the prof's personal website.
        
    for row in spamreader:
        row = " ".join(row)
        row = row.replace('"','')
        print(row)
        ele = str(row) 
        if ele == "":
            pass
        else:
            search_results = google.search(ele,num_page)
            print(search_results)
            try:
                i = str(search_results[0].link)
                print(i)
                csvv.write(i)
                csvv.write('\n')
            except:
                print (ele + 'FAILED')

            # This section is crucial, as if you do not put a sleep
            # between runs of your loop Google will detect you
            # and block your script from running.
            
            timenow = random.randrange(20,80)
            print(timenow)
            time.sleep(timenow)
            
        
csvv.close()

