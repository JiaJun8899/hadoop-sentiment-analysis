<p align="center">
    <br />
    <h1 align="center">HADOOP Sentiment Analysis Model</h1>
</p>

<p align="center">
    <i>There is no need for NLP libraries, I make my own model</i><br />
    <img src="https://img.shields.io/badge/hadoop-2.6-brightgreen" />
    <img src="https://img.shields.io/badge/java-1.7-green" />
    <img src="https://img.shields.io/badge/Coded%20By%20Humans-100%25-brightgreen" />
    <br /><br />
</p>
<hr>

Powered by Hadoop version 2.6 and Java version 1.7  
<br>
<font size="3">🎞️ [Video Demo](https://youtu.be/MKORdvMF_28)</font>

## Installation

### Crawler

1. Make and run a python environment using `py -m venv venv`
2. Run `pip install -r requirements.txt`
3. Change GlassDoor link on line 10 to the desired company
4. Run scraper.py
5. logs.txt can be view for the current progress

### 2 Hadoop JAR

1. Upload all the required files on to the HDFS server
2. Change all the file paths SentimentDriver to where you desire it to be at
3. Export the JAR file and run it on the HDFS server

#### 2.1 Alternative
1. If you have root access, you can directly run it from the DASIL Server
```bash
cd /user/ict2101351/project
hadoop jar group3.jar
```
2. The outputs will be in hdfs `/user/ict2101351/output/`
3. Jobs will be in `/user/ict2101351/output/jobs`
4. Year will be in `/user/ict2101351/output/year`
5. Word Counter will be in count `/user/ict2101351/output/counter`
6. Accuracy will be in accuracy `/user/ict2101351/output/accuracy`

### 3 Running the dashboard
1. Firstly enter the ict2107-flask folder
2. Run the command  
```bash
flask --app ict2107_flask --debug run
```
3. The dashboard should be at <a>localhost:5000</a>

## Model Results

True sentiment is based on the user's rating  
Accuracy is comparision of model's sentiment with true sentiment

### Forced Matching
<img src = "./matchedconfustionmatrix.png">

### Unmatch
<img src = "./matchedconfustionmatrix.png">

## <b>Contributors</b>

This project would not exist without these folks!

🧑 **BENNY LIM YI JIE - 2101955**  
🧑 **CHEN JIAJUN - 2101351**  
🧑 **KYE JORDAN O'REILLY - 2102841**  
🧑 **LAI WEN JUN - 2102989**  
👩 **LEE YAN RONG - 2102608**  
👩 **SOPHIE WONG SHU PING - 2102284**  
