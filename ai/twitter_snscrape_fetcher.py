import sys
import json
import snscrape.modules.twitter as sntwitter

# Usage: python ai/twitter_snscrape_fetcher.py <query> <count> <output_json>
# Example: python ai/twitter_snscrape_fetcher.py OpenAI 20 twitter_sample.json

def fetch_tweets(query, count):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i >= count:
            break
        tweets.append({
            "tweetId": str(tweet.id),
            "username": tweet.user.username,
            "text": tweet.content,
        })
    return tweets

def main():
    if len(sys.argv) < 4:
        print('Usage: python ai/twitter_snscrape_fetcher.py <query> <count> <output_json>')
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