from script import *
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/twilio")
def twilio():
    write_f(url_twilio, 'Twilio', html_twilio) 
    return render_template("twilio.html")

@app.route("/yext")
def yext():
    write_f(url_yext, 'Yext', html_yext)
    return render_template("yext.html")

@app.route("/airbnb")
def airbnb():
    write_f(url_airbnb, 'Airbnb', html_airbnb) 
    return render_template("airbnb.html")

if __name__ == "__main__":
    app.run(debug=True)

