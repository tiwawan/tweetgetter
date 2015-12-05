from requests_oauthlib import OAuth1Session
import json
import datetime
import time
from peewee import *

CK = 'GKfSyzp8iW1rEIg0D21bBXQ8O'                             # Consumer Key
CS = 'Gb7AdIVbMnR9jpGcVQRq6KgXdyhQHYliigWYOmHete9cheLF6Z'         # Consumer Secret
AT = '2838969204-M9jti6tiMFHIBTrHHaVIe8sG1X9DhAwzVuhLqQS' # Access Token
AS = '7SxqI7rO5jo6wkx5VoXw1YCuvCc8FvC9Ub42pk9xe5C6i'         # Accesss Token Secert

# タイムライン取得用のURL
#url = "https://api.twitter.com/1.1/statuses/home_timeline.json"

url = "https://api.twitter.com/1.1/search/tweets.json"

params = {"q":"洗濯", "count": "100", "locale":"ja", "result_type":"recent"}

db = SqliteDatabase('sentaku.db')

class Tweet(Model):
    created_at = DateTimeField()
    screen_name = CharField()
    location = CharField()
    tweet = CharField()
    tweetid = IntegerField()

    class Meta:
        database = db

# OAuth で GET
twitter = OAuth1Session(CK, CS, AT, AS)

db.create_table(Tweet, True)

fp = open("max_id.txt")
max_id = json.load(fp)["max_id"]
params["max_id"] = max_id
fp.close()

while True:
    req = twitter.get(url, params = params)
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline['statuses']:
            try:
                d = datetime.datetime.strptime(tweet['created_at'],
                                               "%a %b %d %H:%M:%S %z %Y")
                name = tweet['user']['screen_name']
                loc = tweet['user']['location']
                t = tweet['text']
                id = tweet['id']
                with db.transaction():
                    Tweet.create(created_at=d,
                                 screen_name=name,
                                 location=loc,
                                 tweet=t,
                                 tweetid=id)
                max_id = id
                if t.count("RT @") == 0:
                    print(id)
                    print(t)
                    print("-"*20)
            except :
                print("SOMETHING HAPPENED")
    else:
        # エラーの場合
        print ("Error: %d" % req.status_code)
    params["max_id"] = str(int(max_id)-1)
    fp = open("max_id.txt","w")
    json.dump({"max_id":params["max_id"]}, fp)
    fp.close()
    time.sleep(60)
        
