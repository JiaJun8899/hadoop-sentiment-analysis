from ict2107_flask import app
from flask import Flask, render_template, request
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
import csv

@app.route('/barPlot/<path:type>')
def barPlot(type):
    if (type == "matchedJob"):
        title = "Matched Job Satisfaction Bar Plot"
        # get job bar plot data
        labels = getArrays.getMatchedJobsArrayBPJ()
        originalPos = getArrays.getMatchedPositiveArrayBPJ()
        originalNeg = getArrays.getMatchedNegativeArrayBPJ()
        originalNeutral = getArrays.getMatchedNeutralArrayBPJ()
        bar = plotlyDoubleBarPlot(title, labels, originalPos, originalNeg, originalNeutral)
        return render_template("barPlot.html", plot=bar)
    elif (type == "unmatchedJob"):
        title = "Unmatched Job Satisfaction Bar Plot"
        # get job bar plot data
        labels = getArrays.getUnmatchedJobsArrayBPJ()
        originalPos = getArrays.getUnmatchedPositiveArrayBPJ()
        originalNeg = getArrays.getUnmatchedNegativeArrayBPJ()
        originalNeutral = getArrays.getUnmatchedNeutralArrayBPJ()
        bar = plotlyDoubleBarPlot(title, labels, originalPos, originalNeg, originalNeutral)
        return render_template("barPlot.html", plot=bar)
    elif (type == "matchedYear"):
        title = "Matched Year Satisfaction Bar Plot"
        # get year bar plot data
        labels = getArrays.getYearArrBPY()
        originalPos = getArrays.getPositiveArrBPY()
        originalNeg = getArrays.getNegativeArrBPY()
        originalNeutral = getArrays.getNeutralArrBPY()

        labels = labels[:len(labels)//2]
        originalPos = originalPos[:len(originalPos)//2]
        originalNeg = originalNeg[:len(originalNeg)//2]
        originalNeutral = originalNeutral[:len(originalNeutral)//2]
        
        bar = plotlyDoubleBarPlot(title, labels, originalPos, originalNeg, originalNeutral)
        return render_template("barPlot.html", plot=bar)
    elif (type == "unmatchedYear"):
        title = "Unmatched Year Satisfaction Bar Plot"
        # get year bar plot data
        labels = getArrays.getYearArrBPY()
        originalPos = getArrays.getPositiveArrBPY()
        originalNeg = getArrays.getNegativeArrBPY()
        originalNeutral = getArrays.getNeutralArrBPY()

        labels = labels[len(labels)//2:]
        originalPos = originalPos[len(originalPos)//2:]
        originalNeg = originalNeg[len(originalNeg)//2:]
        originalNeutral = originalNeutral[len(originalNeutral)//2:]

        bar = plotlyDoubleBarPlot(title, labels, originalPos, originalNeg, originalNeutral)
        return render_template("barPlot.html", plot=bar)


def plotlyDoubleBarPlot(title, labels, originalPos, originalNeg, originalNeutral):
    # add widths based on number of job titles
    widthArray = []
    for x in labels:
        widthArray.append(10)
    widths = np.array(widthArray)

    # populate from from data array
    original = {
        "Positive": [],
        "Negative": [],
        "Neutral": []
    }
    original["Positive"] = originalPos
    original["Negative"] = originalNeg
    original["Neutral"] = originalNeutral
    
    # store percentage of positive and negatives
    dataPercentage = {
        "Positive": [],
        "Negative": [],
        "Neutral": []
    }
    for index, x in enumerate(original["Positive"]):
        # convert to percentage values, 2 dp
        total = originalPos[index] + originalNeg[index] + originalNeutral[index]
        dataPercentage["Positive"].append(float("{:.2f}".format((originalPos[index] / total) * 100)))
        dataPercentage["Negative"].append(float("{:.2f}".format((originalNeg[index] / total) * 100)))
        dataPercentage["Neutral"].append(float("{:.2f}".format((originalNeutral[index] / total) * 100)))

    # colour array
    colour = ['#43AA8B', '#DB3A34', "#948D9B"]
    # colour = ['#a172cc', '#7227b8', "#a3a0a0"]

    # create graph
    fig = go.Figure()
    for index, key in enumerate(dataPercentage):
        fig.add_trace(go.Bar(
            name=key,
            y=dataPercentage[key],
            x=np.cumsum(widths)-widths,
            marker_color=colour[index],
            width=widths,
            offset=0,
            customdata=np.transpose([labels, widths * dataPercentage[key], original[key]]),
            # texttemplate="%{y}%",   # doesn't scale with scroll bar
            # textposition="auto",
            # textangle=0,
            textfont_color="white",
            hovertemplate="<br>".join([
                "Original Value: %{customdata[2]}",
                "Percentage: %{y}%",
                # "width: %{width}",
                # "height: %{y}",
                # "area: %{customdata[1]}",
            ])
        ))

    fig.update_xaxes(
        tickvals=np.cumsum(widths)-widths/2,
        ticktext= ["%s" % (l) for l in zip(labels)]
        # ticktext= ["%s<br>%d" % (l, w) for l, w in zip(labels, widths)]
    )

    fig.update_xaxes(range=[0,100])
    fig.update_yaxes(range=[0,100])

    fig.update_layout(
        title_text=title,
        barmode="stack",
        uniformtext=dict(mode="hide", minsize=10),
        xaxis=dict(rangeslider=dict(visible=True), type="linear")
    )    

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
