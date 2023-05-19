from selectorlib import Extractor
import requests 
import json 
from time import sleep
import csv
from dateutil import parser as dateparser

# Create an Extractor by reading from the YAML file
try:
    e = Extractor.from_yaml_file('selectors.yml')
except:
    e = Extractor.from_yaml_file('Scraper/selectors.yml')

def scrape(url):    
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    print(r.text)
    # Simple check to check if page was blocked (Usually 503)
    if "To discuss automated access to Amazon data" in r.text:
        print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
    # Pass the HTML of the page and create 
    # print(e.extract(r.text))
    return e.extract(r.text)

# product_data = []
def read_urls(urls):

    with open('data.csv','w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["title","content","date","variant","images","verified","author","rating","product","url"],quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for url in urls:
            data = scrape(url)
            try:

                if data:
                    for r in data['reviews']:
                        r["product"] = data["product_title"]
                        r['url'] = url
                        # print(r)
                        if 'verified' in r:
                            if 'Verified Purchase' in r['verified']:
                                r['verified'] = 'Yes'
                            else:
                                r['verified'] = 'Yes'
                        r['rating'] = r['rating'].split(' out of')[0]
                        date_posted = r['date'].split('on ')[-1]
                        if r['images']:
                            r['images'] = "\n".join(r['images'])
                        r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
                        writer.writerow(r)

            except:
                print("No data")

def genrate_urls(url):

    id = url.split("/")[5]
    stars = ['one','two','three','four','five']

    print(id)
    links = []
    for i in range(2,11):
      links.append("https://www.amazon.in/product-reviews/"+id+"/ref=cm_cr_arp_d_paging_btm_next_"+str(i)+"?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i))
      


    return links


def generate_data(url):
    try:
        read_urls(genrate_urls(url))
    except Exception as e:
        print("Error ",e)


if __name__ == '__main__':
    generate_data("https://www.amazon.in/OnePlus-Nord-Marble-128GB-Storage/product-reviews/B08695ZSP6/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")



                # sleep(5)