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
    return 0
#     with open(os.path.join(sys.path[0], 'ict2107_flask/sentiment'), 'r') as foo:
#         for line in foo:
#             fooArray = line.split('\t')
#             tmpSentiProCon = fooArray[0].split('-')
#             sentimentWordCloud.append(tmpSentiProCon[0])
#             proConNeutralWordCloud.append(tmpSentiProCon[1])
#             tmpWrdQty = fooArray[1].split(' ')
#             werdCloud.append(tmpWrdQty[0])
#             wordQtyWordCloud.append(int(tmpWrdQty[1]))




        

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
    def getWordCloud_qty(): return wordQtyWordCloud
    def getWordCloud_sentiment(): return sentimentWordCloud
    def getWordCloud_proConNeutral(): return proConNeutralWordCloud


@app.route("/", methods=["GET", "POST"])
def index():
    readBarPlotYear()   # Reads barPlotYear data and puts it into the arrays
    readBarPlotJobs()   # Reads barPlotJobs data and puts it into the arrays
    readSentiments()    # Reads sentiment data and puts it into the arrays
    readWordCloud()     # Reads wordcloud data and puts it into arrays

    return (
        # f'<p>contains the following contents: {sentimentArrBPY} <br><br> YearArr: {yearArrayBPY} <br> PositiveArr: {positiveArrayBPY}<br> NegativeArr: {negativeArrayBPY} <br> NeutralArr: {neutralArrayBPY}<p>\n'
        f'<p><br> JobsArr: {jobsArrayBPJ} <br> PositiveArr: {positiveArrayBPJ}<br> NegativeArr: {negativeArrayBPJ} <br> NeutralArr: {neutralArrayBPJ}<p>\n'        
        # f'<p> The final returned array is: {getArrays.getSentiments()}</p>\n'        
        # f'<p> The final returned array is: {getArrays.getSentiments()}</p>\n'        
    )



    # Once user clicks on submit and request has been sent to the flask server
    # if request.method == 'POST':
    #     foo = request.files['file']
    #     fooArray = []
    #     # print(fooArray.split(","))

    #     # Put each line in the csv into an array
        # for index, line in enumerate(foo):
        #     line = line.decode("utf-8") # So that we reading it in strings not bytes
        #     fooArray = line.split(" ")  # Split to get the year
        #     if (index % 4 == 0):
        #         yearArray.append(fooArray[0])
        #     sentimentsArray.append(fooArray[1])
            
        #     # print(sentimentsArray)
        
        # for sentiment in sentimentsArray:
        #     sentimentArr = sentiment.split("\t")
        #     if(sentimentArr[0] == "Negative:"):
        #         sentimentArr[1] = sentimentArr[1].strip()
        #         negativeArray.append(sentimentArr[1])
        #     if(sentimentArr[0] == "Positive:"):
        #         sentimentArr[1] = sentimentArr[1].strip()
        #         positiveArray.append(sentimentArr[1])
        #     if(sentimentArr[0] == "Neutral:"):
        #         sentimentArr[1] = sentimentArr[1].strip()
        #         neutralArray.append(sentimentArr[1]) 
    

        # return f'<p>{foo.filename} contains the following contents: {sentimentsArray} <br><br> YearArr: {yearArray} <br> PositiveArr: {positiveArray}<br> NegativeArr: {negativeArray} <br> NeutralArr: {neutralArray}<p>'
    
    # Return this as the default page when first load
    # return render_template("upload.html") + "<a href=/barPlot>go to the barplot page</a>"



# [[negative, neative, negative, ...], [ux, good company work, ...], []]
