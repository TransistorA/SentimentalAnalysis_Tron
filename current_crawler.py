import tweepy
import csv
import pandas as pd

# so that emojis don't 
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

def collect(csvFileName,startTime,endTime):

    ####input your credentials here
    #For account @TeamBot123 , TRXBot
    consumer_key = 'aD0VdJEhOmG27pALUanzBwvuv'
    consumer_secret = 'ovVI2CXSwJ4FayLI7BrusCxQHZje01PEfrbKRmrJ6GYMwh2FZx'
    access_token = '1057247540154900480-604iTbnSXZ5mCK8up01VXZ4vtrj1Rr'
    access_token_secret = 'xpDen6yBtswbAmEhNRqDuCBMXzECmksrbsZxfhPVnmFyR'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)
    #####trx since inception
    # opens or creates files to append
    csvFile = open(csvFileName, 'a')
    #Use CSV Writer
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search,q="#TRX",count=100,
                               lang="en",
                               since = startTime
                            ).items():
        if (not tweet.retweeted) and ('RT @' not in tweet.text) and (tweet.created_at > endTime): #excludes retweets
            print (tweet.created_at, tweet.text.translate(non_bmp_map))
            csvWriter.writerow([tweet.text.encode('utf-8')])
