try:
    from PIL import Image
except ImportError:
    import Image
import os
import re
import pytesseract


# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# Simple image to string
menu_text = pytesseract.image_to_string(Image.open('/Users/marekvitula/Downloads/kozák-2.png'), lang='ces')

days = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek']

# remove blank lines
text = os.linesep.join([s for s in menu_text.splitlines() if s.strip()])

text_list = text.splitlines()
iter_days = iter(days)
iter_lines = iter(text_list)

day_start_index = {}
day_last_index = {}
day_menu = {}
day_soup = {}

price_list = []


# remove substrings with digit and dot (menu items)
text_list = [re.sub(r'^[1-9]\.', '', s) for s in text_list]


day = next(iter_days)
prev_day = day

for idx, line in enumerate(text_list):
   if day in line:
        print(day)
        print(idx)
        day_start_index[day] = idx
        day_last_index[prev_day] = idx
        try:
            prev_day = day
            day = next(iter_days)
        except StopIteration:
            break

print(day_start_index)
print(day_last_index)

for key, value in day_start_index.items():
    try: 
        # add soup of the day to the dictionary - crop day and date from the string
        day_soup[key] = text_list[value][len(key)+7:] 
        # add meneu of the day to the dictionary
        day_menu[key] = text_list[value+1:day_last_index[key]] 
    except KeyError:
        day_menu[key] = text_list[value+1:-5]
    
    print(day_menu)
    print(day_soup)

price_iter = iter(price_list)

for line in text_list:
    if ',-' in line:
        price_list.append(line[:-2] + ' Kč')

print(price_list)

html_table_start = """<div class='content'>
   <h2>{}</h2>
   <table class='menu'>""".format(days[0])
html_soup = "<tr class='soup'><td class='no'></td><td class='food'>{}</td><td class='prize'></td></tr>".format(day_soup[days[0]])
html_menu = ""
for idx, x in enumerate(day_menu[days[0]]):
    html_menu = html_menu + "<tr class='main'><td class='no'>{}. </td><td class='food'>{}</td><td class='prize'>{}</td></tr>\n".format(idx+1, x, price_list[idx])

html_table_end = """</table>
</div>"""

html = html_table_start + html_soup + html_menu + html_table_end
print(html)
