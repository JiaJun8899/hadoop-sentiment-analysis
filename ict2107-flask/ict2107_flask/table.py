from ict2107_flask import app
from flask import Flask, render_template
from matplotlib.figure import Figure

from ict2107_flask.index import *

import base64
from io import BytesIO

import plotly
import plotly.express as px
import plotly.graph_objs as go

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import json

@app.route('/table/<path:sentim>')
def table(sentim):
    # TODO replace with sentiments arrays
    # array of arrays
    # [index num, date, Pos/Neg/Neutral, sentim value, rating, job title, summary, pros, cons]

    # display table based on path
    if (sentim == "negative"):
        values = getArrays.getNegativeSentiments()
        table = sentimentTable("Matched Negative Sentiments", values)
        return render_template("table.html", plot=table)
    elif (sentim == "positive"):
        values = getArrays.getPositiveSentiments()
        table = sentimentTable("Matched Positive Sentiments", values)
        return render_template("table.html", plot=table)
    elif (sentim == "neutral"):
        values = getArrays.getNeutralSentiments()
        table = sentimentTable("Matched Neutral Sentiments", values)
        return render_template("table.html", plot=table)


def sentimentTable(title, values):
    # first data set
    fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3,4,5,6,7,8,9,10,11],
        columnwidth = [10,15,15,15,15,15,10,30,30,40,40],
        header = dict(
            values = [
                ['Index'],
                ['Date'],
                ['Matched Sentiment'],
                ['Unmatched Sentiment'],
                ['Matched Sentiment Value'],
                ['Unmatched Sentiment Value'],
                ['Rating'],
                ['Job Title'],
                ['Summary'],
                ['Pros'],
                ['Cons']],
        line_color='darkslategray',
        fill_color='royalblue',
        align=['left','center','center','center','center','center','center','center','left','left','left'],
        font=dict(color='white', size=12),
        height=40,
        ),
        cells=dict(
            values=values,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise','white','white','white','white','white','white','white','white','white','white']),
            align=['left','center','center','center','center','center','center','center','left','left','left'],
            font_size=12,
            height=30),
    )])

    fig.update_layout(
        title_text=title
    )

    # convert to json
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON