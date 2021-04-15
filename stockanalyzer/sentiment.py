from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pandas as pd


def get_analysis(news_list):
    vader = SentimentIntensityAnalyzer()

    columns = ['ticker','date', 'time', 'headline']
    news_df = pd.DataFrame(news_list, columns=columns)
    ##pd.set_option('display.max_colwidth', 1000)
    scores = news_df['headline'].apply(vader.polarity_scores).tolist()
    scores_df = pd.DataFrame(scores)
    news_df = news_df.join(scores_df, rsuffix='_right')
    news_df['date'] = pd.to_datetime(news_df.date).dt.date
    return news_df

def plot_analysis(news_df):
    
    plt.rcParams['figure.figsize'] = [10, 6]
    mean_scores = news_df.groupby(['ticker','date']).mean()
    mean_scores = mean_scores.unstack()
    mean_scores = mean_scores.xs('compound', axis="columns").transpose()
    mean_scores.plot(kind = 'bar')
    plt.grid()
    plt.savefig('analysis.png')
    plt.close()
