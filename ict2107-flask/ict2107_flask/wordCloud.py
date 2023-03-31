from ict2107_flask import app
from flask import Flask, render_template, request
from matplotlib.figure import Figure
from plotly.subplots import make_subplots

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

@app.route('/wordCloud')
def wordCloud():
    cloud = plotlyWordCloud()
    return render_template("wordCloud.html", plot=cloud)


def plotlyWordCloud():
    # Start with one review:
    text = "hello hello hello world"

    # Create and generate a word cloud image:
    wordcloud = WordCloud(background_color="white").generate(text)

    # Display the generated image:
    fig = plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return data
