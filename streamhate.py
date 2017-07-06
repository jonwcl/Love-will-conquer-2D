import tweepy
from tweepy import OAuthHandler 
from tweepy import Stream
from tweepy.streaming import StreamListener
 
consumer_key = 'XOXXMQmr88yzTkLrc2i7AWNcI'
consumer_secret = 'MtmtHhwwz3WiTuKQbyrDctJl2NqFC4sKtcNhcnxyS9yvUagO1B'
access_token = '2696721355-9DUnNhSbVaY2ZKQKxcyWzG5DNgsdGT2dfI1kj6Q'
access_secret = 'e6I9wdYmrNemFshXmfeInVd2bjGvkwG8EJfiJiQ5NzZfJ'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('pythonhate.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("there is an error in ondata function")
        return True
 
    def on_error(self, status):
        print(status)
        return True
 
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['hate'])