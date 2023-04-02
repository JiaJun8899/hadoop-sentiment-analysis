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

@app.route('/accuracy')
def accuracy():
    matchedArray = getArrays.getMatchedAccuracy()
    unmatchedArray = getArrays.getUnmatchedAccuracy()
    table = accuracyTable("Accuracy Tables", matchedArray, unmatchedArray)
    return render_template("accuracy.html", plot=table)


def accuracyTable(title, matchedArray, unmatchedArray):
    fig = make_subplots(
    rows=2, cols=1,
    vertical_spacing=0.1,
    specs=[[{"type": "table"}],
           [{"type": "table"}]]
    )

    fig.add_trace(go.Table(
        columnorder = [1,2],
        columnwidth = [10,10],
        header = dict(
            values = [
                ['Category (Matched)'],
                ['Value']],
        line_color='darkslategray',
        fill_color='royalblue',
        align=['center','center'],
        font=dict(color='white', size=12),
        height=40,
        ),
        cells=dict(
            values=matchedArray,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise','white']),
            align=['center','center'],
            font_size=12,
            height=30),
    ),
    row=1, col=1)

    fig.add_trace(go.Table(
        columnorder = [1,2],
        columnwidth = [10,10],
        header = dict(
            values = [
                ['Category (Unmatched)'],
                ['Value']],
        line_color='darkslategray',
        fill_color='royalblue',
        align=['center','center'],
        font=dict(color='white', size=12),
        height=40,
        ),
        cells=dict(
            values=unmatchedArray,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise','white']),
            align=['center','center'],
            font_size=12,
            height=30),
    ),
    row=2, col=1)

    fig.update_layout(
        title_text=title
    )

    # convert to json
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON