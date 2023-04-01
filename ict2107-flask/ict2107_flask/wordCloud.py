from ict2107_flask import app
from flask import Flask, render_template, request
from matplotlib.figure import Figure
from plotly.subplots import make_subplots

from ict2107_flask.index import *

import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import random
import json
from wordcloud import WordCloud

import pandas as pd
import matplotlib.pyplot as plt

import base64
from io import BytesIO

@app.route('/wordCloud/<path:type>')
def wordCloud(type):
    if (type == "matchedPros"):
        # get word cloud data
        cloud = plotlyWordCloud(getArrays.getWordCloud_matchedStr())
        return render_template("wordCloud.html", plot=cloud, title="Matched Pros Word Cloud")
    elif (type == "matchedCons"):
        # get word cloud data
        cloud = plotlyWordCloud(getArrays.getWordCloud_matchedStr())
        return render_template("wordCloud.html", plot=cloud, title="Matched Cons Word Cloud")
    elif (type == "unmatchedPros"):
        # get word cloud data
        cloud = plotlyWordCloud(getArrays.getWordCloud_unmatchedStr())
        return render_template("wordCloud.html", plot=cloud, title="Unmatched Pros Word Cloud")
    elif (type == "unmatchedCons"):
        # get word cloud data
        cloud = plotlyWordCloud(getArrays.getWordCloud_unmatchedStr())
        return render_template("wordCloud.html", plot=cloud, title="Unmatched Cons Word Cloud")


def plotlyWordCloud(text):
    # Create and generate a word cloud image:
    wordcloud = WordCloud(background_color="white").generate(text)

    # Display the generated image:
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    # plt.show()

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data
