import requests
import smtplib
from datetime import date
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup

from tesseract_test import KozakScrapper

URL = 'https://www.menicka.cz/tisk.php?restaurace='

# list of restaurants with numbers as listed at menicka.cz 
restaurants = {
    'Rubín':'2749',
    'Crowbar':'4865',
    'Kometa Pub Miki':'2678',
    'Na Piavě': '2770',
    }

# list of recipients
recipients = ['huko.kokoska@seznam.cz',...]

restaurants_soup = {}

# list of days in week in czech
weekdays = ['Pondělí','Úterý','Středa','Čtvrtek','Pátek']
today = date.today().weekday()

f = open('html_menu.html', 'w+', encoding="utf-8")

# html with stylesheet
html_str = """
<html>
<head>
    <style media="screen, print" type="text/css">
        html body {
            background-color: white;
            margin: 0em;
            font-size: .75em;
            line-height: 1.3em;
            font-family: Arial, Helvetica, sans-serif;
            color: black;
        }
        
        div#mother {font-size: 100%;}
        
        div.header, div.footer {background-color: #ffffff; padding: .4em; font-size: 1em; text-align: center; font-style: italic;}
        div.footer {1em 0 .5em;}
        img.logo_restaurace {float: left; max-width: 200px;}
        div.logo {text-align: right;}
        div.logo img {width: 200px;}
        
        div.content {}
        
        div.single {width: 100%;}
        div.left {width: 47%; float: left; margin-right: 1em;}
        div.right {width: 47%; float: right; margin-left: 1em;}
        
        div.menicka {
            text-align: center; 
            margin: 1em auto 0.8em; 
            font-size: 1.2em; 
            font-weight: normal; 
            color: #E9654C;
            border-top: 1px solid #ccc;
            padding-top: .2em;
        }
        
        div.clear {clear: both;}
        
        /* HTML EL */
        p {margin: 1em 0em;}

        table.menu {font-size: 1em; border-collapse: collapse; border: 0; margin-bottom: 2em; width: 100%;}
        table.menu tr td {padding: .15em; font-weight: bold; border-bottom: 1px solid #ddd; vertical-align: top;}
        table.menu tr.main td.no {width: 1.5em;}
        table.menu tr.main td.food {font-size: 1em; font-weight: normal;}
        table.menu tr.main td.food span.description {font-weight: normal;}
        table.menu tr.soup td {font-weight: normal; font-style: italic;}
        table.menu tr.info td {background-color: #f3f3f3; border-bottom: 0;}
        table.menu tr td.prize {width: 4.5em; text-align: right; =width: 5.5em; =padding-right: 1em;}
        table.menu tr td em {width: 12px; height: 12px; padding-top: 0px; display: inline-block; border: 1px solid #cccccc; font-size: 8px; -webkit-border-radius: 12px; -moz-border-radius: 12px; border-radius: 10px; text-align: center; font-style: normal; margin-right: 2px;}

        hr {color: #ccc; background: #ccc; border: 0px; height: 1px;}

        h1 {
            font-family: Georgia, 'Times New Roman', Times, serif; 
            font-weight: bold;
            text-align: center;
            margin: 0;
            font-size: 1.8em; 
            color: #ED6E55; 
            line-height: 1.3em;
        }
        
        h2 {
            font-weight: bold;
            margin: 0em 0em .3em;
            font-size: 1.1em; 
            border-bottom: 0px solid #EE6B53;
            padding-bottom: .2em;
        }
        
        table#title {width: 100%; border-collapse: collapse; border: 0; margin: 1em 0em 1.6em;}
        table#title td {text-align: center; vertical-align: middle; border-bottom: 0px solid #EE6B53; padding-bottom: .5em;}
    </style>
</head>
<body>
"""

#html_end = "</body></html>"
html_end = ""

def append_html(html_string):
    """function for appending html to global html string"""
    global html_str
    html_str = html_str + str(html_string)

def get_soup(resturant_number):
    """get HTML soup from the given restaurant number"""
    page = requests.get(URL+resturant_number)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup

def week_number_of_month(date_value):
    # print(date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1])
    return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1])

#print('<h1>'+weekdays[today]+'</h1>')
append_html('<h1>'+weekdays[today]+'</h1>')

for name,number in restaurants.items(): 
    soup = get_soup(number)
    # restaurants_soup[name] = soup

    divs = soup.find_all('div', attrs = {'class':'content'}) 
    
    # html_str = html_str+'<h2>'+name+'</h2><table class="menu">'
    # print('<h2>'+name+'</h2>')
    append_html('<h2>'+name+'</h2>')
    # print('<table class="menu">')
    append_html('<table class="menu">')
    
    soup_food = divs[today].find('tr', attrs = {'class':'soup'})
    print(soup_food.getText())
    soup_food.td.next_sibling.append(' NOT RECOMMENDED BY VÍŤA CH.')
    append_html(soup_food)
    # html_str = html_str + str(soup_food)

    # favorites filter
    for food in divs[today].findAll('tr', attrs = {'class':'main'}):
        print(food.getText())
        food_text = food.getText().lower()

        if 'smažený' in food_text:
            food.td.next_sibling.append(' STAŇA RECOMMENDS')
        if 'salát ' in food_text:
            food.td.next_sibling.append(' VÍŤOVÉ RECOMMEND')
        if 'špenát' in food_text:
            food.td.next_sibling.append(' MARTIN RECOMMENDS')
        if 'výpečky' in food_text:
            food.td.next_sibling.append(' LACO RECOMMENDS')
        if 'holandský' in food_text:
            food.td.next_sibling.append(' LAĎA RECOMMENDS')
        if 'gnocchi' in food_text:
            food.td.next_sibling.append(' LAĎA RECOMMENDS')
        if 'tortilla' in food_text:
            food.td.next_sibling.append(' LAĎA RECOMMENDS')    
        if 'burger' in food_text:
            food.td.next_sibling.append(' EVERYONE RECOMMENDS')

        append_html(food)
        # html_str = html_str + str(food)

    # print('</table>')
    append_html('</table>')
    # html_str = html_str + '</table>'

append_html(html_end)
# html_str = html_str + html_end
kozak_url = 'https://ukozaka.cz/wp-content/uploads/2020/0{}/koz%C3%A1k-{}.png'.format(datetime.today().month, week_number_of_month(datetime.today()))
print(kozak_url)
kozak = KozakScrapper(r'/usr/bin/tesseract', kozak_url)
menu_text = kozak.get_menu_text()
text_list = kozak.format_menu_text(menu_text)
kozak.get_menu_indexes(text_list)
kozak.get_daily_menu(text_list)
kozak.get_food_price(text_list)
html_kozak = kozak.compose_html_for_day(today)
print(html_kozak)

append_html(html_kozak)

f.write(html_str)
f.close()

# Send the message via local SMTP server.
s = smtplib.SMTP('smtp server')

me = "sender mail address"

# message has to be sent separately, because sending to multiple recipients fails...
for r in recipients:
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Kam dnes na oběd?"
    msg['From'] = me
    msg['To'] = r

    # Create the body of the message (a plain-text and an HTML version).
    text = "Kam dnes na oběd?"

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html_str, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, r, msg.as_string())

s.quit()

