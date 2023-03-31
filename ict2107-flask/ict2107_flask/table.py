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
    # process sentiment data
    readSentiments()

    # TODO replace with sentiments arrays
    # [index num, date, Pos/Neg/Neutral, sentim value, rating, job title, summary, pros, cons]
    # values = [
    #     ['Negative', 'Negative', 'Negative', 'Negative', 'Negative'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],
    #     ['-1', '-4', '-2', '-2', '-2'],]
    values = getArrays.getSentiments()

    # display table based on path
    if (sentim == "negative"):
        table = sentimentTable(values)
        return render_template("table.html", plot=table)
    elif (sentim == "positive"):
        table = sentimentTable(values)
        return render_template("table.html", plot=table)
    elif (sentim == "neutral"):
        table = sentimentTable(values)
        return render_template("table.html", plot=table)


def sentimentTable(values):
    # first data set
    fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3,4,5,6,7,8,9],
        columnwidth = [10,20,20,15,10,30,40,40,40],
        header = dict(
            values = [
                ['Index'],
                ['Date'],
                ['Sentiment'],
                ['Sentiment Value'],
                ['Rating'],
                ['Job Title'],
                ['Summary'],
                ['Pros'],
                ['Cons']],
        line_color='darkslategray',
        fill_color='royalblue',
        align=['left','center','center','center','center','center','left','left','left'],
        font=dict(color='white', size=12),
        height=40,
        ),
        cells=dict(
            values=values,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise','white','white','white','white','white','white','white','white']),
            align=['left','center','center','center','center','center','left','left','left'],
            font_size=12,
            height=30),
    )])

    # convert to json
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON