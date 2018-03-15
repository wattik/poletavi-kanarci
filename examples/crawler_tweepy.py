#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 21:46:23 2018

@author: pmilicka
"""
from datetime import datetime

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


#Variables that contains the user credentials to access Twitter API 
access_token = "963508546062245888-mUm7MXlcj7qfxTh2H10GjMxSCsPI8qJ"
access_token_secret = "6i0eeK6JwhSzpMZZTXH0pV4ijt1SIvqlRJmHsflbdlWZJ"
consumer_key = "wgKbXgMdxUEXapqxDOuDs2X0g"
consumer_secret = "mbQug9X1MPdoXOGnCpcOSFn7WAsE66WjfN0nI4aGI4HG2nw3os"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
    fout =None
    cnt = 0
    
    def __init__(self):
        self.fout = open("data.txt", "w")
        self.fout.write(str(datetime.now().time())+"\n")
        
    def on_data(self, data):
        self.fout.write(data)
        self.cnt += 1
        print(self.cnt)
        self.fout.write("\n\n")
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    try:
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
        stream.filter(track = ["NBA"], encoding = "utf8")
    except:
        
        l.fout.write("\n" + str(datetime.now().time()))
        l.fout.close()