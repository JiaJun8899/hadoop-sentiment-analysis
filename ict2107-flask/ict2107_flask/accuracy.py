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
    values = getArrays.getAccuracy()
    table = accuracyTable("Accuracy Table", values)
    return render_template("accuracy.html", plot=table)


def accuracyTable(title, values):
    fig = go.Figure(data=[go.Table(
        columnorder = [1,2,3],
        columnwidth = [10,15,10],
        header = dict(
            values = [
                ['Matched/Unmatched'],
                ['Category'],
                ['Value']],
        line_color='darkslategray',
        fill_color='royalblue',
        align=['center','center','center'],
        font=dict(color='white', size=12),
        height=40,
        ),
        cells=dict(
            values=values,
            line_color='darkslategray',
            fill=dict(color=['paleturquoise','white','white']),
            align=['center','center','center'],
            font_size=12,
            height=30),
    )])

    fig.update_layout(
        title_text=title
    )

    # convert to json
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON