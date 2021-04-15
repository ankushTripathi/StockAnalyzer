

import sys
import stockanalyzer
from stockanalyzer import crawler
from stockanalyzer import sentiment
from stockanalyzer import tweets

#Main method
def main():
    #extract args and opts from cli
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    opts = [o for o in sys.argv[1:] if o.startswith("-")]

    # Show help message
    if "-h" in opts or "--help" in opts:
        print(__doc__)
        return
    
    tweets_flag=False
    news_flag=False

    if "-t" in opts or "--tweets" in opts:
        tweets_flag=True

    elif "-n" in opts or "--news" in opts:
        news_flag=True

    if not news_flag and not tweets_flag:
        print("please provide source option -n news or -t tweets")
        print(__doc__)
        return

    if not args:
        print("please provide stock names(ticker) to process")
        print(__doc__)
        return 
    
    for ticker in args:

        if news_flag:
            newsFeedhtml = crawler.get_feeds(ticker,stockanalyzer.NewsFeedUrl)
            newsData = crawler.extractData(ticker,newsFeedhtml)
            news_analysis = sentiment.get_analysis(newsData)
            sentiment.plot_analysis(news_analysis)
        elif tweets_flag:
            df = tweets.get(ticker)
            df = tweets.analyse(df)
            df.to_csv('analyzed_tweets_'+ticker+'.csv',sep='|',encoding='utf-8',index=False)





if __name__ == "__main__":
    main()
