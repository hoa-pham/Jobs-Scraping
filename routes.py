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
yext_page = requests.get(url_yext)
twilio_page = requests.get(url_twilio)

def fill(pages, name, h_file):
    page = pages.text
    soup = BeautifulSoup(page, 'html.parser')
    sec = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['opening'])
    data_twilio = []
    for i in range(0, len(sec)):
        row = []
        for j in range(0, 3):
            if j == 0:
                sec[i].a['href'] = sec[i].a['href'].replace(str(sec[i].a.get('href')), green_house_link + str(sec[i].a.get('href')))
                row.append(sec[i].a)
            elif j == 1:
                row.append(name)
            else:
                row.append(sec[i].span)
        data_twilio.append(row)
    code = HTML.table(data_twilio, header_row=['Title', 'Company', 'Location'])
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
            lst = res[i].get('href').split('/')
            if lst[2] == 'departments':
                row = [] 
                res[i]['href'] = res[i]['href'].replace(str(res[i].get('href')), bnb_link + str(res[i].get('href')))
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
    fill(twilio_page, 'Twilio', html_twilio) 
    return render_template("twilio.html")

@app.route("/yext")
def yext():
    fill(yext_page, 'Yext', html_yext)
    return render_template("yext.html")

@app.route("/airbnb")
def airbnb():
    bnb()
    return render_template("airbnb.html")

if __name__ == "__main__":
    app.run(debug=True)

