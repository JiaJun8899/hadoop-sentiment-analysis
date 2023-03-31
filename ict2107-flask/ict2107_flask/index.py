import os
import sys
from ict2107_flask import app
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Definitions for BarPlotYear
jobsArrayBPY = []      # [jobs]
sentimentsArrayBPY = []# [sentiments]
sentimentArrBPY = []   # wee
positiveArrayBPY = []  # [positive]
negativeArrayBPY = []  # [negative]
neutralArrayBPY = []   # [neutral]
yearArrayBPY = []      # [year]

# Definitions for BarPlotJobs
jobsArrayBPJ = []       # jobs for barPlotJobs
sentimentsArrayBPJ = [] # sentiments for barPlotJobs
positiveArrayBPJ = []  # [positive] for barPlotJobs
negativeArrayBPJ = []  # [negative] for barPlotJobs
neutralArrayBPJ = []   # [neutral] for barPlotJobs

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
sentimentWordCloud = []
proConNeutralWordCloud = []
werdCloud = []
wordQtyWordCloud = []
sentiChangesIndex = []  #index at which negative becomes neutral becomes positive

# index at which pros become cons back to pros so an output of 
# [a,b,c,...] means pros will be from index 0 till a-1, cons will be from a to b-1, pros will be from b to c-1 etc etc
prosConsChangesIndex = [] 

def readBarPlotYear():
    with open(os.path.join(sys.path[0], 'ict2107_flask/barPlotYear'), 'r') as foo:
     
        for index, line in enumerate(foo):
            # line = line.decode("utf-8") # So that we reading it in strings not bytes
            fooArray = line.split(" ")  # Split to get the year
            if (index % 4 == 0):
                yearArrayBPY.append(fooArray[0])
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
    with open(os.path.join(sys.path[0], 'ict2107_flask/barPlotJobs'), 'r') as foo:
        for index, line in enumerate(foo):
            fooArray = line.split(":\t")
            if ((index + 1) % 3 == 0):
                stringTemp = fooArray[0].split()
                stringTemp = " ".join(stringTemp[:-1])
                jobsArrayBPJ.append(stringTemp)
                neutralArrayBPJ.append(int(fooArray[1].strip()))
            elif ((index + 1) % 3 == 1):
                positiveArrayBPJ.append(int(fooArray[1].strip()))
            elif ((index + 1) % 3 == 2):
                negativeArrayBPJ.append(int(fooArray[1].strip()))

def readSentiments():
    with open(os.path.join(sys.path[0], 'ict2107_flask/sentiment'), 'r') as foo:
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
    with open(os.path.join(sys.path[0], 'ict2107_flask/wordCloud'), 'r') as foo:
        ah = "negative"
        ahh = "pros"
        for i, line in enumerate(foo):
            fooArray = line.split('\t') # in the format of ['postive-pros','great 1']
            
            tmpSentiProCon = fooArray[0].split('-') # in the format of ['positive', 'pros']
            
            if ah != tmpSentiProCon[0]: sentiChangesIndex.append(i)
            ah = tmpSentiProCon[0]
            sentimentWordCloud.append(tmpSentiProCon[0])
            proConNeutralWordCloud.append(tmpSentiProCon[1])

            if ahh != tmpSentiProCon[1]: prosConsChangesIndex.append(i)
            ahh = tmpSentiProCon[1]
            
            tmpWrdQty = fooArray[1].split(' ')      # in the format of ['great', '1']
            
            werdCloud.append(tmpWrdQty[0])
            wordQtyWordCloud.append(int(tmpWrdQty[1]))




        

class getArrays:
    # For bar plot year
    def getFullArrayBPY():return sentimentsArrayBPY
    def getYearArrBPY():return yearArrayBPY
    def getPositiveArrBPY():return positiveArrayBPY
    def getNegativeArrBPY():return negativeArrayBPY
    def getNeutralArrBPY():return neutralArrayBPY
    
    # For bar plot jobs
    def getJobsArrayBPJ():return jobsArrayBPJ
    def getPositiveArrayBPJ(): return positiveArrayBPJ
    def getNegativeArrayBPJ(): return negativeArrayBPJ
    def getNeutralArrayBPJ(): return neutralArrayBPJ
    
    # For sentiments
    def getSentiments(): return allInOne

    # For wordcloud
    def getWordCloud_word(): return werdCloud
    def getWordCloud_allTheWordsStr(): return ' '.join(werdCloud)
    def getWordCloud_qty(): return wordQtyWordCloud
    def getWordCloud_sentiment(): return sentimentWordCloud
    def getWordCloud_proConNeutral(): return proConNeutralWordCloud
    def getWordCloud_indexSentim(): return sentiChangesIndex
    def getWordCloud_indexProsCons(): return prosConsChangesIndex


@app.route("/", methods=["GET", "POST"])
def index():
    readBarPlotYear()   # Reads barPlotYear data and puts it into the arrays
    readBarPlotJobs()   # Reads barPlotJobs data and puts it into the arrays
    readSentiments()    # Reads sentiment data and puts it into the arrays
    readWordCloud()     # Reads wordcloud data and puts it into arrays

    return (
        # f'<p>contains the following contents: {sentimentArrBPY} <br><br> YearArr: {yearArrayBPY} <br> PositiveArr: {positiveArrayBPY}<br> NegativeArr: {negativeArrayBPY} <br> NeutralArr: {neutralArrayBPY}<p>\n'
        # f'<p><br> JobsArr: {jobsArrayBPJ} <br> PositiveArr: {positiveArrayBPJ}<br> NegativeArr: {negativeArrayBPJ} <br> NeutralArr: {neutralArrayBPJ}<p>\n'        
        # f'<p> The final returned array is: {getArrays.getSentiments()}</p>\n'        
        # f'<p> The final returned array is: {getArrays.getWordCloud_allTheWordsStr()}</p>\n'        
        render_template("upload.html")
    )