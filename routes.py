import requests
import HTML
from bs4 import BeautifulSoup

html_twilio = open("templates/twilio.html", "w")
html_yext = open("templates/yext.html", "w")
html_airbnb = open("templates/airbnb.html", "w")
green_house_link = 'https://boards.greenhouse.io'
bnb_link = 'https://www.airbnb.com'
url_twilio = green_house_link + '/twilio/'
url_yext = green_house_link + '/yext/'

def fill( p_url, p_name, h_file):
    page = requests.get(p_url).text
    soup = BeautifulSoup(page, 'html.parser')
    sec = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['opening'])
    data = []
    for i in range(0, len(sec)):
        row = []
        for j in range(0, 3):
            if j == 0:
                sec[i].a['href'] = green_house_link + sec[i].a.get('href')
                row.append(sec[i].a)
            elif j == 1:
                row.append(p_name)
            else:
                row.append(sec[i].span)
        data.append(row)
    code = HTML.table(data, header_row=['Title', 'Company', 'Location'])
    h_file.write(code)

def bnb():
    data = []
    arr = ['engineering','data-science-analytics','finance-accounting','business-development','customer-experience','design','employee-experience', 'information-technology', 'legal', 'localization','luxury-retreats', 'magical-trips', 'marketing-communications', 'operations', 'photography','product', 'public-policy', 'research', 'samara', 'talent', 'the-art-department', 'trust-and-safety', 'other']
    for sub in arr:
        url = 'https://www.airbnb.com/careers/departments/'
        url += sub
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        if soup.table == None:
            continue
        res = soup.table.tbody.find_all('a')
        for i in range(0, len(res)):
            if res[i].get('href')[9] == 'd':
                row = [] 
                res[i]['href'] = bnb_link + res[i].get('href')
                row.append(res[i])
                row.append('Airbnb')
            else:
                row.append(res[i].text)
                data.append(row)
                continue
    code = HTML.table(data, header_row=['Title', 'Company', 'Location'])
    html_airbnb.write(code)

from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/twilio")
def twilio():
    fill(url_twilio, 'Twilio', html_twilio) 
    return render_template("twilio.html")

@app.route("/yext")
def yext():
    fill(url_yext, 'Yext', html_yext)
    return render_template("yext.html")

@app.route("/airbnb")
def airbnb():
    bnb()
    return render_template("airbnb.html")

if __name__ == "__main__":
    app.run(debug=True)

