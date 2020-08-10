import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "8Mw0a6GutZbrdGc9ObWrtY62d"
consumer_secret = "WHNyQUV4dtdVr1tJZ056TkcniQFC7DDc4TuoZXAD7TPHWhBhJk"
access_key = "846995107899478020-j020Oq0uqIC1htIe62Djsh4wo777MU2"
access_secret = "2PM178d3DM5zZX4swxBScCbZgqwdi4k7sh0CFEGHzWI6B"


def get_all_tweets(screen_name):
    #authentication part
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    alltweets = []  
    
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1  #reference of old tweet(200th)
    
    
    len = 4    #again looping 4 times (200+4(200))
    while len > 0:
        print(f"getting tweets before {oldest}")
        
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        
        alltweets.extend(new_tweets)
        
        oldest = alltweets[-1].id - 1
        
        len = len-1
    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    
    with open(f'new_{screen_name}_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)
    
    pass


if __name__ == '__main__':
    scan = input("Enter twitter id to download tweets:")
    get_all_tweets(scan)
    print("1000 tweets downloaded so far")
