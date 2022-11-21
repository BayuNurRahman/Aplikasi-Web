import streamlit as st
import warnings
warnings.filterwarnings("ignore")
# EDA Pkgs
import pandas as pd
import numpy as np
import pandas as pd
import tweepy
import json
from tweepy import OAuthHandler
import re
import textblob
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import openpyxl
import time
import tqdm

st.set_page_config(
    page_title='Web App',
    page_icon='🐦'
)

#To Hide Warnings
st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_option('deprecation.showPyplotGlobalUse', False)


STYLE = """
<style>
img {
    max-width: 100%;
}
</style> """

def main():
    html_temp = """
	<div style="background-color:yellow;"><p style="color:black;font-size:40px;padding:9px">Crawling Twitter Data Sentiment</p></div>
	"""
    st.markdown(html_temp, unsafe_allow_html=True)
    
    consumer_key = "GcpdrJEU3K2BegvayOkeOuZ2Y"
    consumer_secret = "s8pxiFiYkbvw0yt3m7XuEjDsDh45J3s5iPzd50ehKaz4NNdhr7"
    access_token = "1303271622510403584-QVFnJnmgoTdi36TXX4SOvrjQA99gPK"
    access_token_secret = "M9nxu7zaAxIzqQwpIal7bKOkvtMw4z85mejTPjYwUee6b"

    # Use the above credentials to authenticate the API.

    auth = tweepy.OAuthHandler( consumer_key , consumer_secret )
    auth.set_access_token( access_token , access_token_secret )
    api = tweepy.API(auth)
    df = pd.DataFrame(columns=["Date","User","Tweet",'User_location'])
    
    menu = ["Home", "About", "Sentiment"]
    choice = st.sidebar._selectbox("Sentiment",menu)

    # Write a Function to extract tweets:
    def get_tweets(Topic,Count):
        i=0
            #my_bar = st.progress(100) # To track progress of Extracted tweets
            #for tweet in api.search_tweets(q=Topic,count=10, lang="en"):
        for tweet in tweepy.Cursor(api.search_tweets, q=Topic,count=500,exclude='retweets').items():
            df.loc[i,"Date"] = tweet.created_at
            df.loc[i,"User"] = tweet.user.name
            df.loc[i,"Tweet"] = tweet.text
            df.loc[i,"User_location"] = tweet.user.location
            df.to_csv("Crawling Data Twitter.csv",index=False)
            i=i+1
            if i>Count:
                break
            else:
                pass
    # Function to Clean the Tweet.
    def clean_tweet(tweet):
        return ' '.join(re.sub('(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|([RT])', ' ', tweet.lower()).split())    
        
    # Funciton to analyze Sentiment
    def analyze_sentiment(tweet):
        analysis = TextBlob(tweet)
        if analysis.sentiment.polarity > 0:
            return 'Positive'
        elif analysis.sentiment.polarity == 0:
            return 'Neutral'
        else:
            return 'Negative'
    
    #Function to Pre-process data for Worlcloud
    def prepCloud(Topic_text,Topic):
        Topic = str(Topic).lower()
        Topic=' '.join(re.sub('([^0-9A-Za-z \t])', ' ', Topic).split())
        Topic = re.split("\s+",str(Topic))
        stopwords = set(STOPWORDS)
        stopwords.update(Topic) ### Add our topic in Stopwords, so it doesnt appear in wordClous
        ###
        text_new = " ".join([txt for txt in Topic_text.split() if txt not in stopwords])
        return text_new
    
    # Collect Input from user :
    Topic = str()
    Topic = str(st.text_input("Masukkan topik yang ingin anda cari: (Tekan Enter)"))     
    
    if len(Topic) > 0 :
        
        # Call the function to extract the data. pass the topic and filename you want the data to be stored in.
        with st.spinner("Please wait, waiting for moments"):
            get_tweets(Topic , Count=500)
        st.success('Done ✅')               
    
        # Call function to get Clean tweets
        df['clean_tweet'] = df['Tweet'].apply(lambda x : clean_tweet(x))
    
        # Call function to get the Sentiments
        df["Sentiment"] = df["Tweet"].apply(lambda x : analyze_sentiment(x))        
        
        # See the Extracted Data : 
        if st.button("See the Extracted Data"):
            st.markdown(html_temp, unsafe_allow_html=True)
            st.success("Below is the Extracted Data :")
            st.write(df.head(500))

    if st.button("Exit"):
        st.balloons()

if __name__ == '__main__':
    main()
