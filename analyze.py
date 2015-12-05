import json
import datetime
import time
from peewee import *
import sys

db = SqliteDatabase('result/coin_laundry.db')

class Tweet(Model):
    created_at = DateTimeField()
    screen_name = CharField()
    location = CharField()
    tweet = CharField()
    tweetid = IntegerField()

    class Meta:
        database = db

with db.transaction():
    for t in Tweet.select().where(Tweet.id<100).paginate(2,10):
        try:
            print(t.tweet.encode('utf-8', 'replace').decode('utf-8', 'replace'))
        except:
            pass
