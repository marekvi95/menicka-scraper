try:
    from PIL import Image
except ImportError:
    import Image
import os
import re
import urllib.request
import pytesseract

class KozakScrapper:
    
    def __init__(self, tesseract_path: str, kozak_menu_url) -> None:
        self.DAYS = ['Pondělí', 'Úterý', 'Středa', 'Čtvrtek', 'Pátek']
        
        self.tesseract_path = tesseract_path
        self.kozak_menu_url = kozak_menu_url

        self.day_start_index = {}
        self.day_last_index = {}
        self.day_menu = {}
        self.day_soup = {}

        self.price_list = []

    def get_menu_text(self) -> str:
        """Retrieve PNG menu from the URL provided in the constructor
        and run Tesseract OCR
        
        Returns:
            str -- menu text
        """
        try:
            urllib.request.urlretrieve(self.kozak_menu_url, "menu.png")
        except Exception as e:
            print(e)
        
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        menu_text = pytesseract.image_to_string(Image.open('menu.png'), lang='ces')
        return menu_text
    
    def format_menu_text(self, menu_text: str) -> list:
        """Format menu text - remove blank lines, remove digits
        
        Arguments:
            menu_text {str} -- menu text from the OCR 
        
        Returns:
            list -- formated menu
        """
        # remove blank lines
        text = os.linesep.join([s for s in menu_text.splitlines() if s.strip()])
        text_list = text.splitlines()
        # remove substrings with digit and dot (menu items)
        text_list = [re.sub(r'^[1-9]\.', '', s) for s in text_list]
        return text_list
    
    def get_menu_indexes(self, text_list: list) -> None:
        """Get start and last index in the list for each day
        
        Arguments:
            text_list {list} -- formated menu
        """
        iter_days = iter(self.DAYS)
        day = next(iter_days)
        prev_day = day
        
        for idx, line in enumerate(text_list):
            if day in line:
                self.day_start_index[day] = idx
                self.day_last_index[prev_day] = idx
                try:
                    prev_day = day
                    day = next(iter_days)
                except StopIteration:
                    break
    
    def get_daily_menu(self, text_list: str) -> None:
        """[summary]
        
        Arguments:
            text_list {str} -- [description]
        """
        for key, value in self.day_start_index.items():
            try: 
                # add soup of the day to the dictionary - crop day and date from the string
                self.day_soup[key] = text_list[value][len(key)+7:] 
                # add meneu of the day to the dictionary
                self.day_menu[key] = text_list[value+1:self.day_last_index[key]] 
            except KeyError:
                self.day_menu[key] = text_list[value+1:-5]

    def get_food_price(self, text_list: str) -> None:
        """[summary]
        
        Arguments:
            text_list {str} -- [description]
        """
        for line in text_list:
            if ',-' in line:
                self.price_list.append(line[:-2] + ' Kč')
    
    def compose_html_for_day(self, day_number: int) -> str:
        
        assert day_number >= 0 and day_number < 5
        
        html_table_start = """<div class='content'>
            <h2>{}</h2>
            <table class='menu'>""".format(self.DAYS[day_number])
        html_soup = "<tr class='soup'><td class='no'></td><td class='food'>{}</td><td class='prize'></td></tr>\n".format(self.day_soup[self.DAYS[0]])
        html_menu = ""
        for idx, x in enumerate(self.day_menu[self.DAYS[day_number]]):
            html_menu = html_menu + "<tr class='main'><td class='no'>{}. </td><td class='food'>{}</td><td class='prize'>{}</td></tr>\n".format(idx+1, x, self.price_list[idx])

        html_table_end = """</table>
        </div>"""

        html = html_table_start + html_soup + html_menu + html_table_end
        return html

if __name__ == "__main__":
    kozak = KozakScrapper(r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract', 'https://ukozaka.cz/wp-content/uploads/2020/02/koz%C3%A1k-2.png')
    menu_text = kozak.get_menu_text()
    text_list = kozak.format_menu_text(menu_text)
    kozak.get_menu_indexes(text_list)
    kozak.get_daily_menu(text_list)
    kozak.get_food_price(text_list)
    print(kozak.compose_html_for_day(4))
