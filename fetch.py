import pika
import config
import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = config.api_key
consumer_secret = config.api_secretKey
access_key = config.acess_token
access_secret = config.acess_tokenSecret


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
    
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]  #creating a 2D array to store tweets
    
    with open(f'new_{screen_name}_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])        #writing the CSV file.
        writer.writerows(outtweets)
    
    pass


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='ACCOUNT_DOWNLOADER')

    message = ""

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        message = body
        get_all_tweets(body)
        print("1000 tweets downloaded so far")
        
    channel.basic_consume(queue='ACCOUNT_DOWNLOADER',
                      auto_ack=True,
                      on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    


