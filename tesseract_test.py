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

iter_days = iter(days)
iter_lines = iter(text.splitlines())

day_start_index = {}
day_last_index = {}
day_menu = {}

text_list = text.splitlines()
# remove substrings with digit and dot (menu items)
text_list = [re.sub(r'^[1-9]\.', '', s) for s in text_list]


day = next(iter_days)
prev_day = day

for idx, line in enumerate(text.splitlines()):
   if day in line:
        print(day)
        print(idx)
        day_start_index[day] = idx
        day_last_index[prev_day] = idx - 1
        try:
            prev_day = day
            day = next(iter_days)
        except StopIteration:
            break

print(day_start_index)
print(day_last_index)

for key, value in day_start_index.items():
    try: 
        day_menu[key] = text_list[value+1:day_last_index[key]]
    except KeyError:
        day_menu[key] = text_list[value+1:-5]
    
    print(day_menu)
