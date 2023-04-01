import os
import sys
from ict2107_flask import app
from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Definitions for year_sentiment
matchesBPY = []        # [match/unmatched]
jobsArrayBPY = []      # [jobs]
sentimentsArrayBPY = []# [sentiments]
sentimentArrBPY = []   # wee
positiveArrayBPY = []  # [positive]
negativeArrayBPY = []  # [negative]
neutralArrayBPY = []   # [neutral]
yearArrayBPY = []      # [year]

# Definitions for job_sentiment
matchesBPJ = []         # match/ unmatched 
jobsArrayBPJ = []       # jobs 
sentimentsArrayBPJ = [] # sentiments 
positiveArrayBPJ = []  # [positive] 
negativeArrayBPJ = []  # [negative] 
neutralArrayBPJ = []   # [neutral] 

# definitions for sentiments
senSentiment = []       # sentiments - pos/neg/neutral
summarySentiment = []   # summary of review - first word after \t value
jobSentiment = []       # job title
ratingSentiment = []    # rating
prosSentiment = []      # pros
consSentiment = []      # cons
dateSentiment = []      # date
scoreSentiment = []     # score
counterSenti = []       # index counter
allInOne = [counterSenti, dateSentiment, senSentiment, scoreSentiment, ratingSentiment, jobSentiment, summarySentiment, prosSentiment, consSentiment]

# definitions for wordcloud
matchWordCloud = []
sentimentWordCloud = []
proConNeutralWordCloud = []
werdCloud = []
wordQtyWordCloud = []
sentiChangesIndex = []  #index at which negative becomes neutral becomes positive
matchChangesIndex = []

# index at which pros become cons back to pros so an output of 
# [a,b,c,...] means pros will be from index 0 till a-1, cons will be from a to b-1, pros will be from b to c-1 etc etc
prosConsChangesIndex = [] 

def readBarPlotYear():
    with open(os.path.join(sys.path[0], 'ict2107_flask/year_sentiment'), 'r') as foo:
     
        for index, line in enumerate(foo):
            # line = line.decode("utf-8") # So that we reading it in strings not bytes
            fooArray = line.split(" ")  # Split to get the year
            if (index % 4 == 0):
                tmpArr = fooArray[0].split("\t")
                matchesBPY.append(tmpArr[0])
                yearArrayBPY.append(tmpArr[1])
            sentimentsArrayBPY.append(fooArray[1])
        
        for sentiment in sentimentsArrayBPY:
            sentimentArr = sentiment.split("\t")
            if(sentimentArr[0] == "Negative:"):
                sentimentArr[1] = sentimentArr[1].strip()
                negativeArrayBPY.append(int(sentimentArr[1]))
            if(sentimentArr[0] == "Positive:"):
                sentimentArr[1] = sentimentArr[1].strip()
                positiveArrayBPY.append(int(sentimentArr[1]))
            if(sentimentArr[0] == "Neutral:"):
                sentimentArr[1] = sentimentArr[1].strip()
                neutralArrayBPY.append(int(sentimentArr[1])) 

def readBarPlotJobs():
    with open(os.path.join(sys.path[0], 'ict2107_flask/job_sentiment'), 'r') as foo:
        for index, line in enumerate(foo):
            fooArray = line.split("\t")     # ['matched', 'jobs:', '1']
            matchesBPJ.append(fooArray[0])
            if ((index + 1) % 3 == 0):
                neutralArrayBPJ.append(int(fooArray[2]))
                jobsArrayBPJ.append(fooArray[1].removesuffix('Neutral:'))
            elif ((index + 1) % 3 == 1):
                positiveArrayBPJ.append(int(fooArray[2]))
            elif ((index + 1) % 3 == 2):
                negativeArrayBPJ.append(int(fooArray[2]))

def readSentiments():
    with open(os.path.join(sys.path[0], 'ict2107_flask/sentiment_raw'), 'r') as foo:
        for i, line in enumerate(foo):
            fooArray = line.split(",")
            counterSenti.append(str(i + 1))
            jobSentiment.append(fooArray[1])
            ratingSentiment.append(fooArray[2])
            prosSentiment.append(fooArray[3])
            consSentiment.append(fooArray[4])
            dateSentiment.append(fooArray[5])
            scoreSentiment.append(fooArray[6].removesuffix("\n"))

            fooArray = fooArray[0].split("\t")
            senSentiment.append(fooArray[0])
            summarySentiment.append(fooArray[1])


def readWordCloud():
    with open(os.path.join(sys.path[0], 'ict2107_flask/word_counter'), 'r') as foo:
        ah = "negative"
        ahh = "pros"
        ahhh = "Matched"
        for i, line in enumerate(foo):
            fooArray = line.split('\t') # in the format of ['Matched', 'postive-pros', 'great 1']

            matchWordCloud.append(fooArray[0])
            if fooArray[0] != ahhh: 
                matchChangesIndex.append(i)
                ahhh = fooArray[0] 

            tmpSentiProCon = fooArray[1].split('-') # in the format of ['positive', 'pros']
            
            if ah != tmpSentiProCon[0]: sentiChangesIndex.append(i)
            ah = tmpSentiProCon[0]
            sentimentWordCloud.append(tmpSentiProCon[0])
            proConNeutralWordCloud.append(tmpSentiProCon[1])

            if ahh != tmpSentiProCon[1]: prosConsChangesIndex.append(i)
            ahh = tmpSentiProCon[1]
            
            tmpWrdQty = fooArray[2].split(' ')      # in the format of ['great', '1']
            
            werdCloud.append(tmpWrdQty[0])
            wordQtyWordCloud.append(int(tmpWrdQty[1]))




        

class getArrays:
    # For bar plot year
    def getMatchBPY():return matchesBPY
    def getFullArrayBPY():return sentimentsArrayBPY
    def getYearArrBPY():return yearArrayBPY
    def getPositiveArrBPY():return positiveArrayBPY
    def getNegativeArrBPY():return negativeArrayBPY
    def getNeutralArrBPY():return neutralArrayBPY
    
    # For bar plot jobs
    def getMatchBPY(): return matchesBPY
    def getJobsArrayBPJ():return jobsArrayBPJ
    def getPositiveArrayBPJ(): return positiveArrayBPJ
    def getNegativeArrayBPJ(): return negativeArrayBPJ
    def getNeutralArrayBPJ(): return neutralArrayBPJ
    
    # For sentiments
    def getSentiments(): return allInOne

    # For wordcloud
    def getWordCloud_match(): return matchWordCloud
    def getWordCloud_indexMatchChange(): return matchChangesIndex[0]
    def getWordCloud_word(): return werdCloud
    def getWordCloud_allTheWordsStr(): return ' '.join(werdCloud)
    def getWordCloud_qty(): return wordQtyWordCloud
    def getWordCloud_sentiment(): return sentimentWordCloud
    def getWordCloud_proConNeutral(): return proConNeutralWordCloud
    def getWordCloud_indexSentim(): return sentiChangesIndex
    def getWordCloud_indexProsCons(): return prosConsChangesIndex


@app.route("/", methods=["GET", "POST"])
def index():
    # read all data at the start
    readBarPlotYear()   # Reads barPlotYear data and puts it into the arrays
    readBarPlotJobs()   # Reads barPlotJobs data and puts it into the arrays
    readSentiments()    # Reads sentiment data and puts it into the arrays
    readWordCloud()     # Reads wordcloud data and puts it into arrays

    # redirect to graph main page
    return redirect("/barPlot/matchedJob", code=302)

    return (
        # f'<p><br> MatchedArr: {matchesBPY}<br> YearArr: {yearArrayBPY} <br> PositiveArr: {positiveArrayBPY}<br> NegativeArr: {negativeArrayBPY} <br> NeutralArr: {neutralArrayBPY}<p>\n'
        # f'<p> <br> matchesArr:{matchesBPJ} <br> JobsArr: {jobsArrayBPJ} <br> PositiveArr: {positiveArrayBPJ}<br> NegativeArr: {negativeArrayBPJ} <br> NeutralArr: {neutralArrayBPJ}<p>\n'        
        # f'<p> The final returned array is: {getArrays.getSentiments()}</p>\n'        
        # f'<p> The final returned array is: {getArrays.getWordCloud_indexMatchChange()}</p>\n'        
        # render_template("upload.html")
    )