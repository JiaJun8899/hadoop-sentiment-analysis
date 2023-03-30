from flask import Flask, render_template, request
import sys

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>hello world</p>"

@app.route("/openFile", methods=['GET', 'POST'])
def upload_file():
    uwu = "ohmaiohmaigawd"

    if request.method == 'POST':
        foo = request.files['file']
        contents = foo.readline()
             
        return f'<p>{contents}<p>'
    return render_template("upload.html")



# def openFilePage(): 
#     if 'file' not in request.files:
#         return "<p>ohno</p>"

#     file = request.files['file']
#     data = file.read()

#     testData = '<h3>yas queen</h3>'

#     return render_template("openFile.html") + testData + data