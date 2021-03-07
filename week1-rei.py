from requests_html import HTMLSession
import chompjs
import pandas as pd
import itertools

def fetch(x):
    baseurl = 'https://www.rei.com'
    url = f'https://www.rei.com/c/backpacks?page={x}'
    r = s.get(url)
    results = [baseurl + link.attrs['href'] for link in r.html.find('#search-results > ul > li > a')]
    return list(dict.fromkeys(results))

def parseproduct(url):
    r = s.get(url)
    details = r.html.find('script[type="application/ld+json"]', first=True)
    data = chompjs.parse_js_object(details.text)
    return data
    
def main():
    urls = [fetch(x) for x in range(1,3)]
    #Use itertools to change a list of lists into one full list
    products = list(itertools.chain.from_iterable(urls))
    return [parseproduct(url) for url in products]

if __name__ == '__main__':
    s = HTMLSession()
    df = pd.json_normalize(main())
    df.to_csv('reipacks.csv', index=False)
    print(fin)
