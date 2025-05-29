import os
import sys
import json
import tweepy
from typing import List, Dict

# Instructions:
# 1. Set your Twitter API credentials as environment variables:
#    TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
# 2. Run: python ai/twitter_api_fetcher.py <query> <count> <output_json>
#    Example: python ai/twitter_api_fetcher.py OpenAI 20 twitter_sample.json

def get_api():
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise RuntimeError('Please set TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, and TWITTER_ACCESS_TOKEN_SECRET environment variables.')
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    return tweepy.API(auth, wait_on_rate_limit=True)

def fetch_tweets(query: str, count: int = 100) -> List[Dict]:
    api = get_api()
    tweets = []
    try:
        for status in tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(count):
            tweets.append({
                "tweetId": status.id_str,
                "username": status.user.screen_name,
                "text": status.full_text,
                # Add more fields as needed
            })
    except Exception as e:
        print(f"Error fetching tweets: {e}")
    return tweets

def main():
    if len(sys.argv) < 4:
        print('Usage: python ai/twitter_api_fetcher.py <query> <count> <output_json>')
        sys.exit(1)
    query = sys.argv[1]
    count = int(sys.argv[2])
    output_json = sys.argv[3]
    tweets = fetch_tweets(query, count)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)
    print(f'Saved {len(tweets)} tweets to {output_json}')

if __name__ == '__main__':
    main() 