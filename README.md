# BRUCE Cybersecurity Database Search Engine

The BRUCE Engine is a database search function that allows a user to search for a large number of cybersecurity courses through the domain bruce.ist.psu.edu. A search can return many courses in the area of cybersecurity. Each search result contains information such as professor, university, and textbook. It also includes a link to the course syllabus website and a screenshot preview of what the website looks like.


### Data Gathering
The main method to gather course data at the moment is to use cybersecurity conference program commitee lists to get a list of professors. After that, we use a google search script to get their personal website, and then crawl each of the professor's personal websites to find likely course syllabi. In order to avoid duplicates, each new list of professors from a conference is compared against the total list of professor that have already been found.

*I have uploaded of all the courses we collected into Course_Collected (All the actual courses page)
*ConferenceFiles have all the professor personal websites that we scraped from 


### Page Classification 
* [Naive Bayes] Feed directly with text corpus, achieved >90% test accuracy (from google search corpus).
   Script:naivebayes.py
* [SVM] Feed directly with text corpus achieved >95% test accuracy (from google search corpus).
   Script: test_svm.py
* [LSTM] Feed directly with text corpus, title, numbers of hyperlinks, numbers of pictures achieved >97% test  accuracy(from google search corpus). (reference:https://www.linkedin.com/pulse/identifying-clickbaits-using-machine-learning-abhishek-thakur/) 

Currently using Keywords matching from Script: -Courseextraction.py seems to work best given the professor personal website 

Note all file in -DataCollection-

Note: the distributioin of the dataset varies depending of the web scraping methods, therefore the testing accuracy might change. 

### Feature Extrctioin 

*Metadata extraction including: Professor names& phone number& email address, school name, course title, year of course. File: FeatureClassification.py
*Screenshot website into thumbnail using file Screenshot.py
*Concatnate all csv in the folder using file Concatenate.py

Note all file in -DataCollection-





### Accessing the HTML/CSS Files
When you login to bruce.ist.psu.edu, you'll be logged into /home/xxx1234. Go to the directory bruce by using these commands.
```
cd ..
cd ..
cd data/websites/bruce
```
### Working with MongoDB
For the purposes of this project, MongoDB is quite simple to use. Once you've uploaded the CSV to the bruce server, only a few steps before the database can be built. Perhaps the easiest way to combine the existing csv with the new data is to use cat.

```
cat collection1.csv  collection2.csv > newcollection.csv
```

After you've combined the csv, MongoDB has an easy way to import the csv into a collection.
```
mongoimport --db users --collection contacts --type csv --headerline --file /opt/backups/contacts.csv
```

After you've successfully imported the csv, MongoDB should print out the # of documents you've loaded into the collection.
You can access the collection and look at its contents by following these commands.
```
mongo
show collections
use users (or whatever database the collection is stored in)
db.collection.find() (where collection is the name of the collection)
```

It's important to INDEX the collection now so that the test.php file can properly search in the collection.
An example of an index command. You should read more about it at https://docs.mongodb.com/manual/indexes/
```
db.coursecollection.createIndex(
   {
     DOMAIN: "text",
     TITLE: "text",
   }
 )
```
For a small change in the code or if only changing databases in MongoDB, it's probably most efficient to skip the test server step, and use the main server to see if the change went through. However, if making a big change to the .php or .html files, it's best to make a change in the test server first and then move the file over later.
## Built With

* [Python== 3.5]  - Language
* [PHP == 7.0.33](https://www.php.net/) - Language to call the MongoDB data to the website 
* HTML5
* CSS3
* [MongoDB == 3.6.12](https://www.mongodb.com/) - Database used
### Important Modules to pip install in the CentOS environment
* [BeautifulSoup == 4.4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - The Web Scraping 
* [requests == 2.21](https://docs.python.org/3/library/urllib.html) - The Web Scraping 
* [urllib == 3.7.3](https://docs.python.org/3/library/urllib.html) - The Web Scraping 
* [tldextract](https://github.com/john-kurkowski/tldextract) - The Web Scraping  -Domain Extractor 
* [GoogleSearchAPI](https://github.com/abenassi/Google-Search-API) - Used for googlesearch.py and conferencefinder.py
* [textblob](https://textblob.readthedocs.io/en/dev/) - Page Classificatoin- Naive Bayes Algorithm 
* [Scikit-learn == 0.20.3](https://scikit-learn.org/stable/modules/svm.html) - Page Classificatoin- SVM 

* [nltk == 3.4](https://www.nltk.org/) -Feature Extraction - Named Entity extraction 
* [html2text == 2018.1.9](https://pypi.org/project/html2text/) - Feature Extraciton 


## Authors

* **Weiqin Wang** - *Initial work* - *Summer 2018 - Spring 2019* 
* **Andrew Yang** - *Initial work* - *Summer 2018 - Spring 2019* 

## Acknowledgments

Thanks to Dongwon Lee for overseeing this project.

