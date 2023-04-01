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
sentimentsArrayBPJ = [] # sentiments 
matchedJobsArrayBPJ = []       # jobs 
matchedPositiveArrayBPJ = []  # [positive] 
matchedNegativeArrayBPJ = []  # [negative] 
matchedNeutralArrayBPJ = []   # [neutral] 
unmatchedJobsArrayBPJ = []       # jobs 
unmatchedPositiveArrayBPJ = []  # [positive] 
unmatchedNegativeArrayBPJ = []  # [negative] 
unmatchedNeutralArrayBPJ = []   # [neutral] 

# definitions for sentiments
matchedSentiment = []       # matched sentiments - pos/neg/neutral
unmatchedSentiment = []       # unmatched sentiments - pos/neg/neutral
summarySentiment = []   # summary of review - first word after \t value
jobSentiment = []       # job title
ratingSentiment = []    # rating
prosSentiment = []      # pros
consSentiment = []      # cons
dateSentiment = []      # date
matchedScoreSentiment = []     # matched score
unmatchedScoreSentiment = []     # unmatched score
counterSenti = []       # index counter
# allInOne = [counterSenti, dateSentiment, matchedSentiment, unmatchedSentiment, matchedScoreSentiment, unmatchedScoreSentiment, ratingSentiment, jobSentiment, summarySentiment, prosSentiment, consSentiment]
allNegativeSentiments = [[],[],[],[],[],[],[],[],[],[],[]]
allPositiveSentiments = [[],[],[],[],[],[],[],[],[],[],[]]
allNeutralSentiments = [[],[],[],[],[],[],[],[],[],[],[]]

# definitions for wordcloud
sentimentWordCloud = []
proConNeutralWordCloud = []
werdCloud = []
matchedWordCloud = []
unmatchedWordCloud = []
wordQtyWordCloud = []
sentiChangesIndex = []  #index at which negative becomes neutral becomes positive
matchChangesIndex = []
matchedProWords = []
matchedConWords = []
unmatchedProWords = []
unmatchedConWords = []
matchedProDict = {}
matchedConDict = {}
unmatchedProDict = {}
unmatchedConDict = {}

# accuracy arrays
accuracyTitle = []
accuracyCategory = []
accuracyValue = []
accuracyArray = [accuracyTitle, accuracyCategory, accuracyValue]

# read accuracy file
def readAccuracy():
    with open(os.path.join(sys.path[0], 'ict2107_flask/accuracy'), 'r') as foo:
        for i, line in enumerate(foo):
            lineArray = line.split("\t")
            accuracyTitle.append(lineArray[0])
            backStr = lineArray[1].removesuffix("\n")
            backStrArray = backStr.split(": ")
            accuracyCategory.append(backStrArray[0])
            accuracyValue.append(backStrArray[1])


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
            if (fooArray[0] == "Matched"):
                # matchesBPJ.append(fooArray[0])
                if ((index + 1) % 3 == 0):
                    matchedNeutralArrayBPJ.append(int(fooArray[2]))    #neutralArrayBPJ.append(int(fooArray[2]))
                    matchedJobsArrayBPJ.append(fooArray[1].removesuffix('Neutral:'))    #jobsArrayBPJ.append(fooArray[1].removesuffix('Neutral:'))
                elif ((index + 1) % 3 == 1):
                    matchedPositiveArrayBPJ.append(int(fooArray[2]))    #positiveArrayBPJ.append(int(fooArray[2]))
                elif ((index + 1) % 3 == 2):
                    matchedNegativeArrayBPJ.append(int(fooArray[2]))    #negativeArrayBPJ.append(int(fooArray[2]))
            elif (fooArray[0] == "UnMatched"):
                # matchesBPJ.append(fooArray[0])
                if ((index + 1) % 3 == 0):
                    unmatchedNeutralArrayBPJ.append(int(fooArray[2]))
                    unmatchedJobsArrayBPJ.append(fooArray[1].removesuffix('Neutral:'))
                elif ((index + 1) % 3 == 1):
                    unmatchedPositiveArrayBPJ.append(int(fooArray[2]))
                elif ((index + 1) % 3 == 2):
                    unmatchedNegativeArrayBPJ.append(int(fooArray[2]))


def readSentiments():
    with open(os.path.join(sys.path[0], 'ict2107_flask/sentiment_raw'), 'r') as foo:
        for i, line in enumerate(foo):
            fooArray = line.split("\t")
            if (fooArray[0] == "negative"):
                # [counterSenti, dateSentiment, matchedSentiment, unmatchedSentiment, matchedScoreSentiment, unmatchedScoreSentiment, ratingSentiment, jobSentiment, summarySentiment, prosSentiment, consSentiment]

                allNegativeSentiments[2].append(fooArray[0])
                allNegativeSentiments[3].append(fooArray[1])
                # matchedSentiment.append(fooArray[0])
                # unmatchedSentiment.append(fooArray[1])

                # split the last part
                sentenceArray = fooArray[2].split(",")

                # allNegativeSentiments[0].append(str(i + 1))
                allNegativeSentiments[0].append(len(allNegativeSentiments[2]))
                allNegativeSentiments[8].append(sentenceArray[0])
                allNegativeSentiments[7].append(sentenceArray[1])
                allNegativeSentiments[6].append(sentenceArray[2])
                allNegativeSentiments[9].append(sentenceArray[3])
                allNegativeSentiments[10].append(sentenceArray[4])
                allNegativeSentiments[1].append(sentenceArray[5])
                allNegativeSentiments[4].append(sentenceArray[6])
                allNegativeSentiments[5].append(sentenceArray[7].removesuffix("\n"))

                # counterSenti.append(str(i + 1))
                # summarySentiment.append(sentenceArray[0])
                # jobSentiment.append(sentenceArray[1])
                # ratingSentiment.append(sentenceArray[2])
                # prosSentiment.append(sentenceArray[3])
                # consSentiment.append(sentenceArray[4])
                # dateSentiment.append(sentenceArray[5])
                # matchedScoreSentiment.append(sentenceArray[6])
                # unmatchedScoreSentiment.append(sentenceArray[7].removesuffix("\n"))
                
            elif (fooArray[0] == "positive"):
                allPositiveSentiments[2].append(fooArray[0])
                allPositiveSentiments[3].append(fooArray[1])

                # split the last part
                sentenceArray = fooArray[2].split(",")

                allPositiveSentiments[0].append(len(allPositiveSentiments[2]))
                allPositiveSentiments[8].append(sentenceArray[0])
                allPositiveSentiments[7].append(sentenceArray[1])
                allPositiveSentiments[6].append(sentenceArray[2])
                allPositiveSentiments[9].append(sentenceArray[3])
                allPositiveSentiments[10].append(sentenceArray[4])
                allPositiveSentiments[1].append(sentenceArray[5])
                allPositiveSentiments[4].append(sentenceArray[6])
                allPositiveSentiments[5].append(sentenceArray[7].removesuffix("\n"))

            elif (fooArray[0] == "neutral"):
                allNeutralSentiments[2].append(fooArray[0])
                allNeutralSentiments[3].append(fooArray[1])

                # split the last part
                sentenceArray = fooArray[2].split(",")

                allNeutralSentiments[0].append(len(allNeutralSentiments[2]))
                allNeutralSentiments[8].append(sentenceArray[0])
                allNeutralSentiments[7].append(sentenceArray[1])
                allNeutralSentiments[6].append(sentenceArray[2])
                allNeutralSentiments[9].append(sentenceArray[3])
                allNeutralSentiments[10].append(sentenceArray[4])
                allNeutralSentiments[1].append(sentenceArray[5])
                allNeutralSentiments[4].append(sentenceArray[6])
                allNeutralSentiments[5].append(sentenceArray[7].removesuffix("\n"))


def readWordCloud():
    with open(os.path.join(sys.path[0], 'ict2107_flask/word_counter'), 'r') as foo:
        ah = "negative"
        ahh = "pros"
        ahhh = "Matched"
        for i, line in enumerate(foo):
            fooArray = line.split('\t') # in the format of ['Matched', 'postive-pros', 'great 1']

            # if (fooArray[0] == "Matched"):
            #     # split word and number
            #     wordSplit = fooArray[2].split(" ")
            #     if (fooArray[1][-4:] == "pros"):
            #         for x in range(int(wordSplit[1].removesuffix("\n"))):
            #             matchedProWords.append(wordSplit[0])    # add word the number of times it appeared
            #     elif (fooArray[1][-4:] == "cons"):
            #         for x in range(int(wordSplit[1].removesuffix("\n"))):
            #             matchedConWords.append(wordSplit[0])    # add word the number of times it appeared
            # elif (fooArray[0] == "UnMatched"):
            #     # split word and number
            #     wordSplit = fooArray[2].split(" ")
            #     if (fooArray[1][-4:] == "pros"):
            #         for x in range(int(wordSplit[1].removesuffix("\n"))):
            #             unmatchedProWords.append(wordSplit[0])    # add word the number of times it appeared
            #     elif (fooArray[1][-4:] == "cons"):
            #         for x in range(int(wordSplit[1].removesuffix("\n"))):
            #             unmatchedConWords.append(wordSplit[0])    # add word the number of times it appeared

            if (fooArray[0] == "Matched"):
                # split word and number
                wordSplit = fooArray[2].split(" ")
                if (fooArray[1][-4:] == "pros"):
                    if (wordSplit[0] in matchedProDict):
                        matchedProDict[wordSplit[0]] += int(wordSplit[1].removesuffix("\n"))
                    else:
                        matchedProDict[wordSplit[0]] = int(wordSplit[1].removesuffix("\n"))    # add word the number of times it appeared
                elif (fooArray[1][-4:] == "cons"):
                    if (wordSplit[0] in matchedConDict):
                        matchedConDict[wordSplit[0]] += int(wordSplit[1].removesuffix("\n"))
                    else:
                        matchedConDict[wordSplit[0]] = int(wordSplit[1].removesuffix("\n"))    # add word the number of times it appeared
            elif (fooArray[0] == "UnMatched"):
                # split word and number
                wordSplit = fooArray[2].split(" ")
                if (fooArray[1][-4:] == "pros"):
                    if (wordSplit[0] in unmatchedProDict):
                        unmatchedProDict[wordSplit[0]] += int(wordSplit[1].removesuffix("\n"))
                    else:
                        unmatchedProDict[wordSplit[0]] = int(wordSplit[1].removesuffix("\n"))    # add word the number of times it appeared
                elif (fooArray[1][-4:] == "cons"):
                    if (wordSplit[0] in unmatchedConDict):
                        unmatchedConDict[wordSplit[0]] += int(wordSplit[1].removesuffix("\n"))
                    else:
                        unmatchedConDict[wordSplit[0]] = int(wordSplit[1].removesuffix("\n"))    # add word the number of times it appeared
        

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
    def getMatchedJobsArrayBPJ():return matchedJobsArrayBPJ
    def getMatchedPositiveArrayBPJ(): return matchedPositiveArrayBPJ
    def getMatchedNegativeArrayBPJ(): return matchedNegativeArrayBPJ
    def getMatchedNeutralArrayBPJ(): return matchedNeutralArrayBPJ
    def getUnmatchedJobsArrayBPJ():return unmatchedJobsArrayBPJ
    def getUnmatchedPositiveArrayBPJ(): return unmatchedPositiveArrayBPJ
    def getUnmatchedNegativeArrayBPJ(): return unmatchedNegativeArrayBPJ
    def getUnmatchedNeutralArrayBPJ(): return unmatchedNeutralArrayBPJ
    
    # For sentiments
    # def getSentiments(): return allInOne
    def getNegativeSentiments(): return allNegativeSentiments
    def getPositiveSentiments(): return allPositiveSentiments
    def getNeutralSentiments(): return allNeutralSentiments

    # For wordcloud
    # def getWordCloud_match(): return matchWordCloud
    # def getWordCloud_indexMatchChange(): return matchChangesIndex[0]
    # def getWordCloud_word(): return werdCloud
    # def getWordCloud_allTheWordsStr(): return ' '.join(werdCloud)

    def getWordCloud_matchedStr(): return ' '.join(matchedWordCloud)
    def getWordCloud_unmatchedStr(): return ' '.join(unmatchedWordCloud)

    # def getWordCloud_matchedProStr(): return ' '.join(matchedProWords)
    # def getWordCloud_matchedConStr(): return ' '.join(matchedConWords)
    # def getWordCloud_unmatchedProStr(): return ' '.join(unmatchedProWords)
    # def getWordCloud_unmatchedConStr(): return ' '.join(unmatchedConWords)

    def getWordCloud_matchedProDict(): return matchedProDict
    def getWordCloud_matchedConDict(): return matchedConDict
    def getWordCloud_unmatchedProDict(): return unmatchedProDict
    def getWordCloud_unmatchedConDict(): return unmatchedConDict

    # def getWordCloud_qty(): return wordQtyWordCloud
    # def getWordCloud_sentiment(): return sentimentWordCloud
    # def getWordCloud_proConNeutral(): return proConNeutralWordCloud
    # def getWordCloud_indexSentim(): return sentiChangesIndex
    # def getWordCloud_indexProsCons(): return prosConsChangesIndex

    def getAccuracy(): return accuracyArray


@app.route("/", methods=["GET", "POST"])
def index():
    # read all data at the start
    readBarPlotYear()   # Reads barPlotYear data and puts it into the arrays
    readBarPlotJobs()   # Reads barPlotJobs data and puts it into the arrays
    readSentiments()    # Reads sentiment data and puts it into the arrays
    readWordCloud()     # Reads wordcloud data and puts it into arrays
    readAccuracy()

    # redirect to graph main page
    return redirect("/barPlot/matchedJob", code=302)

    return (
        # f'<p><br> MatchedArr: {matchesBPY}<br> YearArr: {yearArrayBPY} <br> PositiveArr: {positiveArrayBPY}<br> NegativeArr: {negativeArrayBPY} <br> NeutralArr: {neutralArrayBPY}<p>\n'
        # f'<p> <br> matchesArr:{matchesBPJ} <br> JobsArr: {jobsArrayBPJ} <br> PositiveArr: {positiveArrayBPJ}<br> NegativeArr: {negativeArrayBPJ} <br> NeutralArr: {neutralArrayBPJ}<p>\n'        
        # f'<p> The final returned array is: {getArrays.getSentiments()}</p>\n'        
        # f'<p> The final returned array is: {getArrays.getWordCloud_unmatchedStr()}</p>\n'        
        # render_template("upload.html")
    )