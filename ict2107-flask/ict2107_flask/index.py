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
                negativeArrayBPY.append(sentimentArr[1])
            if(sentimentArr[0] == "Positive:"):
                sentimentArr[1] = sentimentArr[1].strip()
                positiveArrayBPY.append(sentimentArr[1])
            if(sentimentArr[0] == "Neutral:"):
                sentimentArr[1] = sentimentArr[1].strip()
                neutralArrayBPY.append(sentimentArr[1]) 

def readBarPlotJobs():
    with open(os.path.join(sys.path[0], 'ict2107_flask/barPlotJobs'), 'r') as foo:

        for index, line in enumerate(foo):
            fooArray = line.split(":\t")
            
            if ((index + 1) % 3 == 0):
                stringTemp = fooArray[0].split()
                stringTemp = " ".join(stringTemp[:-1])
                jobsArrayBPJ.append(stringTemp)
                neutralArrayBPJ.append(fooArray[1].strip())
            elif ((index + 1) % 3 == 1):
                positiveArrayBPJ.append(fooArray[1].strip())
            elif ((index + 1) % 3 == 2):
                negativeArrayBPJ.append(fooArray[1].strip())



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
    



@app.route("/", methods=["GET", "POST"])
def index():
    readBarPlotYear()   # Reads barPlotYear data and puts it into the arrays
    readBarPlotJobs()   # Reads barPlotJobs data and puts it into the arrays

    return (
        # f'<p>contains the following contents: {sentimentArrBPY} <br><br> YearArr: {yearArrayBPY} <br> PositiveArr: {positiveArrayBPY}<br> NegativeArr: {negativeArrayBPY} <br> NeutralArr: {neutralArrayBPY}<p>\n'
        f'<p><br> JobsArr: {jobsArrayBPJ} <br> PositiveArr: {positiveArrayBPJ}<br> NegativeArr: {negativeArrayBPJ} <br> NeutralArr: {neutralArrayBPJ}<p>\n'        
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

# summary
# job title
# rating
# pros
# cons
# date
# score