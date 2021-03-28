from requests_html import HTMLSession
import re
from datetime import date
from csv import DictWriter

def getprice_ander():
    r = s.get('https://www.andertons.co.uk/shure-sm7b-dynamic-vocal-mic-sm7b')
    return r.html.find('span.product-price', first=True).text

def getprice_gear():
    r = s.get('https://www.gear4music.com/PA-DJ-and-Lighting/Shure-SM7B-Dynamic-Studio-Microphone/G6X')
    return r.html.find('span.c-val', first=True).text

def getprice_daws():
    r = s.get('https://www.dawsons.co.uk/93267/shure-sm7b-vocal-microphone')
    return r.html.find('span[itemprop=price]', first=True).text

def getprice_west():
    r = s.get('https://www.westenddj.co.uk/shure-sm7b')
    return r.html.find('span[itemprop=price]', first=True).text

def clean(price):
    return float(re.sub("[^0-9.]", "", price))

def main():
    today = date.today()
    entry = {
        'date': today.strftime("%d/%m/%Y"),
        'ander': clean(getprice_ander()),
        'gear': clean(getprice_gear()),
        'daws': clean(getprice_daws()),
        'west': clean(getprice_west()),
    }
    return entry

def save_tocsv(entry):
    columns = ['date', 'ander', 'gear', 'daws', 'west']
    with open('productdata.csv', 'a') as f:
        w = DictWriter(f, fieldnames=columns)
        w.writerow(entry)
    return

if __name__ == '__main__':
    s = HTMLSession()
    entry = main()
    save_tocsv(entry)
