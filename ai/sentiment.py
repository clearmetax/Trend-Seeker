import logging

try:
    from transformers import pipeline
    _transformers_available = True
except ImportError:
    _transformers_available = False

try:
    from textblob import TextBlob
    _textblob_available = True
except ImportError:
    _textblob_available = False

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.method = None
        if _transformers_available:
            try:
                self.analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
                self.method = "transformers"
            except Exception as e:
                logger.warning(f"Transformers pipeline failed: {e}")
        if self.method is None and _textblob_available:
            self.method = "textblob"
        if self.method is None:
            raise ImportError("No sentiment analysis backend available. Please install 'transformers' or 'textblob'.")

    def classify(self, text):
        if self.method == "transformers":
            result = self.analyzer(text[:512])[0]  # Truncate for model input
            label = result['label'].lower()
            if label == "positive":
                return "positive"
            elif label == "negative":
                return "negative"
            else:
                return "neutral"
        elif self.method == "textblob":
            polarity = TextBlob(text).sentiment.polarity
            if polarity > 0.1:
                return "positive"
            elif polarity < -0.1:
                return "negative"
            else:
                return "neutral"
        else:
            raise RuntimeError("No sentiment analysis method initialized.")

# Example usage:
# analyzer = SentimentAnalyzer()
# print(analyzer.classify("I love this!")) 