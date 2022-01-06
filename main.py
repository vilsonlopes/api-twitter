from typing import Any, Dict, List
import tweepy
from fastapi import FastAPI
from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from pydantic import BaseModel
from pymongo import MongoClient


client = MongoClient('mongodb://vilson:102030@localhost:27017/')
db = client.apitwitter
trends_collection = db.trends


class TrendItem(BaseModel):
    name: str
    url: str


BRAZIL_WOE_ID = 23424768


def get_trends(woe_id: int) -> List[Dict[str, Any]]:
    auth = tweepy.OAuthHandler(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    trends = api.get_place_trends(woe_id)
    return trends[0]["trends"]


app = FastAPI()


@app.get("/trends", response_model=List[TrendItem])
def get_trends_route():
    trends = get_trends(woe_id=BRAZIL_WOE_ID)
    trends_collection.find({})
    trends_collection.insert_many(trends)
    return list(trends)
