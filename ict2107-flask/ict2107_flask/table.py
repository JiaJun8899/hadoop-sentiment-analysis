from ict2107_flask import app
from flask import Flask, render_template
from matplotlib.figure import Figure
from plotly.subplots import make_subplots

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

    # process values
    matchedIndexArray = []
    matchedValueArray = []
    unmatchedIndexArray = []
    unmatchedValueArray = []
    for i, value in enumerate(values[0]):
        matchedIndexArray.append(int(i))
        matchedValueArray.append(int(values[4][i]))
        unmatchedIndexArray.append(int(i))
        unmatchedValueArray.append(int(values[5][i]))

    fig = make_subplots(
    rows=2, cols=1,
    vertical_spacing=0.1,
    specs=[[{"type": "table"}],
           [{"type": "scatter"}]]
    )
    
    # TABLE
    fig.add_trace(go.Table(
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
    ),
    row=1, col=1)


    # SCATTER GRAPH
    fig.add_trace(go.Scatter(
        x = unmatchedIndexArray,
        y = unmatchedValueArray,
        mode="markers",
        name="Unmatched"
    ),
    row = 2, col = 1)

    fig.add_trace(go.Scatter(
        x = matchedIndexArray,
        y = matchedValueArray,
        mode="markers",
        name="Matched"
    ),
    row = 2, col = 1)

    fig.update_layout(
        xaxis_title="Index", 
        yaxis_title="Sentiment Value",
        title_text=title
    )

    fig.update_layout(scattermode="group")

    # convert to json
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


# def plotlyScatter(title, values):

#     # process values
#     matchedIndexArray = []
#     matchedValueArray = []
#     unmatchedIndexArray = []
#     unmatchedValueArray = []
#     for i, value in enumerate(values[0]):
#         matchedIndexArray.append(int(i))
#         matchedValueArray.append(int(values[4][i]))
#         unmatchedIndexArray.append(int(i))
#         unmatchedValueArray.append(int(values[5][i]))\

#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x = matchedIndexArray,
#         y = matchedValueArray,
#         mode="markers",
#         name="Matched"
#     ))

#     fig.add_trace(go.Scatter(
#         x = unmatchedIndexArray,
#         y = unmatchedValueArray,
#         mode="markers",
#         name="Unmatched"
#     ))

#     fig.update_layout(
#         xaxis_title="Index", 
#         yaxis_title="Sentiment Value",
#         title=title
#     )

#     graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

#     return graphJSON