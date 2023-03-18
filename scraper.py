from datetime import datetime
import math
import csv
import os
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

#paste/replace the url to the first page of the company's Glassdoor review in between the ""
base_url="https://www.glassdoor.sg/Reviews/Accenture-Reviews-E4138"
hdr = {'User-Agent': 'Mozilla/5.0'}

def review_scraper(url):
    #scraping the web page content
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    Date_n_JobTitle=[]
    file_name = os.path.join(os.getcwd(), 'accenture_review.csv')
    if not os.path.exists(file_name):
        print("Not here")
    Summary=[]
    Date=[]
    JobTitle=[]
    OverallRating=[]
    Pros=[]
    Cons=[]
    #get the Summary
    for x in soup.find_all('h2', {'class':'mb-xxsm mt-0 css-93svrw el6ke055'}):
        Summary.append(x.text)

    #get the Posted Date and Job Title
    for x in soup.find_all('span', {'class':'middle common__EiReviewDetailsStyle__newGrey'}):
        Date_n_JobTitle.append(x.text)

    #get the Posted Date
    for x in Date_n_JobTitle:
        Date.append(x.split(' - ')[0])

    #get Job Title
    for x in Date_n_JobTitle:
        JobTitle.append(x.split(' - ')[1])

    #get Overall Rating
    for x in soup.find_all('span', {'class':'ratingNumber mr-xsm'}):
        OverallRating.append(float(x.text))

    #get Pros
    for x in soup.find_all('span', {'data-test':'pros'}):
        Pros.append(x.text.replace('\n', '').replace('\r', '').strip())

    #get Cons
    for x in soup.find_all('span', {'data-test':'cons'}):
        Cons.append(x.text.replace('\n', '').replace('\r', '').strip())
    # function to write to csv straight
    with open(file_name, 'a', newline="", encoding='utf-8') as result_file:
        csvWriter = csv.writer(result_file)
        for i in range(len(Summary)):
            csvWriter.writerow([Summary[i], JobTitle[i], OverallRating[i], Pros[i], Cons[i], Date[i]])
    errLog("Done: " + url)
    return

def totalPages():
    #paste/replace the url to the first page of the company's Glassdoor review in between the ""
    input_url="https://www.glassdoor.sg/Reviews/Accenture-Reviews-E4138_P2.htm"
    #scraping the first page content
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(input_url+str(1)+".htm?filter.iso3Language=eng",headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, "html.parser")
    #check the total number of reviews
    countReviews = soup.find('div', {'data-test':'pagination-footer-text'}).text
    countReviews = float(countReviews.split(' Reviews')[0].split('of ')[1].replace(',',''))

    #calculate the max number of pages (assuming 10 reviews a page)
    countPages = math.ceil(countReviews/10)
    return countPages

def errLog(msg):
    with open("logs.txt",'a') as logger:
        logger.write(msg + "\n")

def find_urls_in_log():
    urls = []
    with open("logs.txt", "r") as f:
        for line in f:
            if "Error in https://" in line and "IncompleteRead(0 bytes read)" in line:
                url = line[line.index("https://"):line.index("eng")+3]
                urls.append(url)
    return urls

maxPage = totalPages() + 1
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
errLog("Started:" + dt_string)
for x in range(10747, maxPage):
    url = base_url+"_P"+str(x)+".htm?filter.iso3Language=eng"
    try:
        review_scraper(url)
    except Exception as e:
        errLog(f"Error in {url}: {e}")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
errLog("Done: " + dt_string)

errLog("Error retry Started:" + dt_string)
for errUrl in find_urls_in_log():
    try:
        review_scraper(errUrl)
    except Exception as e:
        errLog(f"Error in {errUrl}: {e}")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
errLog("Error Retry Done: " + dt_string)

# read the CSV file into a DataFrame
df = pd.read_csv("accenture_review.csv")

# drop the duplicated rows from the original DataFrame
df.drop_duplicates(keep=False, inplace=True)

# export the cleaned DataFrame to a new CSV file
df.to_csv("cleaned_reviews.csv", index=False)

print("done")