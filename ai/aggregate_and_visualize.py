import json
import sys
from collections import Counter
from typing import List, Dict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re


def aggregate_sentiments(data: List[Dict]) -> Dict[str, int]:
    sentiments = [item.get('sentiment', 'neutral') for item in data]
    return dict(Counter(sentiments))


def plot_sentiment_distribution(sentiment_counts: Dict[str, int], output_path: str):
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    colors = ['#66b3ff', '#ff9999', '#99ff99']
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)], startangle=140)
    plt.title('Sentiment Distribution')
    plt.axis('equal')
    plt.savefig(output_path)
    plt.close()


def plot_sentiment_bar(sentiment_counts: Dict[str, int], output_path: str):
    labels = list(sentiment_counts.keys())
    sizes = list(sentiment_counts.values())
    plt.figure(figsize=(6, 4))
    plt.bar(labels, sizes, color=['#66b3ff', '#ff9999', '#99ff99'][:len(labels)])
    plt.title('Sentiment Distribution')
    plt.ylabel('Count')
    plt.savefig(output_path)
    plt.close()


def generate_wordcloud(texts: List[str], output_path: str):
    text = ' '.join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(output_path)
    plt.close()


def extract_keywords(texts: List[str]) -> List[str]:
    # Simple keyword extraction: split on non-word chars, filter short words
    words = re.findall(r'\b\w{4,}\b', ' '.join(texts).lower())
    return words


def main():
    if len(sys.argv) < 2:
        print('Usage: python ai/aggregate_and_visualize.py <input_json>')
        sys.exit(1)
    input_json = sys.argv[1]
    with open(input_json, 'r', encoding='utf-8') as f:
        data = json.load(f)
    sentiment_counts = aggregate_sentiments(data)
    plot_sentiment_distribution(sentiment_counts, 'sentiment_pie.png')
    plot_sentiment_bar(sentiment_counts, 'sentiment_bar.png')
    texts = [item.get('text', '') for item in data]
    keywords = extract_keywords(texts)
    generate_wordcloud(keywords, 'wordcloud.png')
    print('Saved sentiment_pie.png, sentiment_bar.png, wordcloud.png')

if __name__ == '__main__':
    main() 