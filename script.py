import requests
import HTML
import sys
from bs4 import BeautifulSoup

html_twilio = open("templates/twilio.html", "w")
html_yext = open("templates/yext.html", "w")
html_airbnb = open("templates/airbnb.html", "w")
green_house_link = 'https://boards.greenhouse.io'
bnb_link = 'https://www.airbnb.com'
url_twilio = green_house_link + '/twilio/'
url_yext = green_house_link + '/yext/'
url_airbnb = bnb_link + '/careers/departments/' 

def fill( p_url, p_name):
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
    return code

def bnb(p_url):
    data = []
    arr = ['engineering','data-science-analytics','finance-accounting','business-development','customer-experience','design','employee-experience', 'information-technology', 'legal', 'localization','luxury-retreats', 'magical-trips', 'marketing-communications', 'operations', 'photography','product', 'public-policy', 'research', 'samara', 'talent', 'the-art-department', 'trust-and-safety', 'other']
    for sub in arr:
        url = p_url 
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
    return HTML.table(data, header_row=['Title', 'Company', 'Location'])

def write_f(p_url, p_name, p_html):
    p_html.seek(0)
    p_html.truncate()
    p_html.write(""" {%extends "layout.html" %}\n{% block content %}\n""")
    if p_name == 'Airbnb':
        p_html.write(bnb(p_url) + '\n' + "{% endblock %}")
    else:
        p_html.write(fill(p_url, p_name) + '\n' + "{% endblock %}")

