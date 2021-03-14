from requests_html import HTMLSession
import pandas as pd


def get_asins(search):
    r = s.get(f'https://www.amazon.co.uk/s?k={search}')
    asins = r.html.find('div.s-main-slot div[data-asin]')
    return [asin.attrs['data-asin'] for asin in asins if asin.attrs['data-asin'] != '']

def getdata(asin):
    r = s.get(f'https://www.amazon.co.uk/dp/{asin}')
    #print(r.html.html)
    productname = r.html.find('#productTitle', first=True).full_text.strip()
    try:
        ratingscount =  r.html.find('#acrCustomerReviewText', first=True).full_text.strip()
    except:
        ratingscount = 0
    reviews = r.html.find('div[data-hook=review]')
    topreviews = []
    for rev in reviews:
        ratings = {
        'title': rev.find('a[data-hook=review-title] span', first=True).full_text,
        'rating': rev.find('i[data-hook=review-star-rating] span', first=True).full_text,
        }
        topreviews.append(ratings)    
    
    product = {
        'productname': productname,
        'ratingscount': ratingscount,
        'reviews': topreviews
    }
    print(product)
    return product

def main():
    search = 'nvme'
    asins = get_asins(search)
    print(f'Found {len(asins)} asins')
    print(asins)
    results = [getdata(asin) for asin in asins]
    df = pd.DataFrame(results)
    df.to_csv(search + '.csv', index=False)
    return

if __name__ == '__main__':
    s = HTMLSession()
    main()
