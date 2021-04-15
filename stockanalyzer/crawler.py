from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

#get news feeds for particular stock
def get_feeds(ticker,url):

    web_url = url + ticker
    req = Request(url=web_url,headers={"User-Agent": "Chrome"}) 
    response = urlopen(req)    
    html = BeautifulSoup(response,"html.parser")
    news_table = html.find(id='news-table')
    return news_table


def extractData(ticker,news_table):

    news_list = []
    for i in news_table.findAll('tr'):
        
        text = i.a.get_text() 
        
        date_scrape = i.td.text.split()

        if len(date_scrape) == 1:
            time = date_scrape[0]
            
        else:
            date = date_scrape[0]
            time = date_scrape[1]
        
        news_list.append([ticker,date, time, text])
    return news_list