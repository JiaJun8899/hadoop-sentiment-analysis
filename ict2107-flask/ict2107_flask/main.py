from ict2107_flask import app

@app.route("/")
def index():
    return "<p>Index</p>"